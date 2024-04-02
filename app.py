

from flask import Flask, jsonify, render_template, request, redirect, url_for
from src.config import (PORT, STATIC_FOLDER_PATH, application)

# Instead of from src.routes import leaderboard, engagement
from src.routes import leaderboard

# Instead of from src.services.flask_socket import socketio, emit_carrousel_refresh
from src.services.flask_socket import socketio, emit_carrousel_refresh

# Instead of from src.services.db.input_manager import InputManager
from src.services.db.input_manager import InputManager

# Instead of from src.controllers.leaderboard_controller import get_leaderboard
from src.controllers.leaderboard_controller import get_leaderboard

from flask_socketio import SocketIO, emit

import os
import random


# Instead of from src.models import InputModel
from src.models import InputModel




@application.route('/billboard')
def render_billboard():
    with InputManager() as db:
        initial_src = db.get_highest_ranked_input_src()
        return render_template('billboard.html', initial_src=initial_src)


@application.route('/dashboard')
def render_leaderboard():
    # Pass the list of LeaderBoard objects to the template
    leaderboard_list = get_leaderboard()
    return render_template('dashboard.html', leaderboard_list=leaderboard_list)


@application.route('/')
def render_index():
    return render_template('home.html')


@application.route('/content', methods=['POST'])
def handle_refresh():
    src = request.args.get('src')
    emit_carrousel_refresh([src])
    return '200'

def generate_random_id():
    return random.randint(1,1000000)

@application.route('/new-content', methods=["GET", "POST"])
def render_new_content():
    if request.method == 'POST':
        # Get form data
        image_name = request.form.get('image_name')
        client_name = request.form.get('client_name')
        image_file = request.files['image_`file']
        # Ensure the 'static' folder exists, create it if not
        if not os.path.exists(STATIC_FOLDER_PATH):
            os.makedirs(STATIC_FOLDER_PATH)

        # Save the uploaded image file to the 'static' folder
        image_path = os.path.join(STATIC_FOLDER_PATH, image_file.filename)
        image_file.save(image_path)
        model = InputModel(
            input_id = generate_random_id(),
            image_score=0,
            input_name=image_name,
            input_image_path=request.url_root + "static/" + image_file.filename,
            client_name=client_name
        )
        with InputManager() as db:
            db.create_input(model)

        # Perform any other processing with the form data as needed

        return redirect(url_for('success'))

    return render_template('new-content.html')


# Route for a success page
@application.route('/success')
def success():
    return render_template('success.html')

DATABASE = "ClientInput"


#where the self.engagement_counter is suppose to send engagement score every event 
@application.route("/engagement",methods =["POST"])
def update_engagement():
    scorerecv = request.json
    score = scorerecv.get("score", 0)
    with InputManager() as db:
        db.create_engagement(0, score) #  modify here, 0 needs to be input_id from client.js
    if score > 0:
        socketio.emit('update_data', ["http://127.0.0.1:8000/static/menu.PNG"])
    return {
        "status": 200,
        "Message": "Score updated"
    }

#socketio = SocketIO(application, cors_allowed_origins="*")
@application.route("/events/<event>", methods = ["POST"])
def send_activity(event):
    
    socketio.emit('message', {'data' : event})


@application.route("/current_score", methods=["GET"])
def current_score():
    with InputManager() as db:
        score = db.get_current_score()
    return jsonify({"Current eng score": score})

@application.route('/leaderboard') # puts data into leaderboard.html
def leaderboard():
    with InputManager() as db:
        data = db.leaderboard_data()
    return render_template('leaderboard.html', data = data)

if __name__ == '__main__':
    # connect to database here

    # register routes
    application.register_blueprint(leaderboard, url_prefix='/leaderboards')
    # Run the Flask application with Socket.IO support
    socketio.run(application, port=8000, debug=True, allow_unsafe_werkzeug=True)

    

