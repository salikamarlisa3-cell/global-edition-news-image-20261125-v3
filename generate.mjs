// generate.mjs — full local build for this entry: first build_poster.py
// writes poster.svg (not committed; it is a build artifact), then the
// cached Chromium headless shell renders that SVG to entry.png at
// exactly 1024x1024. The competition program (main.ts) does none of
// this — it only delivers entry.png.
//
//   node generate.mjs

import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, renameSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));

execFileSync('python3', [join(here, 'build_poster.py')],
             { cwd: here, stdio: 'inherit' });

function chromium() {
  const cache = join(homedir(), '.cache', 'ms-playwright');
  for (const name of readdirSync(cache).sort().reverse()) {
    if (!name.startsWith('chromium_headless_shell')) continue;
    const bin = join(cache, name, 'chrome-headless-shell-linux64',
                     'chrome-headless-shell');
    if (existsSync(bin)) return bin;
  }
  throw new Error('no chromium headless shell in ' + cache);
}

const shot = join(here, 'render.png');
execFileSync(chromium(), [
  '--headless', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  '--force-device-scale-factor=1', '--window-size=1024,1024',
  '--default-background-color=00000000',
  '--screenshot=' + shot,
  pathToFileURL(join(here, 'poster.svg')).href,
], { stdio: 'inherit' });
renameSync(shot, join(here, 'entry.png'));
console.log('entry.png rendered');
