#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os
from jinja2 import Template


def store_terraform_infra(networks, machines, name=None):
    """
    Stores the machines in the Terraform state file.

    :param name:
    :param networks:
    :param machines: list of machines to store
    :return: None
    """
    if not name:
        name = os.urandom(16).hex()
    if not os.path.exists(f'./config/terraform_configs'):
        os.makedirs(f'./config/terraform_configs/')
    with open(f'./config/terraform_configs/{name}.tf', "w") as f:
        # generate jinja template
        template = Template(open('./templates/tf/locals.tf.j2', 'r').read(), trim_blocks=True, lstrip_blocks=True)
        # render template
        rendered_template = template.render(machines=machines)
        # write to file
        f.write(rendered_template)
        f.close()
    return True


def get_all_config_names():
    """
    Returns a list of all the terraform configs.

    :return: list of all the terraform configs
    """
    return os.listdir('./config/terraform_configs/')
