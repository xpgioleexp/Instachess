import functools, http.server, json, os, re, sys, threading
from PIL import Image
from playwright.sync_api import sync_playwright

# Usage: python3 scripts/export.py [carousel ...]   (default: all four)
# Writes slides-png/<carousel>/NN-<slide>.png, plus instagram-ready-jpeg/<carousel>/ JPEGs.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETS = sys.argv[1:] or ['mindset', 'chess-principles', 'italian-game', 'puzzles']
CHROMIUM = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

SHIM = r"""
<script>
window.DCLogic = class { constructor(p){ this.props = p || {}; this.state = {}; } setState(s){ Object.assign(this.state, s); } forceUpdate(){} };
function dcResolve(path, scope){
  path = path.trim();
  if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
  if (path === 'true') return true; if (path === 'false') return false;
  let v = scope; for (const k of path.split('.')) { if (v == null) return ''; v = v[k]; }
  return v == null ? '' : v;
}
function dcSub(str, scope){
  const whole = str.match(/^\s*\{\{([^}]+)\}\}\s*$/);
  if (whole) return dcResolve(whole[1], scope);
  return str.replace(/\{\{([^}]+)\}\}/g, (_, p) => String(dcResolve(p, scope)));
}
function dcRender(node, scope, parent){
  if (node.nodeType === 3) { parent.appendChild(document.createTextNode(dcSub(node.textContent, scope))); return; }
  if (node.nodeType !== 1) return;
  const tag = node.tagName.toLowerCase();
  if (tag === 'helmet') { node.querySelectorAll('style').forEach(s => document.head.appendChild(s.cloneNode(true))); return; }
  if (tag === 'sc-for') {
    const list = dcSub(node.getAttribute('list'), scope) || [];
    const as = node.getAttribute('as') || 'item';
    list.forEach((item, i) => { const s = Object.assign({}, scope, { [as]: item, $index: i }); node.childNodes.forEach(c => dcRender(c, s, parent)); });
    return;
  }
  if (tag === 'sc-if') { if (dcSub(node.getAttribute('value'), scope)) node.childNodes.forEach(c => dcRender(c, scope, parent)); return; }
  const el = node.cloneNode(false);
  for (const a of Array.from(node.attributes)) {
    if (a.name.startsWith('hint-')) { el.removeAttribute(a.name); continue; }
    el.setAttribute(a.name, String(dcSub(a.value, scope)));
  }
  parent.appendChild(el);
  node.childNodes.forEach(c => dcRender(c, scope, el));
}
document.addEventListener('DOMContentLoaded', () => {
  const sc = document.querySelector('script[data-dc-script]');
  const Component = new Function('DCLogic', sc.textContent + '\nreturn Component;')(window.DCLogic);
  const vals = new Component({}).renderVals() || {};
  const xdc = document.querySelector('x-dc');
  const tpl = document.createElement('template'); tpl.innerHTML = xdc.innerHTML;
  const frag = document.createDocumentFragment();
  tpl.content.childNodes.forEach(c => dcRender(c, vals, frag));
  xdc.replaceWith(frag);
  window.__ready = true;
});
</script>
"""

FONTFACE = "<style>@font-face{font-family:'Anton';src:url('/fonts/Anton-Regular.ttf') format('truetype');}</style>"

def slug(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

# Serve the repo over HTTP so slides can load ./pieces/ and the Anton font by relative URL.
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT))
srv.RequestHandlerClass.log_message = lambda *a: None
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:%d/' % srv.server_address[1]

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=CHROMIUM if os.path.exists(CHROMIUM) else None)
    page = browser.new_page(viewport={'width': 1080, 'height': 1350})
    for name in SETS:
        proj = os.path.join(ROOT, 'source', name)
        canvas = json.load(open(os.path.join(proj, 'canvas.json')))
        dest = os.path.join(ROOT, 'slides-png', name); os.makedirs(dest, exist_ok=True)
        jdest = os.path.join(ROOT, 'instagram-ready-jpeg', name); os.makedirs(jdest, exist_ok=True)
        paths = []
        for idx, f in enumerate(canvas['order'], 1):
            html = open(os.path.join(proj, f)).read()
            html = html.replace('<script src="./support.js"></script>', SHIM)
            html = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>', '', html)
            html = html.replace('</head>', FONTFACE + '<style>body{margin:0}</style></head>', 1)
            tmp = os.path.join(proj, '_tmp-%02d.html' % idx)  # next to the source so ./pieces/ resolves; unique name dodges the HTTP cache
            open(tmp, 'w').write(html)
            page.goto(BASE + os.path.relpath(tmp, ROOT))
            page.wait_for_function('window.__ready === true')
            page.evaluate("Promise.all([document.fonts.load('96px Anton'), document.fonts.load('600 26px Inter'), document.fonts.load('64px \"DejaVu Sans\"')]).then(() => document.fonts.ready)")
            page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
            page.wait_for_timeout(150)
            title = canvas['boards'][f].get('title', f)
            png = os.path.join(dest, '%02d-%s.png' % (idx, slug(re.sub(r'^\d+\s*', '', title))))
            page.screenshot(path=png, clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1350})
            Image.open(png).convert('RGB').save(os.path.join(jdest, os.path.basename(png)[:-4] + '.jpg'), quality=92, subsampling=0)
            paths.append(png)
            os.remove(tmp)
        print(name, len(paths))
    browser.close()
