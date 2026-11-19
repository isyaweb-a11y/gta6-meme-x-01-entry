# gta6-meme-x-01-entry

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/isyaweb-a11y/gta6-meme-x-01-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/isyaweb-a11y/gta6-meme-x-01-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

**"In line since 2013"** — a GTA VI launch-week meme: the fans in the midnight queue outside the game store have visibly aged (cap kid → adult → grey hair → grandpa with a cane), while the make.fun ghost waits next in line, star coin in hand — because its AI agent spent the 13 years getting paid in make.fun bounties. The ghost is make.fun's official mascot from its [press kit](https://make.fun/press/), worked into the scene; everything else was drawn for this meme by `build_meme.py` (Python/PIL), no Rockstar artwork or fonts.

The entry itself is a post on X: `meme.png` posted with the caption in `caption.txt` (it tags @makefunai, links the bounty and carries the entrant's play code). `POST.json` names the post's address — it currently holds the starter placeholder and is replaced with the real post URL as soon as the post is live, before submission. `main.ts` copies `POST.json` to `/output/POST.json`, which is all the grader's program has to do.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=sc1d8ke0&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
