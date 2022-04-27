#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from fastapi import APIRouter

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


@router.post("/region/{provider}/{zone}")
async def set_region(provider: str, zone: str):
    """
    Set the region for a provider
    """
    provider = providers.get(provider)
    # instantiate the provider
    provider_instance = provider()
    provider = provider_instance
    # set the region
    provider.set_zone(zone)
    return {"message": "Region set"}


@router.get("/region/{provider}")
async def get_region(provider: str):
    """
    Get the region for a provider
    """
    provider = providers.get(provider)
    # instantiate the provider
    provider_instance = provider()
    provider = provider_instance
    # get the region
    return {"zone": provider.get_zone()}
