#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional
import boto3

from pydantic import BaseModel, validator


class Disk(BaseModel):
    """
    That class represents a disk. It is independent of the provider.
    """
    id: Optional[str]
    type: str = "pd-standard"
    size: int = 10  # GB
    zone: Optional[str]
    name: Optional[str]

    @staticmethod
    def from_google_disk(google_dict: dict):
        """
        This method creates a Disk object from a Google disk.
        :param google_dict: Google disk dict
        :return: Disk object
        """
        return Disk(
            provider='gcp',
            type=google_dict['type'].split('/')[-1],
            size=google_dict['diskSizeGb'],
            name=google_dict['deviceName']
        )

    @staticmethod
    def from_aws_disk(response, **kwargs):
        """
        This method creates a Disk object from an AWS disk.
        :param response: AWS disk response
        :return: Disk object
        """
        ec2 = boto3.resource('ec2', region_name=kwargs['zone'], aws_access_key_id=kwargs['access_key'],
                             aws_secret_access_key=kwargs['secret_key'])
        disks = []
        for d in response:
            disk = ec2.Volume(d['Ebs']['VolumeId'])
            disks.append(Disk(
                id=disk.id,
                providers=['aws'],
                aws_type=disk.volume_type,
                size=disk.size,
                aws_zone=disk.availability_zone,
                name=disk.tags[0]['Value'] if disk.tags else 'a disk'
            ))
        return disks
