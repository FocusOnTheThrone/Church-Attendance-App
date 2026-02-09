<!-- Purpose: short, focused instructions for GitHub Copilot / AI coding agents working locally -->
# Copilot / AI Agent Instructions

This repository is a Django (6.x) monolith with small apps. Use these notes to make fast, correct changes.

- Project layout: top-level Django project is in `config/`; apps are `accounts`, `attendance`, `followup`, `reports`, `messaging`.
- Entry points: use `manage.py` for commands; main settings are in `config/settings.py` (see INSTALLED_APPS and `AUTH_USER_MODEL`).

- Runtime & deps: see `requirements.txt` (Django 6, djangorestframework, psycopg2-binary, python-dotenv). Default local DB is SQLite (`db.sqlite3`), but `psycopg2-binary` indicates Postgres is expected for production.

- Common local workflow (PowerShell on Windows):
  - Create env and install: `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1` then `pip install -r requirements.txt`
  - Run migrations: `python manage.py migrate`
  - Run dev server: `python manage.py runserver`
  - Run tests: `python manage.py test`

- App conventions to follow:
  - Each app is a simple Django app with `models.py`, `views.py`, `serializers.py` (where applicable), `admin.py`, and `tests.py`.
  - Templates are under top-level `templates/` and app templates (e.g. `reports/templates/reports/`). Use `TEMPLATES["DIRS"]` in `config/settings.py` when adding template dirs.
  - REST API uses Django REST Framework (DRF). Default permissions (`IsAuthenticated`) and `SessionAuthentication` are set in `config/settings.py` (see `REST_FRAMEWORK`).

- Notable code patterns (concrete examples):
  - Model serializers are `ModelSerializer` with `read_only_fields` and custom `validate()` methods (see `attendance/serializers.py` — it prevents duplicate Attendance records).
  - Custom user model: `AUTH_USER_MODEL = 'accounts.User'` — always use `get_user_model()` when importing the user model.
  - Tests live in each app's `tests.py` file (not a `tests/` package). Run `python manage.py test <app>` to target specific app tests.

- Editing & migration guidance:
  - After model changes: `python manage.py makemigrations <app>` then `python manage.py migrate`.
  - Commit migrations with the change and ensure tests still pass.

- API & auth considerations for changes:
  - DRF default permissions are strict — API endpoints require an authenticated session. For automated tests use `APIClient.force_authenticate()` or create test users and login.

- Integration points to check when making changes:
  - `messaging` and `followup` interact with attendance-related models for notifications — inspect `followup/serializers.py` and `messaging/views.py` when changing attendance logic.
  - `reports` renders templates and uses querysets — review `reports/views.py` and `reports/serializers.py` for performance-sensitive code.

- When in doubt:
  - Run the dev server and exercise the UI pages under `templates/` (e.g., `events.html`, `record_attendance.html`) to confirm behavior.
  - Check `config/settings.py` for environment-specific toggles. Production DB and secrets are not in repo.

If you'd like, I can refine any section or merge this with an existing `.github/copilot-instructions.md` if you already have one elsewhere.
