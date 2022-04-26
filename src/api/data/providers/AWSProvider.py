#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import yaml

from data.providers.Provider import Provider
import boto3

from models.Disk import Disk
from models.Machine import Machine, SimplifiedMachine
from models.Network.Address import Address
from models.Network.FirewallRule import FirewallRule
from models.Network.Network import Network, SimplifiedNetwork
from models.Network.Rule import Rule
from models.Network.Subnetwork import Subnetwork, SimplifiedSubnetwork


class AWSProvider(Provider):
    def get_machines(self):
        pass

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
            for subnet in subnets:
                subns.append(
                    SimplifiedSubnetwork(
                        name=subnet['SubnetId'],
                        subnetwork_name=subnet['SubnetId'],
                        ip_cidr_range=subnet['CidrBlock'],
                        region=subnet['AvailabilityZone'][:-1],
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
                            source_networks=rule['IpPermissionsEgress'] if 'IpPermissionsEgress' in rule else ['0.0.0.0/0'],
                        )
                    )
                firewalls.append(FirewallRule(
                    name=firewall['GroupName'],
                    is_allow=True,
                    rules=firewalls
                ))
            print(vpc)
            networks.append(
                SimplifiedNetwork(
                    name=vpc['VpcId'],
                    subnets=subns,
                    zone=self.zone,
                    description='None',
                    firewall_rules=firewalls
                )
            )
        print(networks)
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




if __name__ == '__main__':
    provider = AWSProvider()
    provider.get_simple_networks()
