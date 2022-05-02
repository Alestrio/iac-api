#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Literal

from models.Network.Network import Network


class GCPNetwork(Network):
    zone: str = "europe-west1-b"
    routing_type: Literal["REGIONAL", "GLOBAL"] = "REGIONAL"
    google_private_access: bool = False
    google_stream_journal: bool = False

    @staticmethod
    def from_google_network(response, subnetworks, firewalls):
        """
        Converts a Google network to a Network model
        :param firewalls:
        :param subnetworks:
        :param response: Google network response
        :return: Network model
        """
        return GCPNetwork(
            id=response["id"],
            name=response["name"],
            subnet=subnetworks,
            firewall_rules=list(firewalls),
        )
