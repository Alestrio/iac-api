#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), Alexis LEBEL, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.

from fastapi import APIRouter

from data.storage import TerraformStorage as storage
from data.storage import AnsibleStorage as ansible_storage
from models.TerraformConfig import TerraformConfig
from models.AnsibleConfig import AnsibleConfig


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
async def create_config(config: TerraformConfig):
    """
    Create a terraform infra config file.
    """
    storage.store_terraform_infra(config)
    ansible_storage.save_ansible_playbook(AnsibleConfig(name=config.name, roles=config.roles))


@router.delete("/tf_config/{name}")
async def delete_config(name: str):
    """
    Delete a terraform infra config file.
    """
    return storage.delete_terraform_infra(name)


@router.get("/ansible_config/roles")
async def get_ansible_roles():
    """
    Get all ansible roles.
    """
    return ansible_storage.get_available_role_files()



