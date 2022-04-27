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
