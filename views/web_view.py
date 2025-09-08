import json

import fastapi
from ipyleaflet import (
    Map, Marker, AwesomeIcon, Popup
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

    # Create markers for each point feature with popups
    for feature in data['features']:
        if feature['geometry']['type'] == 'Point':
            coords = feature['geometry']['coordinates']
            props = feature.get('properties', {})

            # Create popup content
            popup_html = f"""
            <div style="font-family: Arial, sans-serif;">
                <b>Reference:</b> {props.get('instruction_reference', 'N/A')}<br>
                <b>Detail:</b> {props.get('defect_detail', 'N/A')}<br>
                <b>Date:</b> {props.get('date_recorded', 'N/A')[:10]}<br>
                <b>Status:</b> {props.get('status', 'N/A')}<br>
                <b>Grid:</b> {props.get('grid', 'N/A')}
            </div>
            """

            icon = AwesomeIcon(name='warning', marker_color='red', icon_color='white')
            marker = Marker(
                location=(coords[1], coords[0]),  # GeoJSON is [lng, lat], Marker needs (lat, lng)
                icon=icon,
                title=props.get('instruction_reference', 'Pothole')  # Tooltip on hover
            )

            # Add popup
            popup = Popup(child=HTML(popup_html), max_width=300, min_width=200)
            marker.popup = popup

            m.add(marker)

    embed_minimal_html(filename, views=[m], title='Potholes NI')

    with open(filename, 'r') as f:
        return f.read()


@router.get('/', include_in_schema=False, response_class=HTMLResponse)
async def web_home_page(request: fastapi.Request):
    print(f'{request} Get request')
    map_file = make_map('templates/_map.html')
    return templates.TemplateResponse('web_view.html', {'request': request, 'map_file': map_file})
