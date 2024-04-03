

from flask import Flask, jsonify, render_template, request, redirect, url_for
from src.config import (PORT, STATIC_FOLDER_PATH, application)
from flask import Flask, request, jsonify, url_for
# Instead of from src.routes import leaderboard, engagement
from src.routes import leaderboard

# Instead of from src.services.flask_socket import socketio, emit_carrousel_refresh
from src.services.flask_socket import socketio, emit_carrousel_refresh

# Instead of from src.services.db.input_manager import InputManager
from src.services.db.input_manager import InputManager

# Instead of from src.controllers.leaderboard_controller import get_leaderboard
from src.controllers.leaderboard_controller import get_leaderboard

from flask_socketio import SocketIO, emit

import json
from datetime import datetime
import os
import random

from werkzeug.utils import secure_filename

# Instead of from src.models import InputModel
from src.models import InputModel




#@application.route('/billboard')
#def render_billboard():
#    with InputManager() as db:
#        initial_src = db.get_highest_ranked_input_src()
#        return render_template('billboard.html', initial_src=initial_src)


#@application.route('/dashboard')
#def render_leaderboard():
#    # Pass the list of LeaderBoard objects to the template
#    leaderboard_list = get_leaderboard()
#    return render_template('dashboard.html', leaderboard_list=leaderboard_list)


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

        client_name = request.form.get('client_name')
        curr_date = request.form.get('date')
        main_image_file = request.files.get('main_image')
        main_image_description = request.form.get('main_image_description')
        related_image1_file = request.files.get('related_image1')
        related_image1_description = request.form.get('related_image1_description')
        related_image2_file = request.files.get('related_image2')
        related_image2_description = request.form.get('related_image2_description')
        related_image3_file = request.files.get('related_image3')
        related_image3_description = request.form.get('related_image3_description')

        # Ensure the 'static' folder exists, create it if not
        if not os.path.exists(STATIC_FOLDER_PATH):
            os.makedirs(STATIC_FOLDER_PATH)

        def save_image(image_file):
            if image_file:
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(STATIC_FOLDER_PATH, filename)
                image_file.save(image_path)
                return request.url_root + "static/" + filename
            return None
        
        main_image_path = save_image(main_image_file)
        related_image_paths = [
            save_image(related_image1_file),
            save_image(related_image2_file),
            save_image(related_image3_file)
        ]
        related_descriptions = [
            related_image1_description,
            related_image2_description,
            related_image3_description

        ]
        image_data = json.dumps({
            "main_image": {
                "path": main_image_path,
                "description": main_image_description
            },
            "related_images": [
                {"path": path, "description": desc} 
                for path, desc in zip(related_image_paths, related_descriptions) if path
            ]
        })
        model = InputModel(
            date = curr_date,
            duration = "00:00:10",
            numberOfPeople = 0,
            numberOfEngagedPeople=0,
            score=0,
            image_data=json.dumps(image_data)  # Convert image_data to JSON string for database storage
        )
        with InputManager() as db:
            db.create_input(model)
        #return jsonify({"message": "Content and images uploaded successfully"}), 200

        return redirect(url_for('success'))

    return render_template('new-content.html')


# Route for a success page
@application.route('/success')
def success():
    return render_template('success.html')

DATABASE = "ClientInput"

#@application.route("/brain", methods = ["POST"])
#def brain():




#where the self.engagement_counter is suppose to send engagement score every event 
@application.route("/engagement",methods =["POST"])
def update_engagement():
    received_data = request.json
    score = received_data.get("score", 0)
    numberOfPeople = received_data.get("numberOfPeople", 0)
    numberOfEngagedPeople = received_data.get("numberOfEngagedPeople", 0)
    
    with InputManager() as db:
        db.add_score(score,id) #  modify here, 0 needs to be input_id from client.js
        db.add_numberof(numberOfPeople,numberOfEngagedPeople)
    

@application.route("/events/<event>", methods = ["POST"])
def send_activity(event):
    
    socketio.emit('message', {'data' : event})
    return "Message sent"

@socketio.on('connect') # sends schema to client upon app launch
def send_schema():
    input_schema = {
        "table": "input",  # Updated table name to match your provided schema
        "columns": [
            {"name": "id", "type": "INT", "constraints": ["AUTO_INCREMENT", "PRIMARY KEY"]},
            {"name": "date", "type": "DATE"},
            {"name": "duration", "type": "TIME"},
            {"name": "numberOfPeople", "type": "INT"},
            {"name": "numberOfEngagedPeople", "type": "INT"},
            {"name": "score", "type": "FLOAT"},
            {"name": "image_data", "type": "JSON"},  # Added to reflect your updated schema
        ]
    }
    socketio.emit('schema_data', input_schema)


@application.route('/leaderboard') # puts data into leaderboard.html
def leaderboards():
    with InputManager() as db:
        data = db.leaderboard_data()
    return render_template('leaderboard.html', data = data)

if __name__ == '__main__':
    # connect to database here

    # register routes
    application.register_blueprint(leaderboard, url_prefix='/leaderboards')
    # Run the Flask application with Socket.IO support
    socketio.run(application, port=8000, debug=True, allow_unsafe_werkzeug=True)

    

