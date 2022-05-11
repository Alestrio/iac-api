#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import json

import googleapiclient
from fastapi import APIRouter, HTTPException

from data.providers.AWSProvider import AWSProvider
from data.providers.GCPProvider import GCPProvider

router = APIRouter(
    prefix="/settings",
    responses={
        "200": {"description": "Successful deployment"},
        "400": {"description": "Bad request"},
        "404": {"description": "Not found"},
        "422": {"description": "Unprocessable entity"},
        "500": {"description": "Internal server error"},
    },
    tags=["Settings"],
)

providers = {
    "aws": AWSProvider,
    "gcp": GCPProvider,
}


@router.post("/zone/{provider}/{zone}")
async def set_zone(provider: str, zone: str):
    """
    Set the zone for a provider
    """
    provider = providers.get(provider)
    # instantiate the provider
    provider_instance = provider()
    provider = provider_instance
    # set the zone
    provider.set_zone(zone)
    return {"message": "Region set"}


@router.get("/zone/{provider}")
async def get_zone(provider: str):
    """
    Get the zone for a provider
    """
    provider = providers.get(provider)
    # instantiate the provider
    provider_instance = provider()
    provider = provider_instance
    # get the zone
    return {"zone": provider.get_zone()}


@router.get("/zones/{provider}")
async def get_available_zones(provider: str):
    """
    Get the available zones for a provider
    """
    provider = providers.get(provider)
    # instantiate the provider
    provider_instance = provider()
    provider = provider_instance
    # get the zones
    return {"zones": provider.get_available_zones()}


@router.get("/projects/{provider}")
async def get_available_projects(provider: str):
    """
    Get the available projects for a provider
    """
    try:
        provider = providers.get(provider)
        # instantiate the provider
        provider_instance = provider()
        provider = provider_instance
        # get the projects
        return {"projects": provider.get_available_projects()}
    except googleapiclient.errors.HttpError as e:
        raise HTTPException(
            status_code=e.resp.status, detail=json.loads(e.content)["error"]
        )


@router.get("/project/{provider}")
async def get_project(provider: str):
    """
    Get the project for a provider
    """
    try:
        provider = providers.get(provider)
        # instantiate the provider
        provider_instance = provider()
        provider = provider_instance
        # get the project
        return {"project": provider.get_project()}
    except googleapiclient.errors.HttpError as e:
        raise HTTPException(
            status_code=e.resp.status, detail=json.loads(e.content)["error"]
        )


@router.post("/project/{provider}/{project}")
async def set_project(provider: str, project: str):
    """
    Set the project for a provider
    """
    try:
        provider = providers.get(provider)
        # instantiate the provider
        provider_instance = provider()
        provider = provider_instance
        # set the project
        provider.set_project(project)
        return {"message": "Project set"}
    except googleapiclient.errors.HttpError as e:
        raise HTTPException(
            status_code=e.resp.status, detail=json.loads(e.content)["error"]
        )


@router.get("/forbidden_networks/{provider}")
async def get_forbidden_networks(provider: str):
    """
    Get the forbidden networks for a provider
    """
    try:
        provider = providers.get(provider)
        # instantiate the provider
        provider_instance = provider()
        provider = provider_instance
        # get the forbidden networks
        return {"forbidden_networks": provider.get_forbidden_networks()}
    except googleapiclient.errors.HttpError as e:
        raise HTTPException(
            status_code=e.resp.status, detail=json.loads(e.content)["error"]
        )


@router.get("/machine_types/{provider}")
async def get_machine_types(provider: str):
    """
    Get the machine types for a provider
    """
    try:
        provider = providers.get(provider)
        # instantiate the provider
        provider_instance = provider()
        provider = provider_instance
        # get the machine types
        return {"machine_types": provider.get_machine_types()}
    except googleapiclient.errors.HttpError as e:
        raise HTTPException(
            status_code=e.resp.status, detail=json.loads(e.content)["error"]
        )


@router.get("/machine_images/{provider}")
async def get_machine_images(provider: str):
    """
    Get the machine images for a provider
    """
    try:
        provider = providers.get(provider)
        # instantiate the provider
        provider_instance = provider()
        provider = provider_instance
        # get the machine images
        return {"machine_images": provider.get_machine_image_list()}
    except googleapiclient.errors.HttpError as e:
        raise HTTPException(
            status_code=e.resp.status, detail=json.loads(e.content)["error"]
        )

@router.get("/disk_types/{provider}")
async def get_disk_types(provider: str):
    """
    Get the disk types for a provider
    """
    try:
        provider = providers.get(provider)
        # instantiate the provider
        provider_instance = provider()
        provider = provider_instance
        # get the disk types
        return {"disk_types": provider.get_disk_types()}
    except googleapiclient.errors.HttpError as e:
        raise HTTPException(
            status_code=e.resp.status, detail=json.loads(e.content)["error"]
        )