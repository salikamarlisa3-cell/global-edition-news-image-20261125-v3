// Entry for news-image-20261125: "The World in One Day — 25 Nov 2026".
//
// A single 1024x1024 front page for Wednesday 25 November 2026: the
// Dow closing above 50,000 for the first time, two tankers mined in
// Hormuz, Libya's vow after the drone strike on a Russian warship,
// the oldest quasar ever seen — 56 verified stories in 7 regions, all
// cited in SOURCES.md. The artwork lives in poster.svg (produced by
// build_poster.py) and was rendered to entry.png by generate.mjs.
//
// Delivery is this program's only job: copy entry.png, byte for byte,
// into the grader's output directory ($MAKEFUN_OUTPUT_DIR, falling
// back to /output), then read it back and check the size matches.

import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));
const page = readFileSync(join(here, 'entry.png'));
const target = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
writeFileSync(target, page);

const landed = readFileSync(target);
if (landed.length !== page.length) {
  throw new Error(
    `entry.png copy is ${landed.length} bytes, expected ${page.length}`);
}
