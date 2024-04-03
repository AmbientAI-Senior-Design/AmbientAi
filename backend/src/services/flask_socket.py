from flask_socketio import SocketIO
from src.config import application


socketio = SocketIO(application, cors_allowed_origins="*")


def emit_carrousel_refresh(hrefs: list[str]):
    socketio.emit('update_data', hrefs)
