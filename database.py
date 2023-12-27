# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker



# from urllib.parse import quote_plus

# # Original password
# raw_password = "Cr!st0V!v3J3susS@lvA2023!"

# # URL-encode the password
# encoded_password = quote_plus(raw_password)

# # Construct the database URL with the encoded password
# SQLALCHEMY_DATABASE_URL = f"postgresql://gpstracker2:{encoded_password}@localhost/raw_data_db"



# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # Prod 
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from urllib.parse import quote_plus

# # New database credentials
# username = "postgres"
# password = "Josiah1!"
# host = "localhost"
# port = "5432"
# database = "django"
# sslmode = "require"

# # URL-encode the password
# encoded_password = quote_plus(password)

# # Construct the database URL with the encoded password and the new credentials
# SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{encoded_password}@{host}:{port}/{database}?sslmode={sslmode}"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




from fastapi import FastAPI
import asyncio
import socket
import json
from datetime import datetime
from pydantic import BaseModel
from tortoise import Tortoise, fields
from tortoise.models import Model
from tortoise.transactions import atomic

# Configure your PostgreSQL database
DB_USERNAME = "postgres"
DB_PASSWORD = "Josiah1!"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "django"

# Define the Position model
class Position(Model):
    id = fields.IntField(pk=True)
    device_id = fields.IntField()
    fix_time = fields.DatetimeField(null=True)
    position = fields.JSONField()
    speed = fields.FloatField()
    course = fields.FloatField()

# Initialize Tortoise for asynchronous ORM
Tortoise.init(
    db_url=f"postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    modules={'models': ['__main__']},
)

app = FastAPI()

class GT06Message(BaseModel):
    imei: str
    lat: float
    lon: float
    fix_time: datetime
    speed: float
    course: float

async def write_to_postgres(pos_msg: GT06Message):
    await Tortoise.init(
        db_url=f"postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        modules={'models': ['__main__']},
    )
    await Tortoise.generate_schemas()
    await Position.create(
        device_id=int(pos_msg.imei),
        fix_time=pos_msg.fix_time,
        position={"type": "Point", "coordinates": [pos_msg.lon, pos_msg.lat]},
        speed=pos_msg.speed,
        course=pos_msg.course,
    )

async def handle_gt06_data(data: str):
    gt06_msg = json.loads(data)
    gt06_msg["fix_time"] = datetime.fromtimestamp(gt06_msg["fixTimestamp"])
    await write_to_postgres(GT06Message(**gt06_msg))

async def esp_tracker_server():
    esp_tracker_server_port = 64458
    server = await asyncio.start_server(
        handle_gt06_data, '0.0.0.0', esp_tracker_server_port
    )
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(esp_tracker_server())


