#!/usr/bin/python3

from flask import Blueprint

vistas = Blueprint('vistas', __name__, url_prefix='/api/v1')

from api.v1.views.register import *
from api.v1.views.login import *
from api.v1.views.sistema import *
