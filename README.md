# Fusion29 Godot Template
For Godot 4.6 (4.3+ compatible)

> [!NOTE]  
> Using the latest version of Godot is recommended.   
> See [Main Menu Setup](/addons/maaacks_game_template/docs/MainMenuSetup.md) for use with versions < 4.6.  

This template has a main menu, options menus, pause menu, credits, scene loader, extra tools, and an example game scene.  

**This is just adjustment for our games from here [Godot Game Template](https://github.com/Maaack/Godot-Game-Template) - thanks Maaack :)**

> [!NOTE]
> Upstream is MIT; see LICENSE.txt

## Quick Start

Use Godot normally (import project, run, edit). This repo assumes Godot basics.

For CI/CD (`.github/workflows/godot-ci.yml`):

- Pipeline runs on pushes to the `prod` branch (or manual `workflow_dispatch`).
- Set repository variable: `GODOT_VERSION`.
- Set repository secrets:
  - `BUTLER_API_KEY`
  - `ITCHIO_USERNAME`
  - `ITCHIO_GAME`

## Cursor Notes

This repo ships a **`.cursor/`** folder so Cursor (and similar tools) know how we work. Here’s what each part is for:

| Piece | Location | What it contains |
|-------|-----------|------------------|
| **Agents** | [`.cursor/agents/`](.cursor/agents/) | Ready-made “personas” you can @-mention: **`godot-engine`** (Godot code and scenes), **`game-designer`** (mechanics, pacing, specs), **`test-writer`** (Godot tests: harness scenes, signals, optional GdUnit4/GUT). |
| **Rules** | [`.cursor/rules/`](.cursor/rules/) | Short policies that apply when editing matching files: **`my-stack.mdc`** (Godot stack and addon boundaries), **`coding-preferences.mdc`**, **`workflow-preferences.mdc`**. |
| **Skills** | [`.cursor/skills/`](.cursor/skills/) | Longer playbooks as `SKILL.md` files. **Godot-relevant:** `core-memory-bank`, `core-plan-act`, `thinking-protocol`, `be-brief`. **Legacy / other-domain:** `project-conventions` and `stat-domain` describe a Django/basketball backend—not used for this Godot template unless you copy them to another repo. |
| **Memory bank** | [`.cursor/memory/`](.cursor/memory/) | Markdown “save game” for the project between sessions: **`project_brief`**, **`product_context`**, **`tech_context`**, **`system_patterns`**, **`active_context`**, **`progress`**. Start with `project_brief.md` and `active_context.md` if you’re picking up work cold. |