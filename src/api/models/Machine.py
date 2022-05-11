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
    Machine model
    This model is used to represent a machine for any provider.
    """
    name: Optional[str]
    providers: str = 'gcp'
    type: Optional[str] = "t2.micro"
    machine_image: str = "ami-0f9c9d7f2b6c8f9d6"
    zone: str = "europe-west1-b"
    network: str = "default"
    subnetwork: str = "default"
    addresses: Address = Address(name=f"machine-address-{os.urandom(4).hex()}")
    disks: list[Disk]
    has_public_ip: bool = False
    http_access: bool = False
    https_access: bool = False


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
