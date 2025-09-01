import json
from datetime import datetime
from pathlib import Path
from pprint import pprint

from models.model_potholes import Pothole

from services.co_ordinate_conversion import xy2latlon, xy2irishgrid


async def write_data_to_db():
    json_files = Path('data').glob('*.json')
    for file in json_files:
        with open(f'{file}') as f:
            data = json.load(f)
            table_name = f'{data.keys()}'.split("'")[1]
            table_length = len(data[f'{table_name}']['Table'])
            print(f"table name: {table_name} table length: {table_length}")
            for i in range(table_length):

                status = data[f'{table_name}']['Table'][i]['DEFECT_STATUS']
                if status != 'Archive' and status != 'Completed':
                    instruction_reference = data[f'{table_name}']['Table'][i]['INSTRUCTION_REFERENCE']
                    defect_detail = data[f'{table_name}']['Table'][i]['DEFECT_DETAIL']
                    date_recorded = datetime.strptime(data[f'{table_name}']['Table'][i]['RECORDED_DATE'].split('T')[0],
                                                      '%Y-%m-%d')
                    easting = data[f'{table_name}']['Table'][i]['EASTING']
                    northing = data[f'{table_name}']['Table'][i]['NORTHING']
                    lat = xy2latlon(easting, northing)[0]
                    lon = xy2latlon(easting, northing)[1]
                    grid = xy2irishgrid(easting, northing)
                    pprint(
                        f'defect_detail: {defect_detail}, date_recorded: {date_recorded}, easting: {easting}, northing: {northing}, lat: {lat}, lon: {lon}, grid: {grid}, status: {status}')
                    pothole = Pothole(defect_detail=defect_detail,
                                      date_recorded=date_recorded,
                                      easting=easting, northing=northing,
                                      lat=lat, lon=lon, grid=grid, status=status,
                                      instruction_reference=instruction_reference)
                    await pothole.insert()
