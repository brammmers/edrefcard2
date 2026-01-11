# EDRefCard

Elite: Dangerous has a great many command bindings to learn. To help with that, EDRefCard generates a printable reference card from your Elite: Dangerous bindings file.

Currently hosted at [https://edrefcard.dp.l0l.fr/](https://edrefcard.dp.l0l.fr/).

## Dependencies

* Python 3.12 or later (Python 3.13+ recommended)
* Python modules (see `requirements.txt`):
  * `flask` - Web framework
  * `gunicorn` - WSGI HTTP server
  * `lxml` - XML parsing
  * `wand` - ImageMagick bindings
  * `pytest`, `pytest-cov` - Testing

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

# Access at http://localhost:5000
```

### Docker (Recommended for Local Development)

Build and run with Docker:

```bash
docker build -t edrefcard .
docker run -d --rm --name edrefcard -p 8080:8000 edrefcard
# Access at http://localhost:8080
```

Or with docker-compose (add port mapping for local access):

```bash
# For local development, add ports to docker-compose.yaml:
# ports:
#   - "8080:8000"
docker-compose up -d
# Access at http://localhost:8080
```

> [!NOTE]
> For production deployment with Traefik/Dokploy, remove the `ports` section from docker-compose.yaml. Traefik connects directly to the container via Docker network on port 8000.

## Project Structure

```
edrefcard/
├── www/
│   ├── app.py              # Flask application entry point
│   ├── templates/          # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── refcard.html
│   │   ├── list.html
│   │   ├── devices.html
│   │   └── error.html
│   ├── scripts/
│   │   ├── bindings.py     # Core binding parsing logic
│   │   ├── bindingsData.py # Device definitions
│   │   └── controlsData.py # Control mappings
│   ├── configs/            # Generated configurations (created at runtime)
│   ├── res/                # Image templates for devices
│   ├── fonts/              # Font files
│   └── ed.css              # Stylesheet
├── bindings/               # Test binding files
├── Dockerfile
├── docker-compose.yaml
└── requirements.txt
```

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with upload form |
| `/generate` | POST | Upload .binds file and generate reference card |
| `/list` | GET | List all public configurations |
| `/binds/<id>` | GET | View a saved configuration |
| `/devices` | GET | List all supported controllers |
| `/device/<name>` | GET | View a device's button layout |
| `/configs/<path>` | GET | Static files (generated images) |

## Features

### Lightbox Image Viewer
Reference card images can be viewed in full-screen mode:
- **Click** any reference card image to open lightbox
- **Close** with × button or `Escape` key
- **Keyboard support** for accessibility
- **Responsive** design works on all screen sizes

### Admin Dashboard
Comprehensive admin panel for configuration management:
- View usage statistics and popular devices
- Search and filter configurations
- Toggle public/private visibility
- Bulk operations and data migration tools

### Auto-Migration
Legacy pickle-based configurations are automatically migrated to SQLite on first startup.

### 📊 Global Analytics
New in v2.1: A public dashboard (`/stats`) showing:
- Daily upload activity charts.
- Most popular controller types rankings.

### 🔌 Public API
New in v2.1: A JSON API is available for third-party integrations.
- `POST /api/v1/generate`: Programmatic upload of bindings.
- `GET /api/v1/binds/<id>`: Retrieve configuration metadata.

## Changelog

### v2.1 (2025-01-08)
*   **Frontend**:
    *   Added **Drag & Drop** support with immediate file validation and preview.
    *   Added **Sharing Tools**: Copy link button, social sharing (Reddit/X), and visual feedback.
    *   Added **Global Analytics Dashboard** (`/stats`) with Chart.js visualization.
*   **Backend**:
    *   Implemented **Public JSON API** (`/api/v1/generate`).
    *   Refactored `app.py` into modular **Blueprints** (`web`, `api`, `admin`) for better maintainability.
    *   Standardized route namespaces in templates.

## Configuration

The application can be configured via environment variables or by modifying the Flask app configuration in `www/app.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHONIOENCODING` | Character encoding | `utf-8` |

## Supported Controllers

EDRefCard supports 68+ controllers including:
- Thrustmaster (T16000M, HOTAS Warthog, T-Flight, etc.)
- Logitech (Extreme 3D Pro, X52, X56, etc.)
- VKB (Gladiator, Kosmosima, etc.)
- Virpil (WarBRD, Alpha, MongoosT, etc.)
- CH Products (Fighterstick, Pro Throttle, etc.)
- Xbox 360 / PlayStation controllers
- Standard keyboard

See the full list at `/devices` on the running application.

## Admin Panel

EDRefCard v2.0 includes a built-in admin panel for managing configurations and devices.

### Access
- URL: `/admin/`
- Authentication: HTTP Basic Auth

### Configuration
Set the following environment variables to configure admin access:

| Variable | Description | Default |
|----------|-------------|---------|
| `EDREFCARD_ADMIN_USER` | Admin username | `admin` |
| `EDREFCARD_ADMIN_PASS` | Admin password | `changeme` |
| `FLASK_SECRET_KEY` | Secret key for sessions | `dev-secret-key...` |

### Features
- **Dashboard**: View statistics on configuration usage and popular devices
- **Configurations**: List, search, delete, and toggle visibility of user configurations
- **Devices**: View list of supported devices and their template mappings
- **Data Migration**: Tool to import legacy pickle files into the SQLite database

## Data Storage

EDRefCard v2.0 uses a hybrid storage approach:
- **SQLite Database (`edrefcard.db`)**: Stores configuration metadata (id, description, status, devices used).
- **Filesystem**: Stores generated images (`.jpg`) and original bindings files (`.binds`) in the `configs/` directory.

When upgrading from v1.0, use the `/admin/migrate` tool to import existing pickle files into the database.

## Maintenance

The application includes CLI commands for maintenance tasks:

```bash
# Clean generated images older than 1 day
flask --app www/app.py clean-cache --days 1

# Find unsupported controls in a log file
flask --app www/app.py find-unsupported error.log

# Import legacy configurations (pickle) to SQLite
flask --app www/app.py migrate-legacy
```

## Development

### Running Tests

```bash
pytest --cov=. --cov-report term-missing
```

### Adding New Controllers

1. Add device definition to `www/scripts/bindingsData.py`
2. Add button/axis image template to `www/res/`
3. Run tests to validate

## Credits

EDRefCard is derived with permission from code originally developed by CMDR jgm.

## License

See [LICENSE](LICENSE) file.
