#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from fastapi import APIRouter
from src.api import providers

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


@router.get("/{provider}", response_model=str)
async def get_existing_infrastructure(provider: str):
    """
    Get existing infrastructure
    """
    provider = providers.get(provider)
    # instantiate the provider
    provider_instance = provider()
    provider = provider_instance
