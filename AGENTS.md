# Developer & Agent Guide

This document contains critical information about the architecture, quirks, and troubleshooting procedures for **EDRefCard**. Read this before attempting major refactors or debugging production issues.

## 🏗️ Architecture & Deployment

### Docker Split
The project uses two separate compose files:
*   **`docker-compose.yml`**: For **local development**. Runs with standard user permissions.
*   **`docker-compose.prod.yml`**: For **production**.
    *   **User**: Runs as `root` (`user: root`) to ensure write permissions on the mounted `configs` volume.
    *   **Env Vars**: Explicitly passes `EDREFCARD_ADMIN_USER`, `EDREFCARD_ADMIN_PASS`, and `APP_URL`.

### File Storage Structure
Configuration files are stored in `www/configs/` using a **hashed directory structure** to avoid filesystem limits:
*   Path format: `www/configs/{xx}/{xxxxxx}.{ext}` (where `xx` are the first 2 chars of the run ID).
*   **Example**: ID `unkbsa` is stored in `www/configs/un/unkbsa.binds`.

### 🗄️ Database & Persistence
*   **Engine**: SQLite.
*   **Location**: `www/configs/edrefcard.db`.
    *   *Critical*: The DB is located in `configs/` (mounted volume) and NOT `data/` or root. If moved to a non-mounted path, all data/stats will reset on container rebuild.
*   **Migration**: 
    *   Legacy data consists of `.replay` (Pickle) files.
    *   The `/admin/migrate` endpoint scans `www/configs` for all `.replay` files and populates the SQLite DB.
    *   This is an idempotent operation (safe to run multiple times).

### 🧩 Application Structure (Refactoring v2.1)
*   **Blueprints**: The application has been refactored to use Flask Blueprints:
    *   `www/web.py`: Main user-facing routes (index, list, view, generate).
    *   `www/api.py`: Public JSON API (`/api/v1`).
    *   `www/admin/__init__.py`: Admin interface.
*   **Entry Point**: `www/app.py` initializes the app, registers blueprints, and handles configuration.
*   **Extensions**: Shared extensions (like `Limiter`) are in `www/extensions.py`.

## ⚠️ Known Quirks & Issues

### 1. "Configuration not found" vs "Source missing"
*   **Scenario**: A user accesses a configuration URL (`/binds/ckjcrn`).
*   **Cause**:
    *   If **.binds** file is missing but **.replay** exists: App enters **Archived Mode**. It displays cached images if found, or a "Source missing" warning. Regeneration is disabled. (Logic in `app.py:show_binds`).
    *   If **both** are missing: Returns 404.

### 2. Permissions on Volumes
*   Docker volumes on Linux/Prod often entail permission issues when writing generated images or logs.
*   **Solution**: Ensure the container runs as `root` in production, or carefully manage PUID/PGID matching host folder ownership. Current prod setup uses `user: root`.

### 3. ImageMagick / Wand
*   The application relies on `Wand` (ImageMagick binding).
*   If `Wand` is missing/broken, the app catches the `ImportError` and operates in a degraded mode (no image generation), logging the error to `www/configs/error.log`.

### 4. Download Links
*   When generating download links for `.binds` files, **always** include the subdirectory prefix.
    *   ❌ Incorrect: `url_for(..., path=f"{run_id}.binds")`
    *   ✅ Correct: `url_for(..., path=f"{run_id[:2]}/{run_id}.binds")`

## 🛠️ Debugging Tools

### Admin Debug Panel (`/admin/debug`)
Use this hidden route to investigate the production environment without shell access:
*   **File Browser**: Check existence of files in `configs/` (supports subdirectories like `ck/`).
*   **Logs**: View the tail of `www/configs/error.log`.
*   **Wand Status**: Check if the image renderer library is loaded correctly.

### Logging
*   **Persistent Log**: `www/configs/error.log`. Writes explicitly to disk (unlike stdout which can be lost in rotation).
*   **Memory Buffer**: Last ~50 errors are kept in memory and visible on the Debug page.

## 📝 Common Tasks

### Adding a New Device
1.  Add entry to `scripts/bindingsData.py` (`supportedDevices`).
2.  If it's a new `Template`, ensure the `.jpg` background exists in `www/images/`.
3.  Restart app (or reload if in dev mode).

### Restoring Database
If the SQLite DB is corrupted or lost:
1.  Ensure `www/configs` still contains the `.replay` files.
2.  Go to `https://your-url/admin/migrate` and run the migration.