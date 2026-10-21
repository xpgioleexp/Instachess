# Handoff: @pawn.to.king.chess Instagram page

Read this first. It covers everything made so far and what's left to do.

## The account
- Instagram: **@pawn.to.king.chess** (display name PawnToKing), a Creator account, 0 posts as of Oct 20, 2026.
- It's connected in Composio (toolkit `instagram`, account id `instagram_rowed-framea`). Composio still shows the old username, little.us.game, but it's the same account.
- Profile picture: `profile-pictures/pfp-pawn-to-king.png` (already set).
- Bio, not set yet:
  ```
  Gain rating, one idea a day
  Tactics · Openings · Mindset
  Daily puzzle, answer in Stories
  ```

## Next task: post the puzzles carousel
- Slides: `instagram-ready-jpeg/puzzles/01-cover.jpg` … `08-close.jpg` (1080×1350 JPEG, 4:5, in this order).
- Why it didn't post from the first session: Instagram has to download each image from a public HTTPS link (`image_url`), or the image has to be in Composio's file storage (`image_file` / `child_image_files` with an `s3key`). The first session had neither.
- Steps (Composio): get public URLs or s3keys for the 8 JPEGs → `INSTAGRAM_POST_IG_USER_MEDIA` once per slide with `is_carousel_item: true` → `INSTAGRAM_CREATE_CAROUSEL_CONTAINER` with the 8 child ids in order, plus the caption → `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` with the parent id → `INSTAGRAM_GET_IG_MEDIA` to get the permalink.
- Music: the API can't attach music. After it's published, the owner adds a song in the app: ⋯ › Edit › add audio (possible since July 2026).
- Caption (5 hashtags max, which is Instagram's current limit):
  ```
  3 puzzles. Easy, medium, hard 🧩
  Answers are on the slide right after each puzzle, so no peeking.

  Comment your score (0–3) 👇
  Save it and try again tomorrow if you missed one.
  #chess #chesspuzzle #chesstactics #chesstips #learnchess
  ```

## What's in this folder
| Folder | What |
| --- | --- |
| `slides-png/` | All 4 carousels as PNG, numbered in posting order |
| `instagram-ready-jpeg/puzzles/` | Puzzles carousel as JPEG, ready for the API |
| `profile-pictures/` | 3 profile picture options (pawn-to-king is the one in use) |
| `source/<carousel>/` | Editable slide sources (`.dc.html` + `canvas.json`) |
| `scripts/` | `export.py` renders `.dc.html` slides to PNG with Playwright; `make.py` renders the puzzle Reel and the knight pfps; `pfp_promo.py` renders the pawn-to-king pfp. Fonts: Anton (in `fonts/`), Inter, DejaVu Sans (system) |
| `video/puzzle-reel.mp4` | 17 s vertical puzzle Reel (the owner is focusing on carousels for now) |

## The 4 carousels
| Carousel | Slides | Status |
| --- | --- | --- |
| Puzzles: 3 puzzles easy→hard with answers | 8 | **Post this one first** |
| Italian Game: moves, f7 target, plan, Fried Liver trap, puzzle, mistakes | 9 | Ready |
| Chess principles: center, develop, castle, forks, checks/captures/threats | 7 | Ready (owner finds it too generic) |
| Mindset: The Closer's Mindset, 5 rules | 7 | Ready |

Every chess position was checked move by move. Puzzle answers: 1) Re8# (back rank), 2) Ne7+ forks king and queen, then Nxc6, 3) 1.Qg8+! Rxg8 2.Nf7# (smothered mate).

## Design rules
- Owner's instruction: **use the frontend-design skill for every design.**
- Look: black #0B0B0B, gold #D4AF37, paper #F5F1E6, stone #B9B1A0, board #EADBB8 / #9C7A45. Anton headlines, Inter body text. Gold only marks the idea on the board (arrows, ringed squares) and the Save button.
- Avoid: one gold word inside a headline, all-caps labels, and automatic capitals on chess notation (they turn Nf3 into NF3). The mindset and chess-principles carousels still have the first two of these and could be restyled.
- Handle on every slide: @pawn.to.king.chess.
- The design canvases don't open on the owner's iPad, so always deliver PNG/JPEG exports.

## Links (owner's claude.ai account)
- 90-day content plan doc: https://claude.ai/artifact/QmntRhCyXc4dctbdhyu27J. It has positioning, schedule (Mon tactics, Tue puzzle, Wed opening, Thu blunder review, Fri mindset, Sat famous game), first 30 posts, slide outlines, Reel scripts, hooks, growth routine, 90-day milestones.
- Design canvases: puzzles https://claude.ai/artifact/5Y5JoEDoPNLw6L5HspSkDE · Italian Game https://claude.ai/artifact/WzprFFW8SjobaUwVwBKBQK · chess principles https://claude.ai/artifact/Fos66bZHN3Pv6AjwrLr6os · mindset https://claude.ai/artifact/JPmtLWaZpiNsK8UTmCsZ9j
