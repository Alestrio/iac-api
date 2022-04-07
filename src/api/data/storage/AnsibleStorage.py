#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os

import yaml


def get_available_role_files():
    """
    Get all available role files
    :return: list of available role files
    """
    return os.listdir("./config/ansible_configs/roles")


def save_ansible_playbook(playbook_name, playbook_content):
    """
    Save an ansible playbook to the filesystem
    :param playbook_name: name of the playbook
    :param playbook_content: content of the playbook
    :return: None
    """
    with open(os.path.join(os.path.dirname(__file__), "../../ansible_configs/{}.yaml".format(playbook_name)), "w") as playbook_file:
        playbook_file.write(playbook_content)


def get_config(name):
    """
    Get a config file from the filesystem
    :param name: name of the config file
    :return: content of the config file
    """
    with open("../../ansible_configs/{}.yaml".format(name), "r") as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)
