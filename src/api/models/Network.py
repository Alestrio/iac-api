#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from pydantic import BaseModel

from models.FirewallRule import FirewallRule


class Network(BaseModel):
    """
    Network model
    Defines the structure of a network, independently of the provider
    """
    id: str
    name: str
    region: str
    zone: str
    subnet: str
    description: str
    firewall_rules: list[FirewallRule]
    routing_type: str
    mtu: int
