#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional

from pydantic import BaseModel

from models.Rule import Rule


class FirewallRule(BaseModel):
    name: Optional[str]
    rules: list[Rule]
    target_tags: list[str] = []
