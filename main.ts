// Entrypoint for the gta6-meme-x-01 entry.
//
// The entry itself is a post on X; this program's whole job is to hand the
// post's address to the grader. It reads POST.json from the repository root,
// checks that the file really names an X post before anything is copied, and
// then writes those exact bytes to POST.json in the output directory, reading
// the copy back to prove the two files agree byte for byte.
//
// Locations come from the harness: MAKEFUN_BOT_DIR is the repository root
// (default /bot) and MAKEFUN_OUTPUT_DIR is where the gate reads its files
// (default /output). A malformed POST.json is reported on stderr and exits 1
// without touching the output directory, so a bad hand-in fails loudly here
// instead of quietly at the gate.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

// The gate accepts a POST.json of at most 16 KiB, so a larger file can never
// be a valid hand-in; refuse it here with a clearer message.
const MAX_POST_BYTES = 16384;

// An X post address: https://x.com/<handle>/status/<id>, or the same on
// twitter.com, with an optional www. or mobile. host prefix and an optional
// query or fragment after the id (the house reads past both). The id is
// digits only and the handle is the usual 1-15 word characters. X also
// serves every post under /i/web/status/<id> with no handle in the path;
// the house reads that form too, so it is accepted here. Whichever form
// matched, one of the two capture groups holds the status id.
const POST_URL_PATTERN =
  /^https:\/\/(?:www\.|mobile\.)?(?:x\.com|twitter\.com)\/(?:[A-Za-z0-9_]{1,15}\/status\/(\d+)|i\/web\/status\/(\d+))(?:[?#]\S*)?$/;

class PostFileProblem extends Error {}

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function describe(err: unknown): string {
  return err instanceof Error ? err.message : String(err);
}

// Reads POST.json and returns its raw bytes, plus the status id its url
// names, once the file is known to hold a JSON object whose "url" is the
// address of one X post. The bytes, not the parsed value, are what get
// copied: the gate compares files, so the copy must carry the original
// formatting untouched.
function readCheckedPostBytes(path: string): { bytes: Buffer; statusId: string } {
  let bytes: Buffer;
  try {
    bytes = readFileSync(path);
  } catch (err) {
    fail(`cannot read POST.json at ${path}: ${describe(err)}`);
  }
  if (bytes.length > MAX_POST_BYTES) {
    fail(`POST.json is ${bytes.length} bytes; the gate allows at most ${MAX_POST_BYTES}`);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(bytes.toString('utf8'));
  } catch (err) {
    fail(`POST.json is not valid JSON: ${describe(err)}`);
  }
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    fail('POST.json must be a JSON object of the form {"url": "https://x.com/<handle>/status/<id>"}');
  }

  const url = (parsed as { url?: unknown }).url;
  if (typeof url !== 'string' || url.length === 0) {
    fail('POST.json has no "url" string naming the post');
  }
  const match = POST_URL_PATTERN.exec(url);
  if (match === null) {
    fail(`POST.json url is not an X post address: ${JSON.stringify(url)}`);
  }
  return { bytes, statusId: match[1] ?? match[2] };
}

function main(): void {
  const botDir = resolve(process.env.MAKEFUN_BOT_DIR ?? '/bot');
  const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');
  const sourcePath = join(botDir, 'POST.json');
  const targetPath = join(outputDir, 'POST.json');

  const { bytes, statusId } = readCheckedPostBytes(sourcePath);

  try {
    mkdirSync(outputDir, { recursive: true });
    writeFileSync(targetPath, bytes);
  } catch (err) {
    fail(`cannot write POST.json to ${targetPath}: ${describe(err)}`);
  }

  // Read the copy back and compare it with the bytes that were checked: the
  // hand-in only counts if what landed in the output is exactly what was
  // validated, so a short or altered write is a failure, not a quiet pass.
  let written: Buffer;
  try {
    written = readFileSync(targetPath);
  } catch (err) {
    fail(`cannot read back ${targetPath} to verify the copy: ${describe(err)}`);
  }
  if (!written.equals(bytes)) {
    fail(`copy verification failed: ${targetPath} differs from ${sourcePath}`);
  }

  console.log(
    `POST.json copied to ${targetPath} (${bytes.length} bytes, verified identical); it names X post ${statusId}`,
  );
}

try {
  main();
} catch (err) {
  if (err instanceof PostFileProblem) {
    fail(err.message);
  }
  throw err;
}
