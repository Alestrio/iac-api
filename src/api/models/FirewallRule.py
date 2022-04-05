#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional, Union

from pydantic import BaseModel, validator

from models.Rule import Rule


class FirewallRule(BaseModel):
    name: Optional[str]
    allows: Optional[list[Rule]]
    denies: Optional[list[Rule]]
    target_tags: list[str] = []

    @validator("allows", "denies")
    def check_not_all_rules_are_empty(cls, rules: list, values):
        if not rules:
            raise ValueError("At least one rule must be specified")
        return rules
