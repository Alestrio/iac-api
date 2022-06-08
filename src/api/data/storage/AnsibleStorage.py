#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), Alexis LEBEL, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os

import yaml
from jinja2 import Template

from models.AnsibleConfig import AnsibleConfig


def get_available_role_files():
    """
    Get all available role files
    :return: list of available role files
    """
    return os.listdir("./config/ansible_configs/roles")


def render_content_templates(config: AnsibleConfig):
    """
    Renders the content templates for the given config.

    :param config: the config to render
    :return: None
    """
    content = ""
    with open(f'./templates/ansible_config.yaml.j2', 'r') as f:
        template = Template(f.read(), trim_blocks=True, lstrip_blocks=True)
        rendered_template = template.render(config=config)
        content += rendered_template
    return content


def save_ansible_playbook(config: AnsibleConfig):
    """
    Save an ansible playbook to the filesystem
    :param config:
    :param playbook_name: name of the playbook
    :return: None
    """
    with open("./config/ansible_configs/{}.yaml".format(config.name), "w") as playbook_file:
        # Open the template file generate
        playbook_file.write(render_content_templates(config))


def get_config(name):
    """
    Get a config file from the filesystem
    :param name: name of the config file
    :return: content of the config file
    """
    with open("../../ansible_configs/{}.yaml".format(name), "r") as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)
