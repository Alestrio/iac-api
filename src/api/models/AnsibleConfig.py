#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Union

import yaml
from pydantic import BaseModel


class AnsibleConfig(BaseModel):
    name: str
    roles: list[str]
    hosts: list[Union[str, dict]]
    remote_user: str
    become: bool

    def to_yaml(self):
        """
        Convert AnsibleConfig object to YAML string
        :return: YAML string
        """
        return yaml.dump(self.dict())

    @staticmethod
    def load_from_yaml(yaml_file):
        """
        Load AnsibleConfig object from YAML file
        :param yaml_file: YAML file path
        :return: AnsibleConfig object
        """
        with open(yaml_file, 'r') as stream:
            return AnsibleConfig(**yaml.load(stream, Loader=yaml.FullLoader))
