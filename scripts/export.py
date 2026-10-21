import json, os, re, sys, zipfile
from playwright.sync_api import sync_playwright

ROOT = sys.argv[1]
OUT = os.path.join(ROOT, 'exports')
ANTON = os.path.join(ROOT, 'fonts', 'Anton-Regular.ttf')
SETS = [('carousel', 'mindset'), ('chess', 'chess-principles'), ('italian', 'italian-game'), ('puzzles', 'puzzles')]

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

FONTFACE = "<style>@font-face{font-family:'Anton';src:url('file://%s') format('truetype');}</style>" % ANTON

def slug(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

os.makedirs(OUT, exist_ok=True)
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={'width': 1080, 'height': 1350})
    for folder, name in SETS:
        proj = os.path.join(ROOT, folder, 'project')
        canvas = json.load(open(os.path.join(proj, 'canvas.json')))
        dest = os.path.join(OUT, name); os.makedirs(dest, exist_ok=True)
        paths = []
        for idx, f in enumerate(canvas['order'], 1):
            html = open(os.path.join(proj, f)).read()
            html = html.replace('<script src="./support.js"></script>', SHIM)
            html = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>', '', html)
            html = html.replace('</head>', FONTFACE + '<style>body{margin:0}</style></head>', 1)
            tmp = os.path.join(dest, '_tmp.html'); open(tmp, 'w').write(html)
            page.goto('file://' + tmp)
            page.wait_for_function('window.__ready === true')
            page.evaluate("Promise.all([document.fonts.load('96px Anton'), document.fonts.load('600 26px Inter'), document.fonts.load('64px \"DejaVu Sans\"')]).then(() => document.fonts.ready)")
            page.wait_for_timeout(150)
            title = canvas['boards'][f].get('title', f)
            png = os.path.join(dest, '%02d-%s.png' % (idx, slug(re.sub(r'^\d+\s*', '', title))))
            page.screenshot(path=png, clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1350})
            paths.append(png)
            os.remove(tmp)
        z = os.path.join(OUT, name + '-slides.zip')
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
            for p in paths: zf.write(p, os.path.basename(p))
        print(name, len(paths))
    browser.close()
