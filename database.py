import asyncio
from datetime import datetime
import socket
from tortoise import Tortoise, fields
from tortoise.models import Model

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

async def write_to_postgres(pos_msg):
    await Tortoise.init(
        db_url=f"postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        modules={'models': ['__main__']},
    )
    await Tortoise.generate_schemas()
    await Position.create(
        device_id=int(pos_msg["imei"]),
        fix_time=pos_msg["fix_time"],
        position={"type": "Point", "coordinates": [pos_msg["lon"], pos_msg["lat"]]},
        speed=pos_msg["speed"],
        course=pos_msg["course"],
    )

async def handle_gt06_data(data, addr):
    gt06_msg = {"fix_time": datetime.utcnow()}  # Modify this based on your GT06 message format
    # Process the raw GT06 message and extract relevant information

    await write_to_postgres(gt06_msg)

async def esp_tracker_server():
    esp_tracker_server_port = 64458
    server = await asyncio.start_server(
        handle_gt06_data, '0.0.0.0', esp_tracker_server_port
    )
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_gt06_data, '0.0.0.0', 64458, loop=loop)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
