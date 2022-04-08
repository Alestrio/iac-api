#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os

from pydantic import BaseModel

from models.Machine import Machine
from models.Network.Network import Network


class TerraformConfig(BaseModel):
    name: str = os.urandom(8).hex()
    project_id: str
    gcp_region: str = "europe-west1"
    aws_region: str = "eu-west-1"
    ssh_user: str = "ubuntu"
    private_key_name: str = "sample-key"
    machines: list[Machine]
    networks: list[Network]

    def sanitize(self):
        """
        Sanitize the config to remove any invalid values
        :return:
        """
        for net in self.networks:
            net.name = net.name.replace(" ", "-").lower()

        for machine in self.machines:
            machine.name = machine.name.replace(" ", "-").lower()
            machine.address.name = machine.address.name.replace(" ", "-").lower()
