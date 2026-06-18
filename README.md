# Fusion29 Godot Template
For Godot 4.6 (4.3+ compatible)

> [!NOTE]  
> Using the latest version of Godot is recommended.   
> See [Main Menu Setup](/maaacks_game_template/docs/MainMenuSetup.md) for use with versions < 4.6.  

This template has a main menu, options menus, pause menu, credits, scene loader, extra tools, and an example game scene.  

**This is just adjustment for our games from here [Godot Game Template](https://github.com/Maaack/Godot-Game-Template) - thanks Maaack :)**

> [!NOTE]
> Upstream is MIT; see LICENSE.txt

## Quick Start

Use Godot normally (import project, run, edit). This repo assumes Godot basics.

For CI/CD (`.github/workflows/godot-ci.yml`):

| Git branch | Deploy target |
|------------|---------------|
| `prod` | itch.io (Linux, Windows, macOS, HTML5) |
| `app` | Steam App ID (full game) |
| `demo` | Steam App ID (demo) |
| `playtest` | Steam App ID (playtest) |

All branches export the same Godot build. Manual runs via **Actions → Godot CI/CD Pipeline → Run workflow**; set **steam_target** to retry a Steam upload without pushing.

### Shared configuration

- Repository variable: `GODOT_VERSION`

### itch.io (`prod` branch)

Repository secrets:

- `BUTLER_API_KEY`
- `ITCHIO_USERNAME`
- `ITCHIO_GAME`

### Steam (`app`, `demo`, `playtest` branches)

Repository secrets (shared across all Steam apps):

- `STEAM_USERNAME` — dedicated build account recommended
- `STEAM_CONFIG_VDF` — base64-encoded SteamCMD login cache (`cat config/config.vdf | base64`)

Per-app secrets live in GitHub **Environments** (`Settings → Environments`):

| Environment | Triggered by |
|-------------|--------------|
| `steam-app` | push to `app` |
| `steam-demo` | push to `demo` |
| `steam-playtest` | push to `playtest` |

Each environment uses the same secret names (different values per app):

- `STEAM_APP_ID`
- `STEAM_DEPOT_WINDOWS` — Windows depot ID (also used as `firstDepotIdOverride`)
- `STEAM_DEPOT_LINUX` — Linux depot ID (must be `STEAM_DEPOT_WINDOWS + 1`)
- `STEAM_RELEASE_BRANCH` — optional Steam branch (e.g. `default`, `beta`); omit to use action default

Before the first Steam deploy, in [Steamworks Partner](https://partner.steamgames.com/):

1. Register each app and create Windows + Linux depots; note depot IDs.
2. Grant the CI build account upload permissions for all three apps.
3. Run SteamCMD `+login <build_account>` locally once, then encode `config/config.vdf` into `STEAM_CONFIG_VDF`.

CI uploads builds; promote them to live in Steamworks until you trust the pipeline.

## Cursor Notes

This repo ships a **`.cursor/`** folder so Cursor (and similar tools) know how we work. Here’s what each part is for:

| Piece | Location | What it contains |
|-------|-----------|------------------|
| **Agents** | [`.cursor/agents/`](.cursor/agents/) | Ready-made “personas” you can @-mention: **`godot-engine`** (Godot code and scenes), **`game-designer`** (mechanics, pacing, specs), **`test-writer`** (Godot tests: harness scenes, signals, optional GdUnit4/GUT). |
| **Rules** | [`.cursor/rules/`](.cursor/rules/) | Short policies that apply when editing matching files: **`my-stack.mdc`** (Godot stack and addon boundaries), **`coding-preferences.mdc`**, **`workflow-preferences.mdc`**. |
| **Skills** | [`.cursor/skills/`](.cursor/skills/) | Longer playbooks as `SKILL.md` files. **Godot-relevant:** `core-memory-bank`, `core-plan-act`, `thinking-protocol`, `be-brief`. **Legacy / other-domain:** `project-conventions` and `stat-domain` describe a Django/basketball backend—not used for this Godot template unless you copy them to another repo. |
| **Memory bank** | [`.cursor/memory/`](.cursor/memory/) | Markdown “save game” for the project between sessions: **`project_brief`**, **`product_context`**, **`tech_context`**, **`system_patterns`**, **`active_context`**, **`progress`**. Start with `project_brief.md` and `active_context.md` if you’re picking up work cold. |