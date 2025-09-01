import fastapi
import uvicorn
import os
import requests
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from db.database_mongo import init_ni_potholes_db
from services.parse_xml_to_json import parse_xml_to_dict
from services.json_to_model import write_data_to_db

from api_calls import potholes

load_dotenv('.env')
response = requests.get(os.environ['DATA_URL'], stream=True)
response.raise_for_status()
conn_str = f"{os.environ['MONGODB_URL']}"
with open(f'./data/current_year.xml', 'wb') as f:
    f.write(response.content)
print(f'File downloaded')

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    parse_xml_to_dict("./data/current_year.xml")
    await init_ni_potholes_db(conn_str)
    await write_data_to_db()
    print('Database Initialised')

    yield

    print('Database Shutdown')
api = fastapi.FastAPI(lifespan=lifespan)


def main():
    configure()
    uvicorn.run(api, host="0.0.0.0", port=8000)


def configure():
    api.include_router(potholes.router, tags=['potholes'])





if __name__ == '__main__':
    main()
else:
    configure()
