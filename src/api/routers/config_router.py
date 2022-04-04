#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from fastapi import APIRouter

from data.storage import TerraformStorage
from models.Machine import Machine


router = APIRouter(
    prefix="/config",
    tags=["Configs"],
    responses={
        200: {"description": "Successful operation"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)

@router.post("/terraform_infra")
async def create_config(machines: list[Machine]):
    """
    Create a terraform infra config file.
    """
    return TerraformStorage.store_terraform_infra(None, machines)

