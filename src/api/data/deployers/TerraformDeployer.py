#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from python_terraform import Terraform


def apply_config(config):
    """
    Apply the configuration to the Terraform infrastructure
    :param config: the configuration to apply
    :return:
    """
    t = Terraform(working_dir='./config/terraform_configs/{}'.format(config), is_env_vars_included=True)
    t.init()
    t.cmd('apply', '-auto-approve')


def destroy_config(config):
    """
    Destroy the configuration to the Terraform infrastructure
    :param config: the configuration to destroy
    :return:
    """
    t = Terraform(working_dir='./config/terraform_configs/{}'.format(config), is_env_vars_included=True)
    t.init()
    t.cmd('destroy', '-auto-approve')