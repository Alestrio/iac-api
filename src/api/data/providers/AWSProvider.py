#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import yaml

from data.providers.Provider import Provider
import boto3

from models.Disk import Disk
from models.Machine import Machine
from models.Network.Address import Address
from models.Network.Network import Network


class AWSProvider(Provider):
    provider_key = "aws"
    config_file = f"./config/app_config/provider.{provider_key}.yaml"

    def __init__(self):
        super().__init__()
        # Open yaml config
        with open(self.config_file, 'r') as stream:
            self.config = yaml.load(stream, Loader=yaml.FullLoader)[self.provider_key]
            self.project_id = self.config['project_id']
            self.zone = self.config['zone']
            self.config_dict = {
                'access_key': self.config['access_key'],
                'secret_key': self.config['secret_key'],
                'zone': self.config['zone']
            }

    def get_deployed_instances(self):
        """
        Get all instances from AWS for the project
        :return:
        """
        ec2 = boto3.resource('ec2', region_name=self.zone, aws_access_key_id=self.config['access_key'],
                             aws_secret_access_key=self.config['secret_key'])
        # Get all instances
        instances = ec2.instances.all()
        machines = []
        for instance in instances:
            machines.append(
                Machine(providers=[self.provider_key], aws_type=instance.instance_type,
                        aws_machine_image=instance.image_id, aws_zone=instance.placement['AvailabilityZone'],
                        network=Network.from_aws_network(instance.network_interfaces, **self.config_dict),
                        address=Address.from_aws_address(instance.public_ip_address),
                        disks=Disk.from_aws_disk(instance.block_device_mappings, **self.config_dict))
            )
        print(machines)

    def get_deployed_networks(self):
        pass


if __name__ == '__main__':
    provider = AWSProvider()
    provider.get_deployed_instances()
