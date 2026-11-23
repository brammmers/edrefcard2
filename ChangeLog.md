# Change Log

## Unreleased (January to November 2026)

Everything merged into `main` since 2.2.0. Since 16 November 2026 this code serves
[edrefcard.info](https://edrefcard.info/).

### Controller mappings (new controllers without code changes)
* **Data-driven cards**: a controller's card can now be described as data (photo, boxes, rows, leader lines)
  stored in the database, instead of coordinates hard-coded in `bindingsData.py`. Unused boxes and rows are
  hidden for each player. A published mapping takes over the legacy template of the same controller.
* **Mapping Editor** (`/admin/mapping-editor`): click-to-place boxes on a product photo, stamps (button, hats
  with or without push, POV, 2-stage trigger, stick, axis) with auto-incremented `Joy_N`, automatic arrangement
  in two columns, multi-select, alignment and spacing tools, snapping guides, draggable anchors, optional leader
  detour, movable title and URL, JSON import and export, undo and redo, live checks, and a preview rendered with
  any saved player profile, with a coverage report.
* **Manufacturer sheets**: import of Virpil fillable PDFs and VKB worksheets, with a review of the declared
  inputs before they are kept.
* **Controllers page** (`/admin/controllers`): queue of the unknown hardware IDs seen in real uploads, with a
  scaffold pre-filled from a real `.binds` or a blank scaffold from button, POV and axis counts; attachment of a
  variant ID to a known controller; duplication with an optional mirror for left and right variants.
* **Mapper accounts and review**: `admin` and `mapper` roles with session login (`/admin/users`); every save is
  a draft, an admin reviews the changes with layout previews and publishes; full version history with rollback,
  audit trail, concurrent-edit protection, recovery of unsaved work, Discord notifications.
* **Photo-less cards**: a controller without a mapping or a template gets a text card listing its bindings by
  group instead of an error.
* The public `/devices` page lists the published mappings, and the mapper guide is available in the panel
  (`/admin/help`) and in [CONTROLLER_MAPPING_GUIDE.md](CONTROLLER_MAPPING_GUIDE.md).

### Cards and site
* **New home page** ("Cockpit"): an official Elite Dangerous image framed like a canopy, live figures, the
  upload form as three side panels, the latest public cards with small previews (`/thumb/<id>.jpg`, built once
  with Pillow under `configs/_thumbs/`) and the supported controllers. Its own stylesheet (`home.css`), so the
  other pages are unchanged.
* **Keyboard**: visual keyboard cards (US ANSI 104 and French AZERTY ISO 105) next to the text list; the text
  card now shrinks until every column fits, with plain-text key labels.
* **Controls**: Camera and Settlement categories.
* **Unlisted cards**: uploaders can keep a card out of the public catalogue; it stays reachable by its link.
* **Catalogue** (`/list`): free-text search, pagination, device filters with consistent counts.
* **Privacy policy and legal notice** (`/privacy`).
* **Contact form** (`/contact`): missing controller, wrong card or anything else, with an optional card
  reference (prefilled from the unsupported-controller warnings) and an optional reply address. Sent by SMTP
  from the maintainers' mailbox (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `CONTACT_TO`); without
  that configuration the page points to the forum thread. Spam is filtered without a captcha (hidden field,
  minimal fill time, same-origin check, 5 messages per hour per IP).
* **Render cache**: generated cards are reused until the code or the card's data changes; stale images and PDFs
  are dropped before a card is drawn again.
* Same-named uploads no longer overwrite an existing card.
* Several legacy cards fixed (Thrustmaster TCA left sidestick, Cougar throttle radio buttons) and 21 phantom
  device entries removed.

### Moving edrefcard.info to this code
* `flask import-live` brings the original site's cards over with their six-letter IDs, title and date, so old
  links keep working; untitled cards come over as unlisted.
* Uploads still sent to the original `scripts/bindings.py` address reach `/generate`.
* `CANONICAL_URL` and `REDIRECT_HOSTS`: 301 redirects from the site's former host names, path kept.

### Admin and operations
* **Backups**: scheduled local and SFTP backups with retention, restore from a local, SFTP or uploaded archive,
  hourly health check, Discord notifications labelled per environment (`BACKUP_ENV_LABEL`), maintenance mode.
  Controller mappings and their images are part of the backup.
* **Dashboard**: cards created per day (30, 90 or 365 days, with a 7-day average), per month, and top 5
  controllers.
* `flask rebuild-db` rebuilds the database from the `.binds` files on disk.
* `ACCESS_TOKEN` puts a staging site behind an access code.
* Gunicorn workers are recycled to cap memory growth.

### Security
* Database, logs and source code are no longer reachable through the static routes.
* Restore hardened against path traversal in archives; SFTP host keys pinned; SSRF guards on SFTP and Discord
  settings.
* Same-origin CSRF guard on the admin panel, constant-time credential checks, login rate limiting, hardened
  session cookies revalidated on each request.
* Escaped error pages, scoped configuration deletion, configurable trusted proxy hops (`TRUSTED_PROXY_HOPS`).
* Rate limits are counted once for all gunicorn workers (SQLite counters, `RATELIMIT_STORAGE_URI`) instead of
  once per worker, and crawlers that ignore robots.txt are refused by User-Agent (`BLOCKED_USER_AGENTS`,
  default `CorsairBot`).

### Development
* CI gates releases on real card rendering and on the mapper workflow.
* Legacy CGI `bindings.py` monolith removed; a single generation loop for legacy cards.

## 2.2.0 (2026-01-18)
### Features
* **Friendly URLs**: Configurations now use the upload filename as ID (slugified) instead of random strings.
* **Graceful Device Support**: 
  - Missing image templates no longer crash the rendering engine.
  - Page renders supported devices and shows a warning for unsupported ones with an official forum link.
* **Batch Import Improvements**: Added filename-based ID generation and automatic skipping of existing configurations.
* **API Update**: JSON API now supports friendly URLs consistent with the web interface.

### Improvements & Cleanup
* **Legacy Code Removal**: Completely removed obsolete pickle migration logic (auto-migration, CLI commands, and admin buttons).
* **Code Quality**: Unified ID generation logic and improved error handling in the renderer.

## 2.0.1 (2025-12-31)
### Bug Fixes
* **Template Error**: Fixed Jinja2 TemplateSyntaxError in `refcard.html` that caused 500 errors on configuration pages
* **Data Migration**: Fixed auto-migration to handle partial database states (88 configs successfully restored)
* **Error Handling**: Fixed `Config.path` method call error in Admin module that caused 500 errors
* **CI/CD**: Resolved ruff linting failures by updating configuration (748 → 30 errors, 96% reduction)

### Features
* **Lightbox**: Added full-screen image viewer for reference cards
  - Click-to-zoom on any reference card image
  - Close with X button or Escape key
  - Smooth animations and responsive design
* **Docker Testing**: Added automated Docker build and startup tests to CI pipeline

### Improvements
* **Python Version**: Upgraded to Python 3.13 for better performance and longer support
  - Updated base Docker image to `python:3.13-slim`
  - CI now tests Python 3.12, 3.13, and 3.14
  - Support lifecycle extended until October 2029
* **Code Quality**: Updated ruff and mypy configurations for modern Python
* **Documentation**: Updated README with current Python requirements and features

## 2.0.0 (2025-12-31)
### Major Features
* **Admin Panel**: Introduced a secured Admin Dashboard (`/admin`) for managing configurations and devices.
* **SQLite Database**: Migrated from file-based storage (Pickle) to a structured SQLite database for better performance and data integrity.
* **Docker Support**: Added `Dockerfile` and `docker-compose.yaml` for streamlined deployment and development.
* **Authentication**: Implemented HTTP Basic Auth for admin routes.

### Improvements
* **Architecture**: Refactored into Flask Blueprints for better modularity.
* **CI/CD**: Added GitHub Actions workflows for automated testing and linting.
* **Code Quality**: Integrated `ruff` for code style enforcement.
* **Modernization**: Updated dependencies and removed legacy code.

## 1.4
  * Completed all the outstanding pull requests from GitHub and merged them
  * Adjusted for Python 3.10 compatibility
  * Tested with Python 3.10/Ubuntu 22.04 on WSL2
  * Added support for Xbox360 controller clone (VOYEE Wired 360 - HY4102)

## 1.3.1
* Sundry cleanup and fixes.

## 1.3
* Added support for VKB Gladiator Left and Right sticks, courtesy of awerschlan and esabouraud.
* Added support for VPC Alpha Left and Right grips, courtesy of Slion.
* Added searching by controller type, courtesy of alewando.
* Added support for Odyssey's "On Foot" bindings.

## 1.2.8
* Added support for VKB Kosmosima SCG Left and Right grips, courtesy of ajhewett.
* Handled invalid keyboard bindings of the form `Device="Keyboard" Key=""`

## 1.2.7
* Added support for Thrustmaster Hotas Cougar.

## 1.2.6
* Added binding for Store Toggle Preview.

## 1.2.5
* Added bindings for the Store Camera.
* Revised the color palette.

## 1.2.4

* Amended the VKB Gladiator bindings: my thanks to KellyR (CMDR Analee Winston) for kicking my behind on this an providing corroborating data.
* Added a new URL `https://edrefcard/devices` listing all supported devices by primary name and linking to:
  * New endpoints `https://edrefcard//device/xxx` that show the given device's button names in rectangles shaded in light green and outlined in red, to assist with (a) debugging button mappings and (b) aligning the rectangles pixel-perfect.
* Tweaked CSS styling and column width settings for `/list` and `/devices` to make the table neater. I'll be the first to admit this isn't my strong suit.
* Reduced the maximum input length for the "description" field to 190 characters in light of the above.
* Updated the forum thread URL.

## 1.2.3

* Restored caching of rendered JPEGs to one day now that we have more disk space.

## 1.2.2

* Improved the error reporting when there is an error parsing the bindings file.

## 1.2.1

* Added the new bindings introduced in Chapter 4 beta 3.
* Updated the code that prevents redundant specialisations from being shown on the same card (e.g. when GalMap pitch axis is the same as your regular pitch axis). This should make cards more concise w/o loss of clarity.

## 1.2

* Command names are now in Title Case and some have been abbreviated.
* The keyboard chart makes more use of symbols to identify the keys.
* The Galaxy map controls now say "GalMap" rather than "Camera".
* Added support for Dual Virpil VPC WarBRD DELTA joysticks.
* Added support for Saitek X45 HOTAS.

## 1.1

* Blocking "spammy" descriptions is as those starting with punctuation.

## 1.0.8

* Added bindings introduced in Chapter 4, notable the FSS scanner.

## 1.0.7

* Fixed errors with non-ASCII file encodings. Should now be fully Unicode.

## 1.0.6

* The list view is now sorted in a case-insensitive manner.
* The home page now correctly uses https to access its style sheet from Google APIs. Thanks to eeisenhart.

