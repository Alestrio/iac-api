#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional

from pydantic import BaseModel

from models.Network.FirewallRule import FirewallRule
from models.Network.Subnetwork import Subnetwork, SimplifiedSubnetwork


class Network(BaseModel):
    """
    Network model
    Defines the structure of a network, independently of the provider
    """
    id: Optional[str] = None
    name: Optional[str] = None
    gcp_zone: Optional[str] = None
    aws_zone: str = "eu-west-1"
    subnet: Optional[Subnetwork] = None
    description: str = "network"
    routing_type: str = "static"
    mtu: int = 1500

    @staticmethod
    def from_google_network(response, subnetworks, firewalls):
        """
        Converts a Google network to a Network model
        :param firewalls:
        :param subnetworks:
        :param response: Google network response
        :return: Network model
        """
        return Network(
            id=response["id"],
            name=response["name"],
            subnet=subnetworks,
            firewall_rules=list(firewalls),
            #mtu=int(response["mtu"])
        )

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
    firewall_rules: Optional[list[FirewallRule]] = None



