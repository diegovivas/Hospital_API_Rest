#!/usr/bin/python3


import modelos
from modelos.base_model import BaseModel, Base
from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from datetime import datetime


class Paciente(BaseModel, Base):
    __tablename__ = 'pacientes'
    fecha_nacimiento = Column(String(60))
    hospital_id = Column(String(60), ForeignKey('hospitales.id'), nullable="False")
    observaciones = relationship("Observacion", backref="paciente")
    
    def registro(self):
        registros =  modelos.storage.query_registros()
        registros_propios = []
        for registro in registros:
            if registro.paciente_id == self.id:
                registros_propios.append(registro.to_dict())
        return registros_propios
