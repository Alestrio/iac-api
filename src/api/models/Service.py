#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from pydantic import BaseModel


class Service(BaseModel):
    name: str
    installation_playbook_path: str

    @staticmethod
    def get_from_name_in_config(name: str):
        pass  # TODO get_from_name_in_config

    # override of the equals method
    def __eq__(self, other: dict):
        return self.dict() == other

    def save_service_in_config(self):
        pass  # TODO save_service_in_config
