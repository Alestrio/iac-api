#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.

from typing import Optional
from pydantic import BaseModel, validator
from models.Network.Rule import Rule


class FirewallRule(BaseModel):
    name: Optional[str]
    is_allow: bool = True
    rules: Optional[list[Rule]] = None
    target_tags: list[str] = []

    @staticmethod
    def from_google_firewall(google_dict: dict):
        # TODO - implement
        pass
