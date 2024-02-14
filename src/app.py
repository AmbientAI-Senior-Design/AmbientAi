from flask import render_template
from src.config import PORT
from src.routes import leaderboard, engagement
from src.config import application
from src.services.flask_socket import socketio, emit_carrousel_refresh
from src.services.db.input_manager import InputManager


@application.route('/billboard')
def render_billboard():
    return render_template('billboard.html')


@socketio.on('refresh')
def handle_refresh():
    # handle href logic here
    # TODO: nick, get hrefs (input_image_path) from database, sort them by score
    with InputManager() as db:
        hrefs = db.get_hrefs_for_leaderboard()
        emit_carrousel_refresh(hrefs)


if __name__ == '__main__':
    # connect to database here

    # register routes
    application.register_blueprint(leaderboard, url_prefix='/leaderboards')
    application.register_blueprint(engagement, url_prefix="/engagement")

    # Run the Flask application with Socket.IO support
    socketio.run(application, port=PORT, debug=True, allow_unsafe_werkzeug=True)
