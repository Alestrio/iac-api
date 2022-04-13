#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.

from typing import Optional

import boto3
from pydantic import BaseModel, validator
from models.Network.Rule import Rule


class FirewallRule(BaseModel):
    name: Optional[str]
    is_allow: bool = True
    rules: Optional[list[Rule]] = None
    sranges: list[str] = ["0.0.0.0/0"]
    target_tags: list[str] = []

    @staticmethod
    def from_google_firewall(google_dict: dict):
        # TODO - implement
        pass

    @staticmethod
    def from_aws_firewall(groups, **kwargs):
        ec2 = boto3.resource('ec2', aws_access_key_id=kwargs['access_key'],
                             aws_secret_access_key=kwargs['secret_key'],
                             region_name=kwargs['zone'])
        rs = []
        for group in groups:
            rules = ec2.SecurityGroup(group['GroupId']).ip_permissions
            for rule in rules:
                r = Rule(
                    protocol=rule['IpProtocol'],
                    from_port=rule['FromPort'],
                    to_port=rule['ToPort'],
                    source_networks=[i['CidrIp'] for i in rule['IpRanges']],
                )
                rs.append(r)
        return [FirewallRule(
            name="default",
            is_allow=True,
            rules=rs,
            target_tags=[]
        )]
