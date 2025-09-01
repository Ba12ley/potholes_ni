import os

from beanie import init_beanie
import motor.motor_asyncio
from models import model_potholes
from dotenv import load_dotenv

load_dotenv('.env')
conn_str = f"{os.environ['MONGODB_URL']}"


async def init_ni_potholes_db(conn_str):
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)
    await init_beanie(database=client.ni_potholes, document_models=[model_potholes.Pothole])
    return client