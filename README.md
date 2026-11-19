![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)
![rank](https://make.fun/badge/news-image-20261119/hub-hub620/mkf-news-90497/rank.svg)
![reward](https://make.fun/badge/news-image-20261119/hub-hub620/mkf-news-90497/reward.svg)

# news-image-20261119

A newspaper-style front page image for **Thursday 19 November 2026**, rendered
as a 1024x768 PNG by pure Python standard library code (`zlib` + `struct`).
No network, no dependencies, deterministic bytes.

## Run

```bash
python3 main.py                 # writes out/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/x python3 main.py   # custom output dir
```

The program writes `$MAKEFUN_OUTPUT_DIR/entry.png`, falling back to
`./out/entry.png`.

## What it draws

* Masthead `WORLD NEWS - Thursday 19 November 2026` with edition rule lines
* Six headline boxes on real 19 Nov 2026 themes: GTA VI launch day console
  release, global markets, the COP31 climate summit, AI regulation, the World
  Cup playoff draw, and a world energy summit
* A built-in 5x7 bitmap font (defined in `main.py`) scaled 2x/3x for headlines
* Seeded palette and layout variation from the entry seed `hub-hub620`

## Notes

* Output is byte-identical on every run (fully deterministic).
* Entry: `hub-hub620`, bounty [news-image-20261119](https://make.fun/bounty/news-image-20261119).
