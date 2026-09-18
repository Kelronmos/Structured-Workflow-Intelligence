#!/usr/bin/env node
/**
 * SWI CI gate — system-state honesty + registry consistency.
 * Does not invent production readiness or promote modules.
 *
 * Usage: node scripts/swi-ci-check.mjs
 */
import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");

function fail(msg) {
  console.error("SWI CI FAIL:", msg);
  process.exit(1);
}

// 1. System state must remain research / non-production
const statePath = resolve(root, "SWI_SYSTEM_STATE.json");
if (!existsSync(statePath)) fail("missing SWI_SYSTEM_STATE.json");
const state = JSON.parse(readFileSync(statePath, "utf8"));
if (state.status !== "RESEARCH_PROTOTYPE") {
  fail(`status must be RESEARCH_PROTOTYPE, got ${state.status}`);
}
if (state.risk !== "DO_NOT_DEPLOY") {
  fail(`risk must be DO_NOT_DEPLOY, got ${state.risk}`);
}
console.log("system_state: RESEARCH_PROTOTYPE / DO_NOT_DEPLOY");

// 2. Registry gate
const verify = spawnSync(
  process.execPath,
  [resolve(root, "scripts/swi-verify-module.mjs")],
  { encoding: "utf8" }
);
if (verify.status !== 0) {
  console.error(verify.stdout);
  console.error(verify.stderr);
  fail("registry verification failed");
}
console.log("registry: PASS");

// 3. Registry unit tests
const tests = spawnSync(
  process.execPath,
  ["--test", resolve(root, "tests/swi-module-registry.test.mjs")],
  { encoding: "utf8" }
);
if (tests.status !== 0) {
  console.error(tests.stdout);
  console.error(tests.stderr);
  fail("registry tests failed");
}
console.log("registry tests: PASS");

console.log("SWI CI RESULT: PASS (control plane only; no production claim)");
process.exit(0);
