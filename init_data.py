import asyncio
import requests
import os
from pathlib import Path
from services.parse_xml_to_json import parse_xml_to_dict
from services.json_to_model import write_data_to_db

from db.database_mongo import init_ni_potholes_db
from dotenv import load_dotenv

load_dotenv('.env')
response = requests.get(os.environ['DATA_URL'], stream=True)
response.raise_for_status()
conn_str = f"{os.environ['MONGODB_URL']}"
with open(f'./data/current_year.xml', 'wb') as f:
    f.write(response.content)
print(f'File downloaded')


async def initialize_data():
    geojson_file = Path("data/potholes.geojson")

    if not geojson_file.exists():
        print("Initializing data...")
        parse_xml_to_dict("./data/current_year.xml")
        client = await init_ni_potholes_db(conn_str)
        await write_data_to_db()

        client.close()
        print("Data initialization complete")
    else:
        print("Data already initialized")


if __name__ == "__main__":
    asyncio.run(initialize_data())
