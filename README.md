# EDRefCard

Elite: Dangerous has a great many command bindings to learn. To help with that, EDRefCard generates a printable reference card from your Elite: Dangerous bindings file.

Hosted at [https://edrefcard.info/](https://edrefcard.info/).

## Dependencies

* Python 3.12 or later (the Docker image uses Python 3.13)
* Python modules (pinned in `requirements.txt`, full tree frozen in `constraints.txt`):
  * `flask`, `Flask-Limiter` - Web framework and rate limiting
  * `gunicorn` - WSGI HTTP server
  * `lxml` - XML parsing
  * `wand` - ImageMagick bindings (card rendering)
  * `Pillow`, `fpdf2` - Image handling and PDF export
  * `PyMuPDF` - Import of manufacturer button sheets (admin)
  * `paramiko`, `APScheduler`, `requests`, `cryptography` - Backup system
  * Test and lint tools are in `requirements-dev.txt`

* ImageMagick 6 or 7
  * You may need to configure the `MAGICK_HOME` env var to get `wand` to see the ImageMagick libraries.

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask development server
cd www
python app.py

# Access at http://localhost:8080
```

### Docker (Recommended for Local Development)

Build and run with Docker:

```bash
docker build -t edrefcard .
docker run -d --rm --name edrefcard -p 8080:8000 edrefcard
# Access at http://localhost:8080
```

Or with docker compose:

```bash
docker compose up -d
# Access at http://localhost:8080
```

> [!NOTE]
> `docker-compose.prod.yml` is the production variant: no port mapping (a Traefik reverse proxy reaches the container on port 8000) and a persistent volume for `configs/`. It only passes the environment variables listed in its `environment:` section, so a new variable must be added there too.

## Project Structure

```
edrefcard2/
├── www/
│   ├── app.py              # Flask application entry point
│   ├── web.py              # Public pages (upload, cards, list, devices, stats)
│   ├── api.py              # JSON API
│   ├── commands.py         # flask CLI commands (maintenance, imports)
│   ├── admin/              # Admin panel: auth, backups, dashboard charts, mapping tools
│   ├── templates/          # Jinja2 HTML templates
│   ├── scripts/
│   │   ├── parser.py       # Bindings file parsing
│   │   ├── renderer.py     # Reference card rendering
│   │   ├── database.py     # SQLite storage
│   │   ├── models.py       # Configurations and their files
│   │   ├── bindingsData.py # Legacy device definitions and templates
│   │   ├── controlsData.py # Elite: Dangerous commands and their groups
│   │   ├── keyboardLayouts.py  # Visual keyboard layouts (ANSI, AZERTY)
│   │   ├── mapping_*.py    # Data-driven controller mappings (runtime, validation, lint, diff)
│   │   ├── scaffold.py     # Mapping drafts generated from a .binds or from input counts
│   │   ├── pdf_import.py   # Import of manufacturer button sheets
│   │   └── live_import.py  # Import of the original site's cards
│   ├── configs/            # Bindings, database and generated images (created at runtime)
│   ├── res/                # Image templates of the legacy controllers
│   └── fonts/              # Font files
├── bindings/               # Sample and test binding files
├── tests/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
└── requirements.txt
```

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with upload form |
| `/generate` | POST | Upload .binds file and generate reference card |
| `/list` | GET | List all public configurations |
| `/binds/<id>` | GET | View a saved configuration |
| `/download/<id>/pdf` | GET | Download the reference card as PDF |
| `/devices` | GET | List all supported controllers |
| `/device/<name>` | GET | View a device's button layout |
| `/stats` | GET | Public usage statistics |
| `/privacy` | GET | Privacy policy and legal notice |
| `/configs/<path>` | GET | Static files (generated images) |
| `/api/v1/generate` | POST | Programmatic upload of bindings |
| `/api/v1/binds/<id>` | GET | Configuration metadata as JSON |
| `/admin/` | GET | Admin panel (role `admin`) |
| `/admin/controllers` | GET | Controller mappings and unknown devices (role `mapper` or `admin`) |
| `/admin/mapping-editor` | GET | Mapping Editor (role `mapper` or `admin`) |

## Features

### Lightbox Image Viewer
Reference card images can be viewed in full-screen mode:
- **Click** any reference card image to open lightbox
- **Close** with × button or `Escape` key
- **Keyboard support** for accessibility
- **Responsive** design works on all screen sizes

### Controller Cards Without Code Changes
New controllers are drawn in the admin Mapping Editor and stored as data: a product photo, one box per
physical control and its leader line. Mappers save drafts, an admin reviews and publishes them, and the card
is live without a deploy. A controller with neither a mapping nor a legacy template still gets a text card
listing its bindings. See [CONTROLLER_MAPPING_GUIDE.md](CONTROLLER_MAPPING_GUIDE.md).

### Keyboard Cards
Keyboard bindings can be shown as a text list or on a visual keyboard (US ANSI 104 or French AZERTY ISO 105).

### Unlisted Cards
Cards are listed in the public catalogue by default; the uploader can untick the option to keep a card
reachable only by its link.

### Friendly URLs
Configurations use the bindings filename as their unique ID in the URL (e.g., `/binds/my-setup`).
If a name is already taken, a random suffix is added to ensure uniqueness.
Cards from the original site keep their six-letter IDs, so old links keep working.

### Global Analytics
A public dashboard (`/stats`) showing:
- Daily upload activity charts.
- Most popular controller types rankings.

### Public API
A JSON API is available for third-party integrations:
- `POST /api/v1/generate`: Programmatic upload of bindings.
- `GET /api/v1/binds/<id>`: Retrieve configuration metadata.

## Changelog

See [ChangeLog.md](ChangeLog.md).

## Configuration

The application is configured with environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_URL` | Public URL of the site, printed on the cards and PDFs | `http://localhost:8080/` |
| `APP_ENV` | `development`, `staging` or `production` (production enables scheduled backups) | `development` |
| `EDREFCARD_CONFIGS_DIR` | Where bindings, the database and generated images are stored | `www/configs` |
| `TRUSTED_PROXY_HOPS` | Number of reverse proxies whose forwarded headers are trusted | `1` |
| `CANONICAL_URL` | With `REDIRECT_HOSTS`: the address other host names redirect to | (unset) |
| `REDIRECT_HOSTS` | Comma-separated host names answered with a 301 to `CANONICAL_URL`, path kept | (unset) |
| `ACCESS_TOKEN` | Puts the whole site behind an access code (staging only) | (unset) |
| `BACKUP_ENV_LABEL` | Environment name shown in backup notifications (e.g. `staging`, `production`) | `unknown` |
| `EDREFCARD_ADMIN_USER` | Admin username | `admin` |
| `EDREFCARD_ADMIN_PASS` | Admin password | `changeme` |
| `FLASK_SECRET_KEY` | Secret key for sessions | `dev-secret-key...` |

## Supported Controllers

About 70 controllers are supported by the original templates, including:
- Thrustmaster (T16000M, HOTAS Warthog, T-Flight, etc.)
- Logitech (Extreme 3D Pro, X52, X56, etc.)
- VKB (Gladiator, Kosmosima, STECS, etc.)
- Virpil (WarBRD, Alpha, MongoosT, etc.)
- Winwing (Orion, Ursa Minor)
- CH Products (Fighterstick, Pro Throttle, etc.)
- Xbox 360 / PlayStation / Gamepads
- Standard keyboard

Controllers mapped in the Mapping Editor come on top of these. See the full list at `/devices` on the running
application.

## Admin Panel

EDRefCard includes a built-in admin panel at `/admin/`. The account defined by `EDREFCARD_ADMIN_USER` /
`EDREFCARD_ADMIN_PASS` is always an admin; further accounts are created from the panel with one of two roles:
`admin` (everything) or `mapper` (controller mapping only).

- **Dashboard**: cards created per day and per month, top 5 controllers, usage figures
- **Configurations**: list, search, edit, delete and toggle visibility of user configurations; batch import
- **Controllers**: unknown devices seen in uploads, controller mappings with draft review, publication,
  history and rollback
- **Mapping Editor** and its mapper guide (`/admin/help`)
- **Users**: admin and mapper accounts
- **Backups**: scheduled local and SFTP backups with Discord notifications, restore, maintenance mode

## Data Storage

EDRefCard uses a hybrid storage approach:
- **SQLite Database (`configs/edrefcard.db`)**: Stores configuration metadata (id, description, status, devices used), controller mappings with their versions, and admin accounts.
- **Filesystem**: Stores generated images (`.jpg`) and original bindings files (`.binds`) in the `configs/` directory.

> [!NOTE]
> The `.replay` pickle files of the original site are no longer used. `flask import-live` reads them once, safely, to bring the original site's cards over with their title and date.

## Maintenance

The application includes CLI commands for maintenance tasks:

```bash
# Clean generated images older than 1 day
flask --app www/app.py clean-cache --days 1

# Find unsupported controls in a log file
flask --app www/app.py find-unsupported error.log

# Rebuild the database from the .binds files on disk
flask --app www/app.py rebuild-db

# Import the cards of the original site from an extracted configs folder
flask --app www/app.py import-live /path/to/configs --dry-run
```

## Development

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest --cov=. --cov-report term-missing
```

### Adding New Controllers

New controllers are added in the admin Mapping Editor, not in code: see
[CONTROLLER_MAPPING_GUIDE.md](CONTROLLER_MAPPING_GUIDE.md). The legacy templates in
`www/scripts/bindingsData.py` and `www/res/` are only edited to fix an existing card.

## Credits

EDRefCard is derived with permission from code originally developed by CMDR jgm.

## License

See [LICENSE](LICENSE) file.
