#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os
from typing import Optional, Union

from pydantic import BaseModel

from models.Disk import Disk
from models.Network.Address import Address
from models.Network.Network import Network


class Machine(BaseModel):
    """
    :param disks: List of Disk objects, disks to be attached to the machine
    :param providers: List of provider names, providers to be used for the machine
    :param gcp_zone: Zone of the GCP machine, default is us-central1-a
    :param aws_zone: Zone of the AWS machine, default is eu-west-3
    :param gcp_network: Network of the GCP machine, default is "default"
    :param aws_network: Network of the AWS machine, default is empty
    :param gcp_machine_type: Machine type, default is e2-micro
    :param aws_machine_type: Machine type, default is t2.micro
    :param gcp_machine_image: The image to use for the GCP machine, default is debian-10-buster-v20200101
    :param aws_machine_image: The image to use for the AWS machine, default is a debian 9 stretch image
    :param cpu: The number of CPUs to allocate to the machine, default is 0, using the machine type
    :param memory: The amount of memory to allocate to the machine, default is 0, using the machine type
    :param machine_name: The name of the machine, default is "machine"
    """

    name: Optional[str]
    providers: list[str] = ['gcp']
    cpu: int = 0
    memory: int = 0
    gcp_type: Optional[str] = "e2-micro"
    aws_type: Optional[str] = "t2.micro"
    gcp_machine_image: str = "debian-10-buster-v20220310"
    aws_machine_image: str = "ami-0f9c9d7f2b6c8f9d6"
    gcp_zone: str = "europe-west1-b"
    aws_zone: str = "eu-west-1a"
    gcp_network: Optional[Union[Network, str]] = "default"
    aws_network: str = "default"
    address: Address = Address(name=f"machine-address-{os.urandom(4).hex()}")
    disks: list[Disk]
