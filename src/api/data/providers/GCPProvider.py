#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from pprint import pprint

import oauth2client
from pydantic import json

from data.providers.Provider import Provider
import yaml

from googleapiclient import discovery
from google.oauth2 import service_account

from models.Disk import Disk
from models.Machine import Machine
from models.Network.Address import Address
from models.Network.FirewallRule import FirewallRule
from models.Network.Network import Network
from models.Network.Subnetwork import Subnetwork


class GCPProvider(Provider):
    provider_key = "gcp"
    config_file = f"./config/app_config/provider.{provider_key}.yaml"

    def __init__(self):
        super().__init__()
        # Open yaml config
        with open(self.config_file, 'r') as stream:
            self.config = yaml.load(stream, Loader=yaml.FullLoader)
            self.project_id = self.config['project_id']
            self.zone = self.config['zone']
            self.serviceaccount_email = self.config['serviceaccount_email']
            self.path_to_key = self.config['path_to_key']

        self.credentials = service_account.Credentials.from_service_account_file(self.path_to_key)
        self.compute = discovery.build('compute', 'v1', credentials=self.credentials)

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
                              gcp_network=self.get_network_information_by_name(i['networkInterfaces'][0]['network'].split('/')[-1]),
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


if __name__ == '__main__':
    import time
    start = time.time()
    provider = GCPProvider()
    print(provider.get_deployed_instances())
    print(time.time() - start)
