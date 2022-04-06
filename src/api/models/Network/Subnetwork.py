#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional

from pydantic import BaseModel


class Subnetwork(BaseModel):
    name: str
    network_name: str
    providers: list[str] = ['gcp']
    ip_cidr_range: Optional[str]
    gcp_region: Optional[str]
    aws_region: Optional[str]

    @staticmethod
    def from_google_subnetwork(google_dict):
        """

        :param google_dict:
        :return:
        """
        return Subnetwork(
            name=google_dict['name'],
            network_name=google_dict['network'].split('/')[-1],
            ip_cidr_range=google_dict['ipCidrRange'],
            gcp_region=google_dict['region'].split('/')[-1]
        )
