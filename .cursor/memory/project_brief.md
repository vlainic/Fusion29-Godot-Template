# Project Brief

## Name

**Fusion29 Godot Template** (repo: `Fusion29-Godot-Template`).

## Purpose

A reusable Godot 4.x starter project used as the base for Fusion29 games and prototypes. Forked from Maaack's [Godot Game Template](https://github.com/Maaack/Godot-Game-Template) under MIT; adjusted for our workflow.

## Core Requirements

- Provide a ready-to-extend project with:
  - Opening / splash flow.
  - Main menu, options menu, pause menu, credits, end credits.
  - Scene loading with transitions.
  - Example game scene and level-win / level-lost windows.
  - Debug shortcuts during development.
- Stay close enough to upstream template so updates can be pulled in with minimal conflicts.
- Make it easy to start a new game by editing `scenes/` and `scripts/` without hacking the template internals.

## Scope

- **In scope:** template-level features, menus, scene flow, user settings, credit/license plumbing, developer tooling.
- **Out of scope:** shipping game logic, specific game mechanics, game-specific assets.

## Source of Truth

- `project.godot` for engine version, autoloads, enabled plugins.
- `README.md` for intent and upstream attribution.
- This memory bank for cross-session context.
