import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import inspect, text

from nexus_chat import nexus_chat_bp
from nexus_chat.db_instance import db, BIND_KEY, DB_PATH
try:
    from db_instance import db
except:
    pass

load_dotenv()

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db_uri = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_BINDS"] = {BIND_KEY: db_uri}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(nexus_chat_bp)

    
    with app.app_context():
        db.create_all()
        #add_column_if_missing('trades', 'notes', 'VARCHAR')


    return app

def add_column_if_missing(table, column, ddl_type):
    cols = [c['name'] for c in inspect(db.engine).get_columns(table)]
    if column not in cols:
        db.session.execute(text(f'ALTER TABLE {table} ADD COLUMN {column} {ddl_type}'))
        db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)