#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Literal, Optional

from models.Network.Network import Network
from models.Network.Subnetwork import Subnetwork


class GCPNetwork(Network):
    zone: str = "europe-west1-b"
    subnetworks: Optional[list[Subnetwork]] = None
    description: str = "network"
    routing_type: Literal["REGIONAL", "GLOBAL"] = "REGIONAL"
    google_private_access: bool = False
    google_stream_journal: bool = False
    PROVIDER = "GCP"

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
            subnetworks=subnetworks,
            firewall_rules=list(firewalls),
        )
