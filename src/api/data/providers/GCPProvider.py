#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import requests
from beaker.cache import cache_regions, cache_region

from data.providers.Provider import Provider
import yaml

from googleapiclient import discovery
from google.oauth2 import service_account

from models.Disk import Disk
from models.Machine import Machine, SimplifiedMachine
from models.Network.Address import Address
from models.Network.Firewall import FirewallRule
from models.Network.Network import Network, SimplifiedNetwork
from models.Network.Subnetwork import Subnetwork, SimplifiedSubnetwork


class GCPProvider(Provider):
    provider_key = "gcp"
    config_file = f"./config/app_config/provider.{provider_key}.yaml"

    def __init__(self):
        super().__init__()
        # Open yaml config
        with open(self.config_file, 'r') as stream:
            self.config = yaml.load(stream, Loader=yaml.FullLoader)[self.provider_key]
            self.project_id = self.config['project_id']
            self.zone = self.config['zone']
            self.serviceaccount_email = self.config['serviceaccount_email']
            self.path_to_key = self.config['path_to_key']

        self.credentials = service_account.Credentials.from_service_account_file(self.path_to_key)
        self.compute = discovery.build('compute', 'v1', credentials=self.credentials)

        cache_regions.update({
            'api_data': {
                'type': 'memory',
                'expire': 60 * 60 * 1,  # 1h
                'key_length': 250
            }
        })

    def get_deployed_instances(self):
        """
        Get all deployed instances
        :return: list of instances
        """
        request = self.compute.instances().list(project=self.project_id, zone=self.zone)
        response = request.execute()
        machines = list[Machine]()
        for i in response['items']:
            machine = Machine(name=i['name'], providers=[self.provider_key], gcp_type=i['machineType'].split('/')[-1],
                              gcp_machine_image=i['disks'][0]['licenses'][0].split('/')[-1],
                              gcp_zone=self.zone,
                              gcp_network=self.get_network_information_by_name(
                                  i['networkInterfaces'][0]['network'].split('/')[-1]),
                              address=Address.from_google_address(i['networkInterfaces'][0]["accessConfigs"][0]),
                              disks=[Disk.from_google_disk(j) for j in i['disks']])
            machines.append(machine.dict())
        return machines

    def get_deployed_networks(self):
        pass

    def get_network_information_by_name(self, name):
        request = self.compute.networks().get(project=self.project_id, network=name)
        response = request.execute()
        return Network.from_google_network(response,
                                           self.get_subnetworks_information_by_name(response['subnetworks'][0].
                                                                                    split('/')[-1]),
                                           self.get_firewall_information_by_subnetwork_name(response['subnetworks'][0].
                                                                                            split('/')[-1]))

    def get_subnetworks_information_by_name(self, name):
        request = self.compute.subnetworks().get(project=self.project_id, subnetwork=name, region=self.zone[:-2])
        response = request.execute()
        return Subnetwork.from_google_subnetwork(response).__dict__

    def get_firewall_information_by_subnetwork_name(self, name):
        request = self.compute.firewalls().list(project=self.project_id)
        response = request.execute()
        firewall_list = []
        for i in response['items']:
            if i['network'] == name:
                firewall_list.append(FirewallRule.from_google_firewall(i).__dict__)
        return firewall_list

    def get_disk_information_by_name(self, name):
        request = self.compute.disks().get(project=self.project_id, zone=self.zone, disk=name)
        response = request.execute()
        return Disk.from_google_disk(response)

    def get_simple_machines(self):
        request = self.compute.instances().list(project=self.project_id, zone=self.zone)
        response = request.execute()
        machines = list[Machine]()
        if 'items' in response:
            for i in response['items']:
                machine = SimplifiedMachine(name=i['name'], type=i['machineType'].split('/')[-1],
                                            zone=self.zone, disks_number=len(i['disks']),
                                            os=i['disks'][0]['licenses'][0].split('/')[-1])
                machine.translateType()
                machines.append(machine.dict())
        else:
            return response
        return machines

    @cache_region('api_data')
    def __get_subnetworks(self, j):
        request = self.compute.subnetworks().get(project=self.project_id, subnetwork=j.split('/')[-1],
                                                 region=self.zone[:-2])
        response = request.execute()
        return response

    def get_simple_networks(self):
        request = self.compute.networks().list(project=self.project_id)
        response = request.execute()
        networks = list[Network]()
        for i in response['items']:
            if self.zone[-1] != i['selfLink'].split('/')[-1] or i['selfLink'].split('/')[-2] == 'global':
                subnets = []
                for j in i['subnetworks']:
                    if j.split('/')[-3] == self.zone[:-2]:
                        response = self.__get_subnetworks(j)
                        subnet = Subnetwork.from_google_subnetwork(response)
                        simple_subnet = SimplifiedSubnetwork.from_subnetwork(subnet)
                        subnets.append(simple_subnet.dict())
                firewall_requests = self.compute.firewalls().list(project=self.project_id)
                firewall_response = firewall_requests.execute()
                rules = []
                for k in firewall_response['items']:
                    if k['network'].split('/')[-1] == i['name']:
                        rules.append(FirewallRule.from_google_rule(k))
                firewall = FirewallRule(rules=rules, name=i['name'], is_allow=True)
                network = SimplifiedNetwork(name=i['name'], zone=self.zone,
                                            subnets=subnets, description=i['description'] if 'description' in i else '',
                                            firewalls=[firewall])

                networks.append(network.dict())
        return networks

    @staticmethod
    def set_zone(zone):
        available_zones = []
        with open("./config/app_config/provider.gcp.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            for i in config['gcp']['available_zones']:
                available_zones.append(i)
        if zone not in available_zones:
            raise ValueError('Zone not available')
        else:
            with open("./config/app_config/provider.gcp.yaml", 'w') as f:
                config['gcp']['zone'] = zone
                yaml.dump(config, f)
        return

    @staticmethod
    def get_zone():
        with open("./config/app_config/provider.gcp.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['gcp']['zone']

    @staticmethod
    def get_available_zones():
        with open("./config/app_config/provider.gcp.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['gcp']['available_zones']

    def get_available_projects(self):
        ressource = discovery.build('cloudresourcemanager', 'v1', credentials=self.credentials)
        request = ressource.projects().list()
        response = request.execute()
        projects = []
        for i in response['projects']:
            projects.append(i['projectId'])
        return projects

    @staticmethod
    def get_project():
        with open("./config/app_config/provider.gcp.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['gcp']['project_id']

    def set_project(self, project_id):
        with open("./config/app_config/provider.gcp.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            available_projects = self.get_available_projects()
            if project_id in available_projects:
                config['gcp']['project_id'] = project_id
                with open("./config/app_config/provider.gcp.yaml", 'w') as f:
                    yaml.dump(config, f)
                return
            else:
                raise ValueError('Project not available')
        return

    @staticmethod
    def get_forbidden_networks():
        with open("./config/app_config/provider.gcp.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['gcp']['forbidden_networks']

    @staticmethod
    def get_machine_types():
        with open("./config/app_config/app.yaml", 'r') as f:
            url = yaml.load(f, Loader=yaml.FullLoader)['gcp_instances_api']
        response = requests.get(url).json()
        type_names = []
        for key, value in response.items():
            for key2, value2 in value.items():
                type_names.append(key2)
        return type_names

    @staticmethod
    def get_machine_image_list():
        with open("./config/app_config/provider.gcp.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['gcp']['machine_images']

    @staticmethod
    def get_disk_types():
        with open("./config/app_config/provider.gcp.yaml", 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['gcp']['disk_types']


if __name__ == '__main__':
    import time

    start = time.time()
    provider = GCPProvider()
    print(provider.get_machine_types())
    print(time.time() - start)
