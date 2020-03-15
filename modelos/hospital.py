#!/usr/bin/python3


import modelos
from modelos.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

servicios_hospital = Table('servicios_hospital', Base.metadata,
                          Column('hospital_id', String(60),
                                 ForeignKey('hospitales.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('servicio_id', String(60),
                                 ForeignKey('servicios.servicio', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))

class Hospital(BaseModel, Base):
     __tablename__ = 'hospitales'
     medicos = relationship("Medico", backref="hospital_med")
     medico_observaciones = relationship("Observacion", backref="hospital_ob")
     pacientes = relationship("Paciente", backref="hospital_paci")
     servicios = relationship("Servicio", secondary="servicios_hospital",
                             backref="hospital", viewonly=False)
    
     def registro(self):
          registros =  modelos.storage.query_registros()
          registros_propios = []
          for registro in registros:
               if registro.hospital_id == self.id:
                    registros_propios.append(registro.to_dict())
          return registros_propios
