import fastapi
import requests.exceptions
from beanie.odm.operators.find.comparison import In
from fastapi import status, HTTPException
from typing import List
from beanie import PydanticObjectId
from models.model_potholes import Pothole, reponse_model, error_response_model

router = fastapi.APIRouter()


@router.get('/api/all', response_description='All defects returned', status_code=status.HTTP_200_OK)
async def defects() -> List[Pothole]:
    defects = await Pothole.find_all().to_list()
    return defects


@router.get('/api/all/count', response_description='All defects count', status_code=status.HTTP_200_OK)
async def defects_count() -> int:
    total_defects = await Pothole.find_all().count()
    return total_defects


@router.get('/api/potholes', response_description='Potholes returned', status_code=status.HTTP_200_OK)
async def potholes() -> List[Pothole]:
    potholes = await Pothole.find(
        In(Pothole.defect_detail, ['ASPHALT POTHOLE (CAPH)', 'BITMAC POTHOLE (CBPH)'])).to_list()
    return potholes


@router.get('/api/potholes/count', response_description='Potholes returned', status_code=status.HTTP_200_OK)
async def potholes() -> int:
    total_potholes = await Pothole.find(
        In(Pothole.defect_detail, ['ASPHALT POTHOLE (CAPH)', 'BITMAC POTHOLE (CBPH)'])).count()
    return total_potholes


@router.get('/api/potholes/{ir}', response_description='Single pothole', status_code=status.HTTP_200_OK)
async def single_pothole(ir) -> Pothole:
    single_pothole_entry = await Pothole.find_one(Pothole.instruction_reference == ir)
    return single_pothole_entry


@router.get('/api/potholes/location/{current_position}',
            response_description='Potholes with in nearby area returned',
            status_code=status.HTTP_200_OK)
async def potholes_within_8km(current_position):
    try:
        boundary_size = 0.3
        lat_boundary = [float(current_position.split(',')[0]) + boundary_size,
                        float(current_position.split(',')[0]) - boundary_size]
        lon_boundary = [float(current_position.split(',')[1]) + boundary_size,
                        float(current_position.split(',')[1]) - boundary_size]
        potholes = await Pothole.find(
            In(Pothole.defect_detail, ['ASPHALT POTHOLE (CAPH)', 'BITMAC POTHOLE (CBPH)']),
            Pothole.status != 'Works Order Issued',
            Pothole.lat > lat_boundary[1], Pothole.lat < lat_boundary[0],
            Pothole.lon > lon_boundary[1], Pothole.lon < lon_boundary[0]
        ).to_list()
        return reponse_model(potholes, "Potholes data retrieved successfully")
    except requests.exceptions.ConnectionError:
        print('Unable to connect to database')
    except fastapi.exceptions.ResponseValidationError:
        print('Invalid input, use <lat>,<lon> format')
    except IndexError:
        print('Invalid input, use <lat>,<lon> format')

@router.get('/api/potholes/traveling/{current_position}',
            response_description='Potholes with in nearby area returned',
            status_code=status.HTTP_200_OK)
async def potholes_within_close_proximity(current_position):
    try:
        boundary_size = 0.01
        lat_boundary = [float(current_position.split(',')[0]) + boundary_size,
                        float(current_position.split(',')[0]) - boundary_size]
        lon_boundary = [float(current_position.split(',')[1]) + boundary_size,
                        float(current_position.split(',')[1]) - boundary_size]
        potholes = await Pothole.find(
            In(Pothole.defect_detail, ['ASPHALT POTHOLE (CAPH)', 'BITMAC POTHOLE (CBPH)']),
            Pothole.lat > lat_boundary[1], Pothole.lat < lat_boundary[0],
            Pothole.lon > lon_boundary[1], Pothole.lon < lon_boundary[0]
        ).to_list()
        return reponse_model(potholes, "Potholes data retrieved successfully")
    except requests.exceptions.ConnectionError:
        print('Unable to connect to database')
    except fastapi.exceptions.ResponseValidationError:
        print('Invalid input, use <lat>,<lon> format')
    except IndexError:
        print('Invalid input, use <lat>,<lon> format')