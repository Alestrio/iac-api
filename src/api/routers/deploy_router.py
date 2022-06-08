#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), Alexis LEBEL, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from fastapi import APIRouter

from data.deployers import TerraformDeployer
from data.storage import TerraformStorage as storage

router = APIRouter(
    prefix="/deploy",
    responses={
        "200": {"description": "Successful deployment"},
        "400": {"description": "Bad request"},
        "404": {"description": "Not found"},
        "422": {"description": "Unprocessable entity"},
        "500": {"description": "Internal server error"},
    },
    tags=["Deployment"],
)


@router.post("/apply/{name}")
async def apply(name: str):
    """
    Deploys a machine with the given name.
    """
    available_configs = storage.get_all_config_names()
    if name in available_configs:
        TerraformDeployer.apply_config(name)
    else:
        raise ValueError("Config not found")
    return {"message": "Deployment of machine {} started".format(name)}


@router.post("/destroy/{name}")
async def destroy(name: str):
    """
    Destroys a machine with the given name.
    """
    available_configs = storage.get_all_config_names()
    if name in available_configs:
        TerraformDeployer.destroy_config(name)
    else:
        raise ValueError("Config not found")
    return {"message": "Destruction of machine {} started".format(name)}