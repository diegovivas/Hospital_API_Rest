#!/usr/bin/python3


import modelos
from modelos.base_model import BaseModel, Base
from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from modelos.observaciones import Observacion
from modelos.paciente import Paciente
import csv
 

class Medico(BaseModel, Base):
    __tablename__ = 'medicos'
    especialidad = Column(String(60))
    hospital_id = Column(String(60), ForeignKey('hospitales.id'), nullable="False")
    observaciones = relationship("Observacion", backref="medico_")
    
    def registrar_observacion(self, formulario):
        registro = {}
        hospital = modelos.storage.getbyid(self.hospital_id)
        registro['paciente_id'] = formulario.get('paciente_id')
        registro['registro'] = formulario.get('registro')
        registro['especialidad'] = self.especialidad
        registro['hospital_id'] = self.hospital_id
        registro['medico_id'] = self.id
        registro['medico'] = self.nombre
        registro['hospital'] = hospital.nombre
        registro['id'] = self.hospital_id + formulario.get('paciente_id')
        observacion = Observacion(**registro)
        modelos.storage.agregar(observacion)
        modelos.storage.save()
        
        
    def registro(self):
        registros =  modelos.storage.query_registros()
        registros_propios = []
        for registro in registros:
            if registro.medico_id == self.id:
                registros_propios.append(registro.to_dict())
        return registros_propios

    def descargar_registro(self, paciente_id):
        paciente = modelos.storage.getbyid(paciente_id)
        registros = paciente.registro()
        print(registros)
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
