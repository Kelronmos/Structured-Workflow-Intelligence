#!/usr/bin/env node
/**
 * SWI module registry gate (real control, not documentation theatre).
 *
 * Usage:
 *   node scripts/swi-verify-module.mjs
 *   node scripts/swi-verify-module.mjs M11
 *
 * Exit 0 only if registry is consistent and requested modules are allowed
 * under dependency/seal rules. Never marks production_ready by itself.
 */
import { createHash } from "node:crypto";
import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");
const registryPath = resolve(root, "config/swi-module-registry.json");

const TRUSTED = new Set(["INTEGRATION_READY", "SYSTEM_VERIFIED", "RELEASED"]);

function loadRegistry() {
  if (!existsSync(registryPath)) {
    console.error("FAIL: missing", registryPath);
    process.exit(2);
  }
  const raw = readFileSync(registryPath, "utf8");
  const hash = createHash("sha256").update(raw).digest("hex");
  const data = JSON.parse(raw);
  return { data, hash, raw };
}

function assertRegistryInvariants(data) {
  const errors = [];
  if (!data.modules || !Array.isArray(data.modules)) {
    errors.push("modules array required");
    return errors;
  }
  const byId = new Map();
  for (const m of data.modules) {
    if (!m.id) errors.push("module missing id");
    if (byId.has(m.id)) errors.push(`duplicate id ${m.id}`);
    byId.set(m.id, m);

    if (m.production_ready === true) {
      const v = m.verification || {};
      const ok =
        v.unit &&
        v.negative &&
        v.security &&
        (m.state === "INTEGRATION_READY" ||
          m.state === "SYSTEM_VERIFIED" ||
          m.state === "RELEASED");
      if (!ok) {
        errors.push(
          `${m.id}: production_ready=true forbidden without unit+negative+security and trusted state`
        );
      }
    }

    if (m.integration_enabled === true && !TRUSTED.has(m.state)) {
      errors.push(
        `${m.id}: integration_enabled requires state in ${[...TRUSTED].join(",")}`
      );
    }

    if (m.state === "SEALED" && m.integration_enabled === true) {
      errors.push(`${m.id}: SEALED cannot have integration_enabled=true`);
    }
  }

  // Dependency gating: deps must exist; if integration_enabled, deps must be trusted
  for (const m of data.modules) {
    const deps = m.dependencies || [];
    for (const d of deps) {
      if (!byId.has(d)) errors.push(`${m.id}: missing dependency ${d}`);
      else if (m.integration_enabled) {
        const dep = byId.get(d);
        if (!TRUSTED.has(dep.state)) {
          errors.push(
            `${m.id}: cannot integrate while dependency ${d} state=${dep.state}`
          );
        }
      }
    }
  }

  return errors;
}

function printModule(m) {
  console.log(
    `  ${m.id}  state=${m.state}  seal=${m.seal_level}  class=${m.classification}  prod=${m.production_ready}  integ=${m.integration_enabled}`
  );
}

const { data, hash } = loadRegistry();
console.log("SWI MODULE REGISTRY VERIFICATION");
console.log("registry_sha256:", hash);

const errors = assertRegistryInvariants(data);
if (errors.length) {
  console.error("RESULT: FAILED");
  for (const e of errors) console.error(" -", e);
  process.exit(1);
}

const filter = process.argv[2];
const modules = filter
  ? data.modules.filter((m) => m.id === filter)
  : data.modules;

if (filter && modules.length === 0) {
  console.error("FAIL: unknown module", filter);
  process.exit(1);
}

for (const m of modules) printModule(m);

const sealed = data.modules.filter((m) => m.state === "SEALED");
console.log("sealed_count:", sealed.length);
console.log("RESULT: PASS (registry consistent; no production promotion)");
process.exit(0);
