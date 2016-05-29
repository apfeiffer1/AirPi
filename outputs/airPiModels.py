import netrc

import datetime

import sqlalchemy as sa

from sqlalchemy import event
from sqlalchemy.engine import Engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Time: 2015-08-14 08:31:04.336307
# Temperature: 37.1 C
# Pressure: 959.47 hPa
# Relative_Humidity: 30.0 %
# Light_Level: 417.515274949 Ohms
# Nitrogen_Dioxide: 13790.6976744 Ohms
# Carbon_Monoxide: 127333.333333 Ohms
# Volume: 716.129032258 mV

class AirPiData(Base):
    __tablename__ = 'airpidata'

    id0                = Column(Integer, primary_key=True)
    timeStamp          = Column(DateTime())
    Temperature        = Column(Float())
    Pressure           = Column(Float())
    Relative_Humidity  = Column(Float())
    Light_Level        = Column(Float())
    Nitrogen_Dioxide   = Column(Float())
    Carbon_Monoxide    = Column(Float())
    Volume             = Column(Float())

    def __init__(self, temp, pres, relH, light, no2, co, vol):
        self.timeStamp = datetime.datetime.now()
        self.Temperature        = temp
        self.Pressure           = pres
        self.Relative_Humidity  = relH
        self.Light_Level        = light
        self.Nitrogen_Dioxide   = no2
        self.Carbon_Monoxide    = co
        self.Volume             = vol

    def __repr__(self):
      return "<AirPiData instance: %s>\n" % self.__dict__


user,login,pwd = netrc.netrc().authenticators('postgres')
engine = create_engine('postgresql://pi:%s@rpi2-0.local/airpi' % pwd, echo=False)
session = sessionmaker(bind=engine)

session.configure(bind=engine)

Base.metadata.create_all(engine)
