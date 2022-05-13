#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os
from typing import Optional

from pydantic import BaseModel

from models.Network.FirewallRule import FirewallRule
from models.Network.Rule import Rule
from models.Network.Subnetwork import Subnetwork, SimplifiedSubnetwork


class Network(BaseModel):
    """
    Network model
    Defines the structure of a network, independently of the provider
    """
    id: Optional[str] = None
    name: Optional[str] = 'network-' + os.urandom(4).hex()
    subnets: Optional[list[Subnetwork]] = None
    description: str = "network"
    firewalls: Optional[list[FirewallRule]] = [
        FirewallRule(
            name="allow-ssh",
            is_allow=True,
            rules=[
                Rule(
                    protocol="tcp",
                    from_ports=[22],
                    to_ports=[22],
                    source_networks=["0.0.0.0/0"],
                )
            ],
        )
    ]

    @staticmethod
    def from_aws_network(networks, **kwargs):
        nets = []
        for network in networks:
            nets.append(Network(
                id=network.id,
                name=network.description,
                subnet=Subnetwork.from_aws_network(network.id, **kwargs),
                firewall_rules=FirewallRule.from_aws_firewall(network.groups, **kwargs)
            ))
        return nets


class SimplifiedNetwork(BaseModel):
    name: str
    zone: str
    subnets: list[SimplifiedSubnetwork] = []
    description: str = "network"
    firewalls: Optional[list[FirewallRule]] = None



