import fastapi
import uvicorn
import os
from beanie.odm import views
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import asyncio
from db.database_mongo import init_ni_potholes_db
from services.make_geojson import export_potholes_to_geojson
import views.web_view
from api_calls import potholes

load_dotenv('.env')
conn_str = f"{os.environ['MONGODB_URL']}"


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    try:
        client = await init_ni_potholes_db(conn_str)
        print("Database initialized")


    except Exception as e:
        print(f"Failed to initialize database: {e}")
        client = None

    yield

    if client:
        asyncio.create_task(export_potholes_to_geojson())
        print("GeoJSON export scheduled")

    # --- Shutdown ---
    if client:
        client.close()
        print("Database shutdown")


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
