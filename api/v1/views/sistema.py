#!/usr/bin/python3

from api.v1.app import usertoken, confirm_token, app  #, mail
from flask_mail import Message

from api.v1.views import vistas
from flask import jsonify, abort, request, send_from_directory
from modelos import storage
from modelos.hospital import Hospital
from modelos.paciente import Paciente
from modelos.medico import Medico

from flask_jwt_extended import jwt_required, get_jwt_identity

import datetime

@vistas.route('/change_password', methods=['PUT'])
@jwt_required
def change_password():
    content = request.get_json()
    current_user = get_jwt_identity()
    old = content.get('old_password')
    new = content.get('new_password')
    usuario = storage.getbyid(current_user)
    autorizado = usuario.check_password(old)
    if not autorizado:
        return {'error': 'Password invalido'}, 401
    usuario.password = new
    usuario.hash_password()
    usuario.save()
    return {"status": "ok"}, 200

@vistas.route('/reset_password', methods=['PUT'])
def reset_password():
    content = request.get_json()
    usuario = storage.getbymail(content.get('correo'))
    access_token =  str(usertoken(hospital.correo))
    mail = 'http://0.0.0.0:5000/api/v1/reset/' + access_token
    return {"status": mail}

@vistas.route('/reset', methods=['PUT'])
def reset():
    try:
        email = confirm_token(token)
    except:
        pass
    usuario = storage.getbymail(email)
    content = request.get_json()
    try:
        usuario.password = content.get("new_password")
        usuario.hash_password()
        usuario.save()
        return jsonify({"status": "OK"})
    except:
        return jsonify({"error":"link no valido"}), 400

    
@vistas.route('/registrar_medico', methods = ['POST'])
@jwt_required
def registrar_medico():
    content = request.get_json()
    usuario = get_jwt_identity()
    autorizacion = storage.es_hospital(usuario)
    if not autorizacion:
        return {"error": "usuario no authorizado"}, 401

    formulario = content.get('formulario')
    medico = Medico(**content['formulario'])
    medico.hash_password()
    storage.agregar(medico)
    storage.save()
    return {"status": "ok"}, 200

@vistas.route('/registrar_observacion', methods = ['POST'])
@jwt_required
def registrar_observacion():
    content = request.get_json()
    usuario = get_jwt_identity()
    autorizacion = storage.es_medico(usuario)
    print(autorizacion)

    if not autorizacion:
        return {"error": "usuario no authorizado"}, 401
    
    formulario = content.get('formulario')
    medico = storage.getbyid(usuario)
    medico.registrar_observacion(formulario)
    return {"status": "observacion registrada"}

@vistas.route('/consultar/', methods = ['GET'])
def consultar_observaciones(id):
    observaciones = {}
    id_usuario = get_jwt_identity()
    usuario = storage.getbyid(id_usuario)
    observaciones = usuario.registro()
    if len(observaciones) > 0:
        return jsonify(observaciones), 200
    else:
        return {"status":"No tiene registros guardados"}, 201
    
@vistas.route("/descargar_consulta/<paciente_id>")
def get_csv(paciente_id):
    usuario = get_jwt_identity()
    autorizacion = storage.es_medico(usuario)
    if not autorizacion:
        return {"error": "usuario no authorizado"}, 401
    medico = storage.getbyid(usuario)
    filename = medico.descargar_registro(paciente_id)
    try:
        return send_from_directory("./", filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
