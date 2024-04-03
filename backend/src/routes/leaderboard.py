from flask import Blueprint
from src.controllers import create_leaderboard, get_leaderboard


leaderboard = Blueprint('leaderboard', __name__)

leaderboard.route('/', methods=['GET'])(create_leaderboard)
