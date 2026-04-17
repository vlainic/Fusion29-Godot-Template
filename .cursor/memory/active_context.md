# Active Context

## Current Focus

Cursor tooling for this repo: rules, agents, and the Memory Bank are being aligned with the **Fusion29 Godot Template** (Godot 4.6), away from the prior NSMK Django/DRF wording inherited from earlier configs.

## Recent Changes

- **Agents** (`.cursor/agents/`):
  - Added `godot-engine.md` — Godot 4.x implementation specialist (scenes, GDScript 2, autoloads, addon boundaries).
  - Added `game-designer.md` — design partner for mechanics, pacing, onboarding, and engineering handoff.
  - Rewrote `test-writer.md` for Godot (test scenes / `SceneTree` / `await` / signals, optional GdUnit4 or GUT).
  - Backend-only agents (`api-doc-generator`, `django-boilerplate`, `migration-verifier`) remain untouched; they do not apply to this repo and may be removed or replaced later.
- **Rules** (`.cursor/rules/`):
  - Updated `my-stack.mdc` to describe the Godot 4.6 stack, addons, autoloads, and testing posture.
  - `coding-preferences.mdc` and `workflow-preferences.mdc` unchanged (still generic / useful).
- **Memory Bank** (`.cursor/memory/`):
  - Initial set created: `project_brief.md`, `product_context.md`, `tech_context.md`, `system_patterns.md`, `active_context.md`, `progress.md`.

## Active Decisions

- **Addon boundary:** keep modifications in `scenes/` and `scripts/`; treat `addons/` as upstream.
- **Navigation:** route scene changes through `SceneLoader`.
- **Settings:** `AppConfig` for app-level, `UserSettings` for user-facing preferences.
- **Debug:** prefer `GGT_DebugShortcuts` bindings over ad-hoc debug keys.

## Open Questions / Considerations

- **Testing framework:** adopt **GdUnit4**, **GUT**, or stay with plain test scenes under `res://tests/`? (Agent is written to accommodate either.)
- **Backend-flavored skills** — `project-conventions` and `stat-domain` in `.cursor/skills/` describe an NSMK Django project that does not apply here. Options:
  1. Remove them from this repo.
  2. Rewrite them as Godot-focused skills (e.g. `godot-project-conventions`).
  3. Keep as-is only if another repo under the same Cursor workspace uses them.
- **Backend agents** — same call applies to `api-doc-generator`, `django-boilerplate`, `migration-verifier`.
- **CI** — no automation configured yet; decide whether to add headless-Godot exports or lint passes later.

## Next Steps (Proposed)

1. Decide fate of backend skills/agents (remove / rewrite / keep).
2. Pick a testing addon or commit to plain test-scene convention; add a `res://tests/` scaffold when decided.
3. Capture any new patterns in `system_patterns.md` as they emerge.
