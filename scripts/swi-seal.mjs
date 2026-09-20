#!/usr/bin/env node
/**
 * SWI seal gate.
 *
 * A registry flag is never evidence.
 * SEALED requires seal_record under evidence/ with schema-valid PASS checks.
 * This verifier does not manufacture evidence.
 */

import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const REGISTRY = resolve(ROOT, "config/swi-module-registry.json");
const SCHEMA = resolve(ROOT, "schemas/swi-seal-record.schema.json");
const EVIDENCE_ROOT = resolve(ROOT, "evidence");

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exitCode = 1;
}

function loadJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

if (!existsSync(REGISTRY)) {
  fail("registry missing");
  process.exit(1);
}

if (!existsSync(SCHEMA)) {
  fail("seal schema missing: schemas/swi-seal-record.schema.json");
  process.exit(1);
}

const registryRaw = readFileSync(REGISTRY, "utf8");
const registry = JSON.parse(registryRaw);
const registrySha256 = createHash("sha256").update(registryRaw).digest("hex");

if (!Array.isArray(registry.modules)) {
  fail("registry.modules must be an array");
  process.exit(1);
}

const requestedModule = process.argv[2];
const ids = new Set();
const errors = [];

for (const module of registry.modules) {
  if (!module.id || ids.has(module.id)) {
    errors.push(`invalid/duplicate module id: ${module.id}`);
  }
  ids.add(module.id);

  if (module.state !== "SEALED") continue;

  const sealRecord = module.seal_record;
  if (!sealRecord || typeof sealRecord.path !== "string") {
    errors.push(
      `${module.id}: SEALED requires seal_record.path (registry flag is not evidence)`
    );
    continue;
  }

  const recordPath = resolve(ROOT, sealRecord.path);
  if (!recordPath.startsWith(`${EVIDENCE_ROOT}/`) && !recordPath.startsWith(`${EVIDENCE_ROOT}\\`)) {
    errors.push(`${module.id}: seal record must live under evidence/`);
    continue;
  }

  if (!existsSync(recordPath)) {
    errors.push(`${module.id}: missing seal record ${sealRecord.path}`);
    continue;
  }

  let record;
  try {
    record = loadJson(recordPath);
  } catch {
    errors.push(`${module.id}: invalid JSON in ${sealRecord.path}`);
    continue;
  }

  if (record.schema_version !== "1.0.0") {
    errors.push(`${module.id}: unsupported seal-record schema_version`);
  }
  if (record.module_id !== module.id) {
    errors.push(`${module.id}: seal record module_id mismatch`);
  }
  if (record.status !== "PASS") {
    errors.push(`${module.id}: seal record status must be PASS`);
  }

  for (const check of ["contract", "unit", "negative", "deterministic", "security", "reproducible"]) {
    if (record.checks?.[check] !== true) {
      errors.push(`${module.id}: seal check ${check} is not true`);
    }
  }

  if (!/^[0-9a-f]{7,64}$/.test(record.commit ?? "")) {
    errors.push(`${module.id}: invalid/missing commit`);
  }
  if (!record.run?.id) {
    errors.push(`${module.id}: missing run.id`);
  }
  if (!record.source?.repository) {
    errors.push(`${module.id}: missing source.repository`);
  }
  if (!Array.isArray(record.limitations)) {
    errors.push(`${module.id}: limitations must be an array`);
  }
}

const m12 = registry.modules.find((m) => m.id === "M12");
if (m12?.state === "SEALED") {
  errors.push(
    "M12: cannot be SEALED without an implemented, independently verified module and seal_record"
  );
}

if (errors.length > 0) {
  console.error("SWI SEAL GATE: FAILED");
  console.error(
    "(Expected until SEALED modules carry real evidence under evidence/ — do not invent PASS files.)"
  );
  for (const error of errors) console.error(` - ${error}`);
  console.error(`registry_sha256: ${registrySha256}`);
  process.exit(1);
}

const modules = requestedModule
  ? registry.modules.filter((m) => m.id === requestedModule)
  : registry.modules;

if (requestedModule && modules.length === 0) {
  fail(`unknown module ${requestedModule}`);
  process.exit(1);
}

console.log("SWI SEAL GATE: PASS");
console.log(`registry_sha256: ${registrySha256}`);
for (const module of modules) {
  console.log(`${module.id} state=${module.state} seal_level=${module.seal_level ?? "?"}`);
}
process.exit(0);
