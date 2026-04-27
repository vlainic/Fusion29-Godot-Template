# Tech Context

## Engine & Language

- **Godot 4.x**, currently targeting **4.6** (`project.godot` → `config/features=PackedStringArray("4.6")`).
- **GDScript 2** is the primary language. No C# / GDExtension in this repo today.

## Application Entry

- Main scene: `res://scenes/opening/opening.tscn` (`run/main_scene` in `project.godot`).
- Display: `1920 x 1080` viewport (`[display]`).
- Renderer: `gl_compatibility` on desktop and mobile (`[rendering]`).

## Enabled Plugins (`[editor_plugins]`)

- `res://scenes/runtime_template/plugin.cfg` — Maaack’s Godot Game Template (menus, options, loaders, helpers).
- `res://addons/ggt-core/plugin.cfg` — GGT core utilities (scenes history, transitions, progress, multithread loader).
- `res://addons/ggt-debug-shortcuts/plugin.cfg` — debug shortcuts (restart, pause, quit, speedup, step frame).

## Autoloads (`[autoload]`)

- `AppConfig` — `addons/maaacks_game_template/base/nodes/autoloads/app_config/app_config.tscn`
- `SceneLoader` — `addons/maaacks_game_template/base/nodes/autoloads/scene_loader/scene_loader.tscn`
- `ProjectMusicController` — Maaack music controller autoload.
- `ProjectUISoundController` — Maaack UI sound controller autoload.
- `GGT` — `addons/ggt-core/ggt.gd`.
- `GGT_DebugShortcuts` — `addons/ggt-debug-shortcuts/autoload/debug_shortcuts.tscn`.
- `UserSettings` — project-owned autoload at `res://scripts/autoloads/user_settings.gd`.

## Repository Layout

- `addons/` — upstream plugins; treat as external code.
- `scenes/` — project-specific scenes (opening, menus, game scene, credits, windows, loading screen).
- `scripts/` — project-specific GDScript (game state, level state/loader, autoloads, utils).
- `resources/` — project resources.
- `assets/` — art / audio / icons.
- `.cursor/` — rules, agents, skills, memory (this folder).

Folder colors are configured in `project.godot` (`[file_customization]`) to visually separate these areas in the editor.

## Input Actions

Defined in `project.godot` (`[input]`):

- UI: `ui_accept`, `ui_cancel`, `ui_page_up`, `ui_page_down`.
- Movement: `move_up`, `move_down`, `move_left`, `move_right`.
- Gameplay: `interact`.
- Debug (GGT): `ggt_debug_restart_scene`, `ggt_debug_pause_game`, `ggt_debug_quit_game`, `ggt_debug_speedup_game`, `ggt_debug_step_frame`.

## Internationalization

- English and French translations bundled from Maaack’s template:
  - `addons/maaacks_game_template/base/translations/menus_translations.en.translation`
  - `addons/maaacks_game_template/base/translations/menus_translations.fr.translation`

## Maaack Template Settings

Configured in `[maaacks_game_template]`:

- `copy_path="res://"`
- `disable_install_wizard=true`
- `disable_install_audio_busses=true`
- `disable_update_check=false`

## Build / Run

- Open in Godot 4.6 and press F5 (main scene runs `opening.tscn`).
- No Python/Node toolchain; no CI configuration assumed in this repo at the moment.

## Testing

- No bundled unit-test addon yet.
- Recommended path (see `.cursor/agents/test-writer.md`):
  - Lightweight test scenes/scripts under `res://tests/`.
  - Optionally adopt **GdUnit4** or **GUT** later and follow that addon’s layout.

## Dependencies / Constraints

- Stay compatible with Maaack’s template so upstream updates can be integrated.
- Keep modifications localized to `scenes/` and `scripts/` when possible.
- Respect addon licenses; this project is MIT-licensed via upstream (`LICENSE.txt`).
