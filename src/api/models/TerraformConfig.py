#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), Alexis LEBEL, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os
from typing import Optional, Union

from pydantic import BaseModel

from data.storage import AnsibleStorage
from models.Machine import Machine
from models.Network.AWSNetwork import AWSNetwork
from models.Network.GCPNetwork import GCPNetwork
from models.Network.Network import Network


class TerraformConfig(BaseModel):
    name: str = os.urandom(8).hex()
    project_id: str = "environnement-de-test-329611"
    ssh_user: str = "ubuntu"
    private_key_name: str = "sample-key"
    machines: list[Machine]
    networks: Optional[list[Union[AWSNetwork, GCPNetwork]]] = None
    roles: list[str] = []

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

        for role in self.roles:
            if role not in AnsibleStorage.get_available_role_files():
                self.roles.remove(role)
        
        for net in self.networks:
            if isinstance(net, AWSNetwork):
                net.create_subnets_cidr_ranges()

    def get_gcp_networks(self):
        """
        Get the name of the GCP network
        :return:
        """
        for net in self.networks:
            if isinstance(net, GCPNetwork):
                return net

    def get_aws_networks(self):
        """
        Get the name of the AWS network
        :return:
        """
        for net in self.networks:
            if isinstance(net, AWSNetwork):
                return net
