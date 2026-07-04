from flask import Blueprint

nexus_chat_bp = Blueprint(
    'nexus_chat',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/chat'
)

from . import routes
