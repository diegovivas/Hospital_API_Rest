#!/usr/bin/python3
"""
se encuentran las clases encargadas
de registrar y confirmar un usuario.
"""
from api.v1.app import usertoken, confirm_token, mail
from flask_mail import Message

from api.v1.views import vistas
from flask import jsonify, abort, request
from modelos import storage
from modelos.hospital import Hospital
from modelos.paciente import Paciente
from modelos.medico import Medico

@vistas.route('/register', methods = ['POST'])
def sing_up():
    """
    crea una instancia de un usuario
    dependiendo de su tipo y la guarda
    en la base de datos.
    """
    content = request.get_json()
    if content is None:
            abort(400, 'Not es un JSON')
    usuario = content.get("usuario")
    usuario_id = content.get('formulario').get('id')
    if not storage.verificar_id(usuario_id):
            return jsonify({"error": "id invalido"}), 401
    correo = content.get('formulario').get('correo')
    msg = Message(recipients=[correo])
    if not storage.verificar_correo(correo):
            return jsonify({"error": "correo invalido"}), 401
    servicios = content.get("servicios")
    if usuario == 'hospital':
        if len(servicios) < 1:
            return jsonify({"error": "debe registrar servicios"}), 401
        hospital = Hospital(**content['formulario'])
        hospital.hash_password()
        storage.agregar(hospital)
        storage.agregar_servicios(servicios, hospital)
        storage.save()
        mail_confirm = 'http://0.0.0.0:5000/api/v1/confirmar/'
        sk = str(usertoken(hospital.correo))
        mail_confirm = mail_confirm + sk
        
    elif usuario == 'paciente':
        if len(content.get('formulario').get('fecha_nacimiento')) < 1:
            return jsonify({"error": "debe poner fecha de nacimientoo"}), 401
        paciente = Paciente(**content['formulario'])
        paciente.hash_password()
        storage.agregar(paciente)
        storage.save()
        mail_confirm = 'http://0.0.0.0:5000/api/v1/confirmar/'
        sk = str(usertoken(paciente.correo))
        mail_confirm = mail_confirm + sk
    else:
        return jsonify({"error":"usuario incorrecto"}), 400
    texto_mensaje = "<p>Hola gracias por registrarte<p></br>"
    texto_mensaje += '<a href="'+mail_confirm+'">Confirma tu registro.</a></br>'
    msg.subject = "Confirmar registro"
    msg.html = texto_mensaje
    mail.send(msg)
    return jsonify({"status":"OK"}), 201

@vistas.route('/confirmar/<token>')
def confirmar(token):
    """
    funcion para verificar un registro por email.
    """
    try:
        email = confirm_token(token)
    except:
        pass
    usuario = storage.getbymail(email)
    print(email)
    usuario.activo = True
    usuario.save()
    return jsonify({"status": "OK"})

"""
    try:
        usuario.activo = True
        usuario.save()
        return jsonify({"status": "OK"})
    except:
        return jsonify({"error":"link no valido"}), 400
"""
