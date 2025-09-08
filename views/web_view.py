import json

import fastapi
from ipyleaflet import (
    Map, GeoJSON, AwesomeIcon
)
from ipywidgets.embed import embed_minimal_html
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

router = fastapi.APIRouter()


def make_map(filename='map.html'):
    m = Map(center=(54.65, -6.9), zoom=8, scroll_wheel_zoom=True, touch_zoom=True, dragging=True, tap=True,
            tap_tolerance=15, world_copy_jump=False, close_popup_on_click=True, bounce_at_zoom_limits=True,
            keyboard=True, keyboard_pan_delta=80, keyboard_zoom_delta=1, inertia=True, inertia_deceleration=3000,
            inertia_max_speed=1500, zoom_control=True, attribution_control=True)
    with open('data/potholes.geojson') as f:
        data = json.load(f)

    pothole_icon = AwesomeIcon(name='warning', marker_color='orange')

    style = {
        "color": "red",
        "radius": 2,
        "fillColor": "red",
        "weight": 1,
        "opacity": 0.6,
        "fillOpacity": 0.6,
    }
    geo_json = GeoJSON(data=data, style=style, point_style=pothole_icon)
    m.geojson = geo_json
    m.add(geo_json)
    embed_minimal_html(filename, views=[m], title='Potholes NI')

    with open(filename, 'r') as f:
        return f.read()


@router.get('/', include_in_schema=False, response_class=HTMLResponse)
async def web_home_page(request: fastapi.Request):
    print(f'{request} Get request')
    map_file = make_map('templates/_map.html')
    return templates.TemplateResponse('web_view.html', {'request': request, 'map_file': map_file})
