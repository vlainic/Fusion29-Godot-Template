# Progress

## What Works

- Godot 4.6 project opens and runs from `res://scenes/opening/opening.tscn`.
- Full Maaack-style menu flow: opening → main menu → options → credits → game scene.
- Pause menu, level-won and level-lost windows, scrolling end credits.
- Scene loading with transitions via `SceneLoader` autoload.
- Audio bus / UI sound scaffolding via `ProjectMusicController` and `ProjectUISoundController`.
- Persisted user preferences via `UserSettings` autoload.
- Debug shortcuts (restart, pause, quit, speed up, step frame) via `GGT_DebugShortcuts`.
- Input map covers UI, movement, `interact`, and debug actions.
- Localization wiring for English and French via Maaack translation resources.

## What's Left to Build (Template-Level)

- Decide and adopt a testing approach (plain test scenes or GdUnit4/GUT) and scaffold `res://tests/`.
- Decide what to do with backend-flavored Cursor skills and agents that were carried over (see `active_context.md`).
- Optionally add a minimal CI workflow (headless export or lint) once testing is chosen.
- Optional: refresh README with current stack and the `.cursor/` tooling map.

## Current Status

- **Stage:** template reusable for new games; Cursor tooling being realigned with the Godot stack.
- **Stability:** stable for prototyping; no known regressions from upstream Maaack base.
- **Documentation:** Memory Bank initialized (this commit); rules and agents updated to Godot.

## Known Issues / Watchlist

- Backend-era skills (`project-conventions`, `stat-domain`) and agents (`api-doc-generator`, `django-boilerplate`, `migration-verifier`) do **not** apply to this repo; agents that load them should be treated as off-scope until they are rewritten or removed.
- No automated tests yet — regressions must be caught manually by running the template.
- Upstream Maaack template updates should be reviewed before pulling, because local tweaks may live under `scenes/` and `scripts/` and can drift.
