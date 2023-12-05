from sqlalchemy import Column, Float, BigInteger, String, DateTime, Text, Integer, Boolean

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



class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)
    added_by = Column(String, nullable=False)
    added_on = Column(DateTime, default=datetime.utcnow)
    client_id = Column(Integer, nullable=False)
    full_address = Column(Text, nullable=False)
    service_rep = Column(String, nullable=False)
    email = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    updated_by = Column(String, nullable=True)
    updated_date = Column(DateTime, nullable=True)
    latitude = Column(Float, nullable=True)  # New field for latitude
    longitude = Column(Float, nullable=True)  # New field for longitude
    alert = Column(Boolean, default=False)  # Defaults to False (equivalent to 'no')
    radius = Column(Integer)  # New field for radius
    notification_sent = Column(Boolean, nullable=True, default=None)  # Defaults to null, not included in the endpoint
    notified_on = Column(DateTime, nullable=True, default=None)  # Date and time, defaults to null
