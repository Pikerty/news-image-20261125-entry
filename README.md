# The World in One Page — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Pikerty/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Pikerty/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the make.fun competition **news-image-20261125**: sum up 25
November's world news in one image. Bounty page:
https://make.fun/bounty/news-image-20261125 — join make.fun with the
referral link https://make.fun/r/mpwgq2aa.

The image is a one-page newspaper front page for **Wednesday 25 November
2026**, drawn from stories reported that day:

- **Top story** — Iran's Revolutionary Guard says two oil tankers struck
  naval mines and caught fire in the Strait of Hormuz; Tehran says the
  vessels had taken an unauthorised route.
- **Middle East / Saudi Arabia** — Houthi drone strike on a Riyadh
  skyscraper injures 11; the Houthis say they also hit the Ras Tanura
  refinery.
- **Ukraine war** — overnight strikes kill 3 and injure 15 across Russia
  and Ukraine; Ukrainian drones set two Rosneft refineries ablaze.
- **Israel / Gaza** — Israeli strike kills Hamas security chief Mohammad
  Abuelouf, his wife and two children in Gaza City.
- **United States / technology** — Brooklyn jury convicts Huawei of
  trade-secret theft and bank fraud on 10 of 12 counts.
- **Pacific** — Australia and Solomon Islands sign a treaty precluding
  any foreign military base on the Solomons.
- **Sudan** — RSF drone strikes kill 19 civilians, wound 20.
- **Markets** — S&P 500 −0.5%, Nasdaq −1.5%, Dow +0.9% (first close
  above 50,000), Nikkei −2.8%, KOSPI −6.2%, Brent crude $87.8.
- **In brief** — Shenzhou-24 docks at Tiangong with Pakistan's first
  astronaut aboard; Pope Leo XIV laments the COP31 failure; Colombia
  police free supermarket hostages; Dell reports a record quarter on
  AI servers.

Sources: Just Security's Early Edition (25 Nov 2026), SCMP world page,
Yeni Safak, NordFX market pulse, Reuters markets, Open Chronicle's
25 Nov 2026 brief.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` outside the
grader). The poster itself is drawn offline by
`tools/render_poster.py` (Python + Pillow) and committed as
`entry.png`, so the graded program needs no network and always writes
identical bytes.

## License

MIT — see `LICENSE`.
