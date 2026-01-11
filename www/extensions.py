from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Limiter (will be attached to app later)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    strategy="fixed-window"
)
