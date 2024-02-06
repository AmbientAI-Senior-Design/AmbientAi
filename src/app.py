from flask import Flask, render_template
from src.config import PORT
from src.routes import leaderboard

# TODO: add the setup steps for mysql in setup.sql 

application = Flask(__name__)

@application.route('/billboard')
def render_billboard():
    return render_template('billboard.html')


if __name__ == '__main__':
    # connect to database here
    
    # register routes
    application.register_blueprint(leaderboard, url_prefix='/leaderboards')
    application.run(port=PORT, debug=True)
