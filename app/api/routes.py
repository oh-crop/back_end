from flask import jsonify, request, current_app, url_for
from . import api
from ..models import Plant

@api.route('/')
def endpoint():
    return "I need to go take a shower so I can't tell if I'm crying or not."
