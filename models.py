from .db_instance import db, BIND_KEY


class chat_history(db.Model):
    __bind_key__ = BIND_KEY

    id = db.Column(db.Integer, primary_key=True)