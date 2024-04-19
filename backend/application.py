

from flask import Flask, jsonify, render_template, request, redirect, url_for
from src.config import (PORT, STATIC_FOLDER_PATH, application)
from werkzeug.utils import secure_filename
from src.routes import leaderboard
from src.services.flask_socket import socketio, emit_carrousel_refresh
from src.services.db.input_manager import InputManager
from flask_socketio import SocketIO, emit
import os
import random
from datetime import datetime
from src.models.input_model import PostModel, EngagementReportModel, SlideModel, BackendModel

# @application.route('/billboard')
# def render_billboard():
#     with InputManager() as db:
#         initial_src = db.get_highest_ranked_input_src()
#         return render_template('billboard.html', initial_src=initial_src)


# @application.route('/dashboard')
# def render_leaderboard():
#     leaderboard_list = get_leaderboard()
#     return render_template('dashboard.html', leaderboard_list=leaderboard_list)


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
        date = request.form.get('date')
        images = {}
        descriptions = {}
        for i in range(4):
            img_key = f"main_image" if i == 0 else f"related_image{i}"
            desc_key = f"main_image_description" if i == 0 else f"related_image{i}_description"
            image_file = request.files[img_key]
            description = request.form[desc_key]
            if not os.path.exists(STATIC_FOLDER_PATH):
                os.makedirs(STATIC_FOLDER_PATH)

            image_path = os.path.join(STATIC_FOLDER_PATH, image_file.filename)
            image_file.save(image_path)
            
            images[img_key] = image_path
            descriptions[desc_key] = description

        with InputManager() as db:
            for i, (img_key, desc_key) in enumerate(zip(images, descriptions)):
                model = EngagementReportModel(
                    id=generate_random_id(),
                    score=0,
                    input_name=images[img_key],
                    input_image_path=images[img_key],
                    description=descriptions[desc_key],
                    client_name=client_name,
                    date=date,
                    slide_index=i
                )
                db.create_input(model)
        with InputManager() as db:
            post_id = db.add_new_row_to_Post()
            db.add_fk_id(post_id)

        return redirect(url_for('success'))

    return render_template('new-content.html')

@application.route('/success')
def success():
    return render_template('success.html')

DATABASE = "ClientInput"
@application.route("/engagement",methods =["POST"])
def update_engagement():
    scorerecv = request.json
    score = scorerecv.get("score", 0)
    number_of_engaged_people = scorerecv.get("numberOfEngagedPeople", 0)
    number_of_people = scorerecv.get("numberOfPeople", 0)
    duration = scorerecv.get("duration", 0)
    with InputManager() as db:

       db.insert_into_db(score)

    if score > 0:
        socketio.emit('update_data', ["http://127.0.0.1:8000/static/menu.PNG"])
    return {
        "status": 200,
        "Message": "Score updated"
    }

@application.route("/events/<event>", methods = ["POST"])
def send_activity(event):
    
    socketio.emit('message', {'data' : event})
    return "Message sent"


@socketio.on("full-report")
def recv_data(data):
    with InputManager() as db:
        db.populate_db(data)


@application.route("/motion_report", methods = ["POST"])
def send_mreport():
    motion_rep = request.json
    motion_rep["date"] = datetime.now().date().isoformat()
    socketio.emit('motion_report', motion_rep)
    return {"Status": "Report sent"}


@application.route('/leaderboard')
def leaderboards():
    with InputManager() as db:
        data = db.leaderboard_data()
        
    return render_template('leaderboard.html', data = data)

@application.route('/upload-slides', methods=['POST'])
def upload_slides():
    client_name = request.form['client_name']
    date = request.form['date']
    descriptions = {
        'main_image': request.form['main_image_description'],
        'related_image1': request.form['related_image1_description'],
        'related_image2': request.form['related_image2_description'],
        'related_image3': request.form['related_image3_description']
    }
    if not os.path.exists(application.config['UPLOAD_FOLDER']):
        os.makedirs(application.config['UPLOAD_FOLDER'])

    with InputManager() as db:
        post_id = db.add_new_row_to_Post()
        index = 0
        for key in descriptions.keys():
            image_file = request.files[key]
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)

            slide = SlideModel(
                path=file_path,
                description=descriptions[key],
                fk_post_id=post_id,
                slide_index=index
            )
            db.add_slide(slide)
            index += 1

    return redirect(url_for('success'))

@application.route('/slides', methods=['GET'])
def get_slides():
    with InputManager() as db:
        slides = db.get_all_slides()
    return jsonify(slides)


if __name__ == '__main__':
    socketio.run(application, port=8000, debug=True, allow_unsafe_werkzeug=True)

