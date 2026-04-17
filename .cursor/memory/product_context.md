# Product Context

## Why This Project Exists

Setting up a new Godot game from scratch repeatedly produces the same plumbing: menus, settings, scene loaders, pause handling, credits. This template absorbs that work once so each new Fusion29 game can start at “make the game” instead of “wire the menus”.

## Problems It Solves

- Repeated boilerplate for main menu / options / pause / credits flows.
- Inconsistent scene-loading and transition patterns between projects.
- Missing developer ergonomics (debug shortcuts, reset-to-default settings, input remapping) during prototyping.
- Drift from the upstream Maaack template when features are copied ad-hoc per project.

## How It Should Work

- Cloning this repo yields a runnable Godot 4.x project with:
  - A polished opening → main menu → game scene flow.
  - Working options, input remapping, audio buses, and user settings persistence.
  - Pause menu, level-won / level-lost windows, scrolling credits.
- Game developers add new gameplay under `scenes/` and `scripts/`.
- Addon folders (`addons/maaacks_game_template/`, `addons/ggt-core/`, `addons/ggt-debug-shortcuts/`) are treated as upstream code and kept mostly untouched.

## User Experience Goals

- **First-run feel:** the template itself should play like a tiny complete product — no broken buttons, dead scenes, or debug stubs on the main path.
- **Developer UX:** adding a new scene, autoload, or option should be obvious by example.
- **Upgradeability:** pulling newer Maaack template versions should be low-friction.
