import json

import fastapi
import requests
from beanie.odm.operators.find.comparison import In
from ipyleaflet import Map, GeoJSON
from ipywidgets.embed import embed_minimal_html
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.model_potholes import Pothole

templates = Jinja2Templates(directory='templates')

router = fastapi.APIRouter()


def make_map(filename='map.html'):
    m = Map(center=(54.65,-6.9), zoom=8)
    with open('data/potholes.geojson') as f:
        data = json.load(f)

    style = {
        "color": "red",
        "radius": 2,
        "fillColor": "red",
        "weight": 1,
        "opacity": 0.6,
        "fillOpacity": 0.6,
    }
    geo_json = GeoJSON(data=data, style=style)
    m.add(geo_json)
    embed_minimal_html(filename, views=[m],  title='Potholes NI')

    with open(filename, 'r') as f:
        return f.read()

@router.get('/', include_in_schema=False, response_class=HTMLResponse)
async def web_home_page(request: fastapi.Request):
    print(f'{request} Get request')
    map_file = make_map('templates/_map.html')
    return templates.TemplateResponse('web_view.html', {'request': request, 'map_file': map_file})
