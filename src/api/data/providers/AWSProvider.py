#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import json

import requests
import yaml
from beaker.cache import cache_region, cache_regions

from data.providers.Provider import Provider
import boto3

from models.Disk import Disk
from models.Machine import Machine, SimplifiedMachine
from models.Network.Address import Address
from models.Network.Firewall import Firewall
from models.Network.Network import Network, SimplifiedNetwork
from models.Network.Rule import Rule
from models.Network.Subnetwork import Subnetwork, SimplifiedSubnetwork


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

        cache_regions.update({
            'api_data': {
                'type': 'memory',
                'expire': 60 * 60 * 1,  # 1h
                'key_length': 250
            }
        })

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
        return machines

    def get_deployed_networks(self):
        pass

    def get_simple_machines(self):
        ec2 = boto3.resource('ec2', region_name=self.zone, aws_access_key_id=self.config['access_key'],
                             aws_secret_access_key=self.config['secret_key'])
        # Get all instances
        instances = ec2.instances.all()
        machines = []
        for instance in instances:
            machine = SimplifiedMachine(name=instance.tags[0]['Value'] if instance.tags else None,
                                        type=instance.instance_type,
                                        zone=instance.placement['AvailabilityZone'],
                                        disks_number=len(instance.block_device_mappings),
                                        os=ec2.Image(instance.image_id).name)
            machine.translateType()
            machines.append(machine)
        return machines

    def get_simple_networks(self):
        client = boto3.client('ec2', region_name=self.zone, aws_access_key_id=self.config['access_key'],
                              aws_secret_access_key=self.config['secret_key'])
        networks = []
        for vpc in client.describe_vpcs()['Vpcs']:
            # Fetches all subnets in the vpc
            subns = []
            subnets = client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])['Subnets']
            print(subnets)
            for subnet in subnets:
                subns.append(
                    SimplifiedSubnetwork(
                        zone=subnet['AvailabilityZone'][:-1],
                        name=subnet['SubnetId'],
                        subnetwork_name=subnet['SubnetId'],
                        ip_cidr_range=subnet['CidrBlock'],
                     )
                )
            firewalls = []
            for firewall in client.describe_security_groups(
                    Filters=[{'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])['SecurityGroups']:
                for rule in firewall['IpPermissions']:
                    firewalls.append(
                        Rule(
                            protocol=rule['IpProtocol'],
                            from_ports=[rule['FromPort']] if 'FromPort' in rule else [-1],
                            to_ports=[rule['ToPort']] if 'ToPort' in rule else [-1],
                            source_networks=rule['IpPermissionsEgress'] if 'IpPermissionsEgress' in rule else ['0.0.0'
                                                                                                               '.0/0'],
                        )
                    )
                firewalls.append(Firewall(
                    name=firewall['GroupName'],
                    is_allow=True,
                    rules=firewalls
                ))
            networks.append(
                SimplifiedNetwork(
                    name=vpc['VpcId'],
                    subnets=subns,
                    zone=self.zone,
                    description='None',
                    firewalls=firewalls
                )
            )
        return networks

    @staticmethod
    def set_zone(zone):
        available_zones = []
        with open("./config/app_config/provider.aws.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            for i in config['aws']['available_zones']:
                available_zones.append(i)
        if zone not in available_zones:
            raise ValueError('Zone not available')
        else:
            with open("./config/app_config/provider.aws.yaml", 'w') as f:
                config['aws']['zone'] = zone
                yaml.dump(config, f)
        return

    @staticmethod
    def get_zone():
        with open("./config/app_config/provider.aws.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['aws']['zone']

    @staticmethod
    def get_available_zones():
        with open("./config/app_config/provider.aws.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['aws']['available_zones']

    def get_available_projects(self):
        return []

    @staticmethod
    def get_project():
        return None

    @staticmethod
    def get_machine_types():
        with open("./config/app_config/app.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            url = config['aws_instances_api']
            token = config['aws_token']
            headers = {'Authorization': 'Bearer ' + token}
            response = requests.get(url, headers=headers).json()
            machine_types = []
            for i in response['products']:
                machine_types.append(i['name'])
            return machine_types

    @staticmethod
    def get_machine_image_list():
        with open("./config/app_config/aws_amis.json", 'r') as f:
            config = json.load(f)
            return config

    @staticmethod
    def get_disk_types():
        return 'none'

    @staticmethod
    def get_access_key():
        with open("./config/app_config/provider.aws.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['aws']['access_key']

    @staticmethod
    def get_secret_key():
        with open("./config/app_config/provider.aws.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['aws']['secret_key']
    

if __name__ == '__main__':
    provider = AWSProvider()
    print(provider.get_machine_image_list())
