from flask import Flask, render_template
from src.config import PORT
from src.routes import leaderboard
from flask_socketio import SocketIO


application = Flask(__name__)
socketio = SocketIO(application)


@application.route('/billboard')
def render_billboard():
    return render_template('billboard.html')


@socketio.on('refresh')
def handle_refresh():
    # Handle the refresh images logic here
    socketio.emit('update_data', ["https://picsum.photos/200", "https://picsum.photos/200"])


if __name__ == '__main__':
    # connect to database here
    
    # register routes
    application.register_blueprint(leaderboard, url_prefix='/leaderboards')
    # Run the Flask application with Socket.IO support
    socketio.run(application, port=PORT, debug=True, allow_unsafe_werkzeug=True)
