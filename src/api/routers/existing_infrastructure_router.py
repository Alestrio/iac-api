#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), Alexis LEBEL, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import json

import googleapiclient
from fastapi import APIRouter, HTTPException

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


@router.get("/simple_machines/{provider}")
async def get_existing_simple_machines(provider: str):
    """
    Get existing machines
    """
    provider = providers.get(provider)
    # instantiate the provider
    provider_instance = provider()
    provider = provider_instance
    machines = provider.get_simple_machines()
    return machines


@router.get("/simple_networks/{provider}")
async def get_existing_simple_networks(provider: str):
    """
    Get existing networks
    """
    try:
        provider = providers.get(provider)
        # instantiate the provider
        provider_instance = provider()
        provider = provider_instance
        networks = provider.get_simple_networks()
        return networks
    except Exception as e:
        raise HTTPException(
            status_code=e.resp.status, detail=json.loads(e.content)["error"]
        )
