import json
from pathlib import Path
from models.model_potholes import Pothole
from beanie.odm.operators.find.comparison import In

async def export_potholes_to_geojson(filepath: str = "data/potholes.geojson"):
    potholes = await Pothole.find(
        In(Pothole.defect_detail, ['ASPHALT POTHOLE (CAPH)', 'BITMAC POTHOLE (CBPH)'])).to_list()

    features = []
    for p in potholes:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [p.lon, p.lat],
            },
            "properties": {
                "instruction_reference": p.instruction_reference,
                "defect_detail": p.defect_detail,
                "date_recorded": p.date_recorded.isoformat(),
                "status": p.status,
                "easting": p.easting,
                "northing": p.northing,
                "grid": p.grid,
            },
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    Path(filepath).write_text(json.dumps(geojson, indent=2))
    print(f"GeoJSON exported to {filepath}")
