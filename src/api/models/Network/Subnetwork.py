#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional

import boto3
import requests
from pydantic import BaseModel

from models.Network.FirewallRule import FirewallRule


class Subnetwork(BaseModel):
    id: Optional[str]
    name: str
    providers: list[str] = ['gcp']
    ip_cidr_range: Optional[str]
    gcp_region: Optional[str]
    aws_region: Optional[str]

    @staticmethod
    def from_google_subnetwork(google_dict):
        """
        :param firewall_rules:
        :param google_dict:
        :return:
        """
        #print(google_dict)
        return Subnetwork(
            name=google_dict['name'],
            network_name=google_dict['network'].split('/')[-1],
            ip_cidr_range=google_dict['ipCidrRange'],
            gcp_region=google_dict['region'].split('/')[-1],
        )

    @staticmethod
    def from_aws_network(net_id, **kwargs):
        ec2 = boto3.resource('ec2', aws_access_key_id=kwargs['access_key'],
                             aws_secret_access_key=kwargs['secret_key'],
                             region_name=kwargs['zone'])
        interface = ec2.NetworkInterface(net_id)
        return Subnetwork(
            name="default",
            network_name=interface.description,
            ip_cidr_range=interface.subnet.cidr_block,
            aws_region=interface.subnet.availability_zone.split('-')[-1],
        )


class SimplifiedSubnetwork(BaseModel):
    name: str
    ip_cidr_range: str
    region: str

    @staticmethod
    def from_subnetwork(subnet):
        return SimplifiedSubnetwork(
            name=subnet.name,
            ip_cidr_range=subnet.ip_cidr_range,
            region=subnet.gcp_region,
        )
