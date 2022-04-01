#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from pydantic import BaseModel

from models.Rule import Rule


class FirewallRule(BaseModel):
    project_id: str
    name: str
    network: str
    rules: list[Rule]
    target_tags: list[str]

    @staticmethod
    def get_from_name_in_config(name: str, config: dict) -> dict:
        """
        Gets the rule from the config file
        :param name:
        :param config:
        :return: None
        """
        pass  # TODO get_from_name_in_config

    # define the equal operator
    def __eq__(self, other: dict):
        """
        Overrides the default implementation
        :param other:
        :return:
        """
        return self.dict() == other

    def save_rule_in_config(self, config: dict) -> None:
        """
        Saves the rule in the config file
        :param config:
        :return: None
        """
        pass  # TODO save_rule_in_config

    def delete_rule_in_config(self, config: dict) -> None:
        """
        Deletes the rule in the config file
        :param config:
        :return: None
        """
        pass  # TODO delete_rule_in_config

    def update_rule_in_config(self, config: dict) -> None:
        """
        Updates the rule in the config file
        :param config:
        :return:
        """
        pass  # TODO update_rule_in_config
