// Entry program for make.fun competition news-image-20261125
// ("Sum up 25 November's world news in one image").
//
// The poster beside this file, entry.png, is a one-page newspaper front
// page drawn by tools/render_poster.py from the world news reported on
// Wednesday 25 November 2026. This program's whole job is to place that
// image where the grader reads it: /output/entry.png. Outside the
// grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only, no network. The copy is byte-exact,
// so repeated runs always write identical bytes.

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });

const target = join(outDir, 'entry.png');
copyFileSync(source, target);

// Fail loudly rather than hand the grader a truncated image: the copy
// must land with exactly the source's byte count.
const written = statSync(target).size;
const expected = statSync(source).size;
if (written !== expected) {
  throw new Error(`entry.png copy incomplete: wrote ${written} of ${expected} bytes`);
}
console.log(`entry.png written: ${written} bytes`);
