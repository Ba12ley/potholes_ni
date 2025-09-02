import datetime

from beanie import Document


class Pothole(Document):
    schema_version: str = 'version 0.1'
    defect_detail: str
    date_recorded: datetime.datetime
    easting: int
    northing: int
    lat: float
    lon: float
    grid: str
    status: str
    instruction_reference: str



    class Settings:
        name = 'pothole'
        indexes = [
            'date_recorded',
            'easting',
            'northing',
            'lat',
            'lon',
            'grid',
            'status',
            'instruction_reference',
        ]

    class Config:
        json_schema_extra = {
            'pothole': {
                'schema_version': 'version 0.1',
                'recorded_date': datetime.datetime.utcnow(),
                'easting': 123456.7,
                'northing': 123456.7,
                'lat': 123456.7,
                'lon': 123456.7,
                'grid': 'A 123456 123456',
                'status': 'COMPLETE',
            }
        }

def reponse_model(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

def error_response_model(error, code, message):
    return {"error": error, "code": code, "message": message}