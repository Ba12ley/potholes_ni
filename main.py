import fastapi
import uvicorn
import os
from beanie.odm import views
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from pathlib import Path
from db.database_mongo import init_ni_potholes_db

import views.web_view
from api_calls import potholes

load_dotenv('.env')
conn_str = f"{os.environ['MONGODB_URL']}"


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    geojson_file = Path("data/potholes.geojson")

    try:
        client = await init_ni_potholes_db(conn_str)
        print("Database initialized")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        client = None
    if geojson_file.exists():
        print("GeoJSON file already exists, skipping initialization")
    else:
        print("GeoJSON file not found, run initialization")

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
