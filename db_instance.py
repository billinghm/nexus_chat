import os

# Bind key + db file used by this app's models, whether running standalone
# or embedded. Computed relative to this file so both entry points resolve
# to the same physical database.
BIND_KEY = "nexus_chat"
DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "instance", "nexus_chat.db"
).replace(os.sep, "/")

try:
    # Embedded in a portal: use the shared SQLAlchemy instance from the
    # project root, so all apps register models on the same db/app.
    from extensions import db
except ImportError:
    # Standalone: this package's own instance.
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
