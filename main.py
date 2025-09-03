import fastapi
import uvicorn
import os
import requests
import gc
from beanie.odm import views
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from pathlib import Path
from db.database_mongo import init_ni_potholes_db
from services.parse_xml_to_json import parse_xml_to_dict
from services.json_to_model import write_data_to_db
from services.make_geojson import export_potholes_to_geojson
import views.web_view
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
    geojson_file = Path("data/potholes.geojson")

    if not geojson_file.exists():
        print("GeoJSON file not found, initializing database...")
        parse_xml_to_dict("./data/current_year.xml")
        client = await init_ni_potholes_db(conn_str)
        await write_data_to_db()
        print('Database Initialised')
        await export_potholes_to_geojson()
        collected = gc.collect()
        print(f'Garbage collected {collected} objects')
        gc.collect()
    else:
        print("GeoJSON file already exists, skipping initialization")
        # Still need to initialize the client for the app to work
        client = await init_ni_potholes_db(conn_str)

    yield

    print('Database Shutdown')
    client.close()
api = fastapi.FastAPI(lifespan=lifespan)


def main():
    configure()
    uvicorn.run(api, host="0.0.0.0", port=8000)


def configure():
    api.include_router(potholes.router, tags=['potholes'])
    api.include_router(views.web_view.router, tags=['web_view'])





if __name__ == '__main__':
    main()
else:
    configure()
