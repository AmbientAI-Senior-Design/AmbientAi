from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS
socketio = SocketIO(app, cors_allowed_origins="*")
@app.route('/events/<event>', methods=['POST'])
def handle_event(event):
    socketio.emit('message', {'data': event})
    return 'Message sent'

if __name__ == '__main__':
    socketio.run(app, port=8080)