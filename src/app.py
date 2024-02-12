from flask import Flask
from config import PORT
from src.routes import leaderboard


if __name__ == '__main__':
    app = Flask(__name__)
    # connect to database here
    ...
    # register routes
    app.register_blueprint(leaderboard, url_prefix='/leaderboards')
    app.run(port=PORT, debug=True)
