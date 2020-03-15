#!/usr/bin/python3


import modelos
from modelos.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
import sqlalchemy as db
from sqlalchemy.orm import relationship


class Servicio(Base):
     __tablename__ = 'servicios'
     servicio = Column(String(60), primary_key=True, nullable=False)
