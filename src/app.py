from flask import render_template
from src.config import PORT
from src.routes import leaderboard
from src.config import application
from src.services.flask_socket import socketio, emit_carrousel_refresh


@application.route('/billboard')
def render_billboard():
    return render_template('billboard.html')


@socketio.on('refresh')
def handle_refresh():
    # handle href logic here
    hrefs = ['https://picsum.photos/200', 'https://picsum.photos/200'] # insert the images here
    emit_carrousel_refresh(hrefs)


if __name__ == '__main__':
    # connect to database here
    
    # register routes
    application.register_blueprint(leaderboard, url_prefix='/leaderboards')
    # Run the Flask application with Socket.IO support
    socketio.run(application, port=PORT, debug=True, allow_unsafe_werkzeug=True)
