---
name: stat-domain
description: Basketball stat and game-flow domain knowledge for the NSMK project (and future ORL/LZR extensions). Load when working on stats, standings, play-by-play, or league-specific logic.
---

# Basketball Stat Domain (NSMK-Focused)

## Game State Machine

For NSMK leagues, each game moves through a simple but important state machine:

```
SCHEDULED → IN_PROGRESS → FINISHED → VERIFIED
                              ↑
                         (correction possible before VERIFIED)
```

- **SCHEDULED**
  - Game has a date/time, venue, and teams set.
  - No official stats are recorded yet.
- **IN_PROGRESS**
  - Game is currently being played.
  - Live stats and play-by-play can be captured.
- **FINISHED**
  - Final score and stats have been entered, but not yet locked.
  - Corrections are allowed, but should be tracked.
- **VERIFIED**
  - Final, authoritative record.
  - Only admins can move a game to VERIFIED.
  - Stats should not be editable after this state.

Rules:

- Only authorized league admins can change a game’s state.
- Transition from FINISHED back to IN_PROGRESS or SCHEDULED should be rare and, if allowed, logged with a reason.

## Stat Levels by League

NSMK is the primary focus; ORL and LZR can be added later with more detailed requirements.

| Stat                                | NSMK | ORL | LZR NS |
|-------------------------------------|------|-----|--------|
| Shot attempts (2pt, 3pt, FT)       | ✓    | TBD | ✓      |
| Points scored                      | ✓    | TBD | ✓      |
| Fouls                              | ✓    | TBD | ✓      |
| Minutes played                     | ✗    | TBD | ✓      |
| Full box score (reb, ast, stl, blk, to) | ✗ | TBD | ✓  |
| Play-by-play                       | ✓    | TBD | ✓      |

- For NSMK:
  - Must reliably capture points, shot attempts, and fouls.
  - Play-by-play is supported and should be the source of truth for reconstructing scoring and fouls when needed.
- For ORL and LZR:
  - Treat requirements as flexible until explicitly defined.

## Play-by-Play Event Types

Core event types that should be represented in models/services:

- Shooting:
  - `2PT_MADE`, `2PT_MISSED`
  - `3PT_MADE`, `3PT_MISSED`
  - `FT_MADE`, `FT_MISSED`
- Fouls:
  - `FOUL` (with fouler and optionally fouled player; can be extended into more detailed foul types if needed).
- Timeouts and substitutions:
  - `TIMEOUT`
  - `SUBSTITUTION` (with `player_in` and `player_out`)
- Period markers:
  - `PERIOD_START`, `PERIOD_END`

Mappings:

- Events should be consistent with:
  - `PlayByPlay` model fields (game, quarter/period, time remaining, event type, player/team, and score snapshot).
  - `PlayerGameStats` aggregations (points, shot attempts/makes, fouls, etc.).
  - Services that compute standings, leaders, and derived stats.

## League and Competition Structure

- **NSMK**
  - Youth basketball organization centered around Novi Sad.
  - Multiple age groups (e.g. U12–U15) with separate leagues per season.
  - Needs:
    - Standings tables with points, wins, losses, point differentials.
    - Schedules and results per league and location.
    - Basic scoring stats and leaders.
    - Play-by-play for richer game detail.

- **ORL** (future)
  - Separate organization with similar core structure.
  - Stat requirements may differ (currently “TBD”).

- **LZR NS (Ligazarekreativce Novi Sad)** (future)
  - Recreational league with:
    - Full stats (rebounds, assists, steals, blocks, turnovers, etc.).
    - Full scheduler support, possibly more complex competition formats.

## Competition Formats

Common formats to support across leagues:

- **Leagues**
  - Round-robin, typically “each plays each” with configurable number of rounds.
  - Standings based on league points (win/loss rules) and tie-breakers (point differential, head-to-head, etc.).
- **Knockout**
  - Single- or double-elimination brackets.
- **Combined**
  - Group stage → knockout phase.
  - For LZR NS and similar, schedulers must understand both group and bracket phases.

When implementing or modifying scheduling, standings, or stats-related services, load this skill to stay consistent with the domain expectations.

