/**
 * Registry control tests — prevent accidental production_ready / integration flags.
 * Run: node --test tests/swi-module-registry.test.mjs
 *   or: vitest run tests/swi-module-registry.test.mjs (if vitest resolves .mjs)
 */
import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const registryPath = resolve(root, "config/swi-module-registry.json");

describe("swi-module-registry", () => {
  const raw = readFileSync(registryPath, "utf8");
  const data = JSON.parse(raw);

  it("has stable sha256 over file bytes", () => {
    const h = createHash("sha256").update(raw).digest("hex");
    assert.equal(h.length, 64);
  });

  it("includes M01–M15", () => {
    const ids = new Set(data.modules.map((m) => m.id));
    for (let i = 1; i <= 15; i++) {
      const id = `M${String(i).padStart(2, "0")}`;
      assert.ok(ids.has(id), `missing ${id}`);
    }
  });

  it("M11 and M12 remain non-integrated and not production_ready", () => {
    const m11 = data.modules.find((m) => m.id === "M11");
    const m12 = data.modules.find((m) => m.id === "M12");
    assert.equal(m11.state, "SEALED");
    assert.equal(m11.integration_enabled, false);
    assert.equal(m11.production_ready, false);
    assert.equal(m12.state, "SEALED");
    assert.equal(m12.integration_enabled, false);
    assert.equal(m12.production_ready, false);
  });

  it("no module claims production_ready under current registry", () => {
    for (const m of data.modules) {
      assert.equal(m.production_ready, false, m.id);
    }
  });

  it("verify script exits 0 on current registry", () => {
    const r = spawnSync(
      process.execPath,
      [resolve(root, "scripts/swi-verify-module.mjs")],
      { encoding: "utf8" }
    );
    assert.equal(r.status, 0, r.stderr + r.stdout);
    assert.match(r.stdout, /RESULT: PASS/);
  });
});
