#!/usr/bin/python3

from api.v1.app import usertoken, confirm_token  #, mail
from flask_mail import Message

from api.v1.views import vistas
from flask import jsonify, abort, request
from modelos import storage
from modelos.hospital import Hospital
from modelos.paciente import Paciente
from modelos.medico import Medico

@vistas.route('/register', methods = ['POST'])
def sing_up():
    content = request.get_json()
    if content['usuario'] == 'hospital':
        hospital = Hospital(**content['formulario'])
        hospital.hash_password()
        storage.agregar(hospital)
        storage.save()
        mail_confirm = 'http://0.0.0.0:5000/api/v1/confirmar/'
        sk = str(usertoken(hospital.correo))
        mail_confirm = mail_confirm + sk
        
    elif content['usuario'] == 'paciente':
        paciente = Paciente(**content['formulario'])
        paciente.hash_password()
        storage.agregar(paciente)
        storage.save()
        mail_confirm = 'http://0.0.0.0:5000/api/v1/confirmar/'
        sk = str(usertoken(paciente.correo))
        mail_confirm = mail_confirm + sk
    else:
        return jsonify({"error":"usuario incorrecto"}), 400
    
    return jsonify({"status":mail_confirm})

@vistas.route('/confirmar/<token>')
def confirmar(token):
    try:
        email = confirm_token(token)
    except:
        pass
    usuario = storage.getbymail(email)
    try:
        usuario.activo = True
        usuario.save()
        return jsonify({"status": "OK"})
    except:
        return jsonify({"error":"link no valido"}), 400
