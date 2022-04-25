#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import json

from fastapi import APIRouter

from data.providers.AWSProvider import AWSProvider
from data.providers.GCPProvider import GCPProvider

router = APIRouter(
    prefix="/existing",
    tags=["Existing infrastructure"],
    responses={
        200: {"description": "Successful operation"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)

providers = {
    "aws": AWSProvider,
    "gcp": GCPProvider,
}


@router.get("/{provider}")
async def get_existing_infrastructure(provider: str):
    """
    Get existing infrastructure
    """
    provider = providers.get(provider)
    # instantiate the provider
    provider_instance = provider()
    provider = provider_instance
    machines = provider.get_deployed_instances()
    return machines


@router.get("/machines/{provider}")
async def get_existing_machines(provider: str):
    """
    Get existing machines
    """
    provider = providers.get(provider)
    # instantiate the provider
    provider_instance = provider()
    provider = provider_instance
    machines = provider.get_machines()
    return machines
