from flask import render_template, request, redirect, url_for
from src.config import (PORT, STATIC_FOLDER_PATH, application)
from src.routes import leaderboard, engagement
from src.services.flask_socket import socketio, emit_carrousel_refresh
from src.services.db.input_manager import InputManager
from src.controllers.leaderboard_controller import get_leaderboard
import os
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


@application.route('/new-content', methods=["GET", "POST"])
def render_new_content():
    if request.method == 'POST':
        # Get form data
        image_name = request.form.get('image_name')
        client_name = request.form.get('client_name')
        image_file = request.files['image_file']
        # Ensure the 'static' folder exists, create it if not
        if not os.path.exists(STATIC_FOLDER_PATH):
            os.makedirs(STATIC_FOLDER_PATH)

        # Save the uploaded image file to the 'static' folder
        image_path = os.path.join(STATIC_FOLDER_PATH, image_file.filename)
        image_file.save(image_path)
        model = InputModel(
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


if __name__ == '__main__':
    # connect to database here

    # register routes
    application.register_blueprint(leaderboard, url_prefix='/leaderboards')
    application.register_blueprint(engagement, url_prefix="/engagement")
    # Run the Flask application with Socket.IO support
    socketio.run(application, port=PORT, debug=True, allow_unsafe_werkzeug=True)
