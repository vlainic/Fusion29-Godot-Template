---
name: project-conventions
description: Core conventions for the NSMK Django/DRF backend — app layout, service layer, serializers, URLs, and testing. Load this before generating or refactoring backend code.
---

# Project Conventions (NSMK Backend)

## App Structure

- Current primary apps:
  - `core` — core entities such as clubs, players, teams, venues.
  - `competitions` — seasons, leagues, rounds, playoff brackets.
  - `games` — games, player game stats, play-by-play.
  - `player_base` — internal player records, profiles, season summaries.
  - `api` — DRF serializers, viewsets, and API URL routing.
- Business logic should live in `services.py` (or a `services/` package) inside each domain app, not in views or serializers.
- Views are thin:
  - Validate input.
  - Call service functions.
  - Return DRF `Response` objects.

## Models

- Always define:
  - `__str__` for human-readable representation.
  - `class Meta` with:
    - `ordering` (default sort for lists).
    - Any composite indexes in `indexes` list.
- Use timestamps when appropriate:
  - `created_at = models.DateTimeField(auto_now_add=True)`
  - `updated_at = models.DateTimeField(auto_now=True)`
- Indexes:
  - All `ForeignKey` fields should be indexed (either via `db_index=True` or explicit `Meta.indexes`).
  - Any field used commonly in `.filter()` or `.order_by()` (e.g. `status`, `scheduled_date`, `league`, `season`) should be indexed.
- Keep domain rules (like standings, stats aggregation, or state transitions) in services instead of model methods when the logic is non-trivial.

## Serializers

- Use `ModelSerializer` with an explicit `fields` list — never use `fields = "__all__"`.
- For read operations:
  - It is acceptable to use nested serializers to expose related objects (e.g. a game with embedded team info).
- For write operations:
  - Prefer simple FK ID fields (`team_id`, `league_id`, etc.) instead of nested writable objects.
  - Put validation logic in `validate_<field>` or `validate()` methods on the serializer.
- Do not perform heavy business logic or side effects inside serializers; delegate to services.

## ViewSets & Permissions

- Default to `ModelViewSet` for resources that support CRUD; use `ReadOnlyModelViewSet` when appropriate.
- Always set `permission_classes` explicitly:
  - Public read-only endpoints (tables, schedules, basic stats) should use permissive read perms.
  - Admin-only or internal management endpoints (e.g. editing games, stats, internal player base) should enforce stricter permissions.
- Use `filter_backends` and `filterset_fields` via `django-filter` for structured filtering.
- Consider `search_fields` and `ordering_fields` where helpful for API consumers.
- Custom actions:
  - Use DRF `@action` on viewsets for resource-specific operations (e.g. `/leagues/{id}/standings/`, `/games/{id}/stats/`).

## URL Naming & API Prefix

- API is exposed under an `/api/` prefix (or `/api/v1/` if versioning is enabled).
- Use DRF `DefaultRouter` in `api/urls.py` to register viewsets.
- Router-generated names follow:
  - `<resource>-list`
  - `<resource>-detail`
- Custom action route names:
  - `<resource>-<action>` (for example, `league-standings`, `league-leaders`, `game-stats`).

## Response Format

- For list endpoints:
  - Use DRF pagination defaults: `{ "count": N, "next": ..., "previous": ..., "results": [...] }` when pagination is enabled.
- For detail endpoints:
  - Return a single flat JSON object representing the resource.
- For validation errors:
  - Return DRF-style errors, typically `{ "field": ["message"] }`.
- For other errors:
  - Use `{ "detail": "message" }` (e.g. 404, 403, etc.).

## Testing

- Use `pytest` and `pytest-django` with `@pytest.mark.django_db` for tests hitting the database.
- Use `model_bakery.baker` for creating model instances; never rely on hardcoded primary keys.
- Test file placement:
  - Domain app logic: `<app>/tests/test_<resource>.py`.
  - API-specific behavior (if split out): `api/tests/test_<resource>_endpoints.py`.
- For each feature:
  - Cover happy paths.
  - Cover validation failures.
  - Cover permission behavior.
  - Include edge cases that reflect NSMK domain rules (e.g. game state transitions, standings tie-breakers).

Load this skill before generating or refactoring backend code so that all agents and tools follow the same conventions.

