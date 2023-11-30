from sqlalchemy import Column, Float, BigInteger, String, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RawData(Base):
    __tablename__ = 'raw_data'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    timestamp = Column(BigInteger, nullable=True)
    hdop = Column(String, nullable=True)
    altitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    raw_data = Column(Text, nullable=True)  # Field to store raw data
    created_at = Column(DateTime, default=datetime.utcnow)
