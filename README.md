# The World in One Day — Wednesday 25 November 2026

[![News Image — 25 November 2026](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b17-heroalt/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b17-heroalt/reward.svg)](https://make.fun/bounty/news-image-20261125)

One image summing up the world's news of **Wednesday 25 November 2026** — 50 stories
across 10 regions, in a single 1024×640 front page. Variant **HEROALT**: the
lead visual is a drawn Shenzhou-24 scene, with the two other big stories of the
day as hero cards beside it and the remaining 47 stories in a grid below.

## The three heroes

1. **Trump's new tariff salvo** — the US proposes new tariffs on 14 trading
   partners to fight excess factory capacity. China faces 20% (up to 40% if the
   trade truce fails); the EU faces 15%. A public hearing is set for 25 January.
2. **AI chip selloff sinks Asia** — the Kospi falls 6.16% to 4,697.51, Samsung
   −9.87%, SK Hynix −11.05%, as AI shares sell off; Wall Street follows
   (S&P −2.2%, Nasdaq −3.2%).
3. **Shenzhou-24 carries Pakistan's first astronaut to Tiangong** — Muhammad
   Zeeshan Ali becomes the first foreign astronaut aboard China's space
   station, flying with two Chinese crew.

Every card carries its region and a certainty letter: **C** = confirmed,
**R** = reported, **CL** = claim (used where the source is a party's own
assertion, e.g. Iran's Hormuz mine claims). Each hero card also has a
WHY IT MATTERS line and an ALSO line with a second key fact.

## The grid

47 more stories from 25 November 2026, including the Hormuz tanker-mine
claims, the Houthi strike on Saudi Arabia's Ras Tanura refinery, the Riyadh
tower strike, COP31 ending without a deal, the Huawei conviction, Nvidia
reinstating Jensen Huang, the Bogor gold-mine collapse (9 dead, 17 trapped),
the Australia–Solomon Islands treaty, and the Cairo tanker crash.

## How it is built

- `gen.py` renders `entry.png` at build time with Pillow (1024×640, under 1 MiB).
- `main.py` is standard-library only: it copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy byte-for-byte. The
  grader image has no third-party packages, so `main.py` never imports PIL.
- Run locally: `python3 gen.py && MAKEFUN_OUTPUT_DIR=out python3 main.py`.

## License

MIT — see [LICENSE](LICENSE).
