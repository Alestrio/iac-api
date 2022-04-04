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

from data.storage import TerraformStorage as storage
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


@router.get("/tf_configs")
async def get_tf_configs_names():
    """
    Get all terraform infra config files.
    """
    return storage.get_all_config_names()


@router.post("/tf_config")
async def create_config(machines: list[Machine]):
    """
    Create a terraform infra config file.
    """
    return storage.store_terraform_infra(None, machines)

