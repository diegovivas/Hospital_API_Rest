#!/usr/bin/python3
"""
clase medico hereda de BaseModel y Base
"""

import modelos
from modelos.base_model import BaseModel, Base
from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from modelos.observaciones import Observacion
from modelos.paciente import Paciente
from uuid import uuid4, UUID
import csv
 

class Medico(BaseModel, Base):
    """
    atributos y metodos de la clase Medico.
    """
    __tablename__ = 'medicos'
    especialidad = Column(String(60))
    hospital_id = Column(String(60), ForeignKey('hospitales.id'), nullable="False")
    observaciones = relationship("Observacion", backref="medico_")
    
    def registrar_observacion(self, formulario):
        """
        registra observacion de un paciente recibe
        como parametro formulario, que es un 
        diccionario con las claves, paciente_id
        y registro.
        """
        registro = {}
        hospital = modelos.storage.getbyid(self.hospital_id)
        registro['paciente_id'] = formulario.get('paciente_id')
        registro['registro'] = formulario.get('registro')
        registro['especialidad'] = self.especialidad
        registro['hospital_id'] = self.hospital_id
        registro['medico_id'] = self.id
        registro['medico'] = self.nombre
        registro['hospital'] = hospital.nombre
        registro['id'] = str(uuid4())
        observacion = Observacion(**registro)
        modelos.storage.agregar(observacion)
        modelos.storage.save()
        
        
    def registro(self):
        """
        retorna una lista con los registros
        que ha realizado el medico.
        """
        registros =  modelos.storage.query_registros()
        registros_propios = []
        for registro in registros:
            if registro.medico_id == self.id:
                registros_propios.append(registro.to_dict())
        return registros_propios

    def descargar_registro(self, paciente_id):
        """
        guarda un registro en formato csv para que 
        el metodo de flask pueda retornarlo a partir 
        de su ubicacion en el disco, retorna el nombre
        del archivo.
        """
        paciente = modelos.storage.getbyid(paciente_id)
        registros = paciente.registro()
        n_registro = paciente.id + ".csv" 
        with open(n_registro, 'w') as f:
            writer = csv.writer(f)
            writer.writerow( ('Hospital', 'Medico', 'Especialidad', 'Registro') )
            for registro in registros:
                writer.writerow( (registro.get('hospital'),
                                  registro.get('medico'),
                                  registro.get('especialidad'),
                                  registro.get('registro')) )
        return n_registro
