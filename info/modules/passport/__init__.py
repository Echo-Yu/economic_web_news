from flask import Blueprint

passport_blue = Blueprint('passport', __name__, url_prefix='/possport')

from . import views