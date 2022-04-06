#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from pydantic.main import BaseModel


class Rule(BaseModel):
    """
    Abstract class for rules
    A rule is a simple instruction to deny or allow traffic on a network port
    """
    protocol: str = "tcp"
    ports: list[int] = [80]
    source_networks: list[str] = ["0.0.0.0/0"]