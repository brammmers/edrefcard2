from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Importing the module registers the sqlite:// scheme with the limits library.
from ratelimit_storage import storage_uri

# Initialize Limiter (will be attached to app later). The counters are shared
# by every gunicorn worker when RATELIMIT_STORAGE_URI points to a SQLite file
# (see ratelimit_storage.py); swallow_errors keeps pages up if that file fails.
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=storage_uri(),
    strategy="fixed-window",
    swallow_errors=True,
)
