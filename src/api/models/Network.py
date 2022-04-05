#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional

from pydantic import BaseModel

from models.FirewallRule import FirewallRule


class Network(BaseModel):
    """
    Network model
    Defines the structure of a network, independently of the provider
    """
    id: Optional[str] = None
    name: Optional[str] = None
    gcp_zone: str = "europe-west1"
    aws_zone: str = "eu-west-1"
    subnet: str = ""
    description: str = "network"
    firewall_rules: list[FirewallRule]
    routing_type: str = "static"
    mtu: int = 1500
