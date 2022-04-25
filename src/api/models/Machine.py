#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import json
import os
from typing import Optional, Union

import requests
import yaml
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


class SimplifiedMachine(BaseModel):
    name: Optional[str]
    cpu: int = 0
    memory: int = 0
    type: str = "e2-micro"
    zone: str = "europe-west1-b"
    disks_number: int = 0
    os: str = "debian-10-buster-v20220310"

    def translateType(self):
        translateMachineType(self)


def translateMachineType(machine: Union[Machine, SimplifiedMachine]):
    with open('./config/app_config/app.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        gcp_instances_api = config['gcp_instances_api']
        aws_instances_api = config['aws_instances_api']
        aws_token = config['aws_token']

    if machine.type is None:
        return machine
    else:
        # Make a request and get all gcp instances
        gcp_instances = requests.get(gcp_instances_api)
        aws_instances = requests.get(aws_instances_api, headers={'Authorization': f'Bearer {aws_token}'})

        # filtering the gcp instances, deleting 'regions' dict items
        gcp_instances = json.loads(gcp_instances.text)
        filtered_instances = {}
        for supertype, gtype in gcp_instances.items():
            for key, subtype in gtype.items():
                try:
                    del subtype['regions']
                except:
                    pass
                filtered_instances[key] = subtype

        # formatting the aws instances
        filtered_aws_instances = {}
        for instance in aws_instances.json()['products']:
            key = instance['name']
            del instance['name']
            filtered_aws_instances[key] = instance

        # find the machine type
        instance_types = {
            'gcp': filtered_instances,
            'aws': filtered_aws_instances
        }
        for provider in instance_types.values():
            for key, instance in provider.items():
                if machine.type == key:
                    if instance.get('specs'):
                        machine.cpu = instance['specs']['cores']
                        machine.memory = instance['specs']['memory']
                    else:
                        machine.cpu = instance['details']['vcpu']
                        machine.memory = instance['details']['memory']
        return machine


if __name__ == '__main__':
    machine = SimplifiedMachine(name="test", type="t2.micro", zone="europe-west1-b", disks_number=1)
    machine.translateType()
    print(machine)
