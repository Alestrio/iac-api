#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os
from typing import Optional

import boto3
import requests
from pydantic import BaseModel

from models.Network.FirewallRule import FirewallRule


class Subnetwork(BaseModel):
    id: Optional[str]
    name: str = "subnet-" + os.urandom(4).hex()
    provider: str = 'gcp'
    ip_cidr_range: Optional[str] = '0.0.0.0/0'
    zone: Optional[str] = 'eu-west-1'

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
            ip_cidr_range=google_dict['ipCidrRange'],
            zone=google_dict['region'].split('/')[-1],
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
            zone=interface.subnet.availability_zone.split('-')[-1],
        )


class SimplifiedSubnetwork(BaseModel):
    name: str
    ip_cidr_range: str
    zone: str

    @staticmethod
    def from_subnetwork(subnet):
        return SimplifiedSubnetwork(
            name=subnet.name,
            ip_cidr_range=subnet.ip_cidr_range,
            zone=subnet.zone,
        )
