from flask import Blueprint
from src.controllers import create_engagement_report


engagement = Blueprint('engagement', __name__)

engagement.route('/', methods=["POST"])(create_engagement_report)
