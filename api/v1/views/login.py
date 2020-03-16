#!/usr/bin/python3
"""
login para permitir acceso al sistema
de un usuario.
"""
from api.v1.app import usertoken, confirm_token  #, mail
from flask_mail import Message

from api.v1.views import vistas
from flask import jsonify, abort, request
from modelos import storage
from modelos.hospital import Hospital
from modelos.paciente import Paciente
from modelos.medico import Medico

from flask_jwt_extended import create_access_token

import datetime

@vistas.route('/login', methods = ['POST'])
def login():
    
    content = request.get_json()
    
    if content is None:
            abort(400, 'Not es un JSON')
            
    id = content.get('id')
    password = content.get('password')
    
    usuario = storage.getbyid(id)
    
    autorizado = usuario.check_password(password)
    
    if not autorizado:
        return {'error': 'Usuario o password invalidos'}, 401
    
    if not usuario.activo:
        if usuario.__class__.__name__ == "Medico":
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(usuario.id),
                                               expires_delta=expires)
            return jsonify({"http://0.0.0.0:5000/api/v1/change_password": access_token}), 201
        return {'error': 'Debes confirmar tu registro primero'}, 401
    
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(usuario.id), expires_delta=expires)
    
    return jsonify({str(usuario.__class__.__name__): access_token})

