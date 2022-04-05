#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os
from unittest import TestCase

from data.storage import TerraformStorage
from models.Disk import Disk
from models.FirewallRule import FirewallRule
from models.Machine import Machine
from models.Network import Network
from models.TerraformConfig import TerraformConfig
from models.Rule import Rule

# expected_content = """locals {
#     project_id       = 000-test
#     region           = eu-west-1
#     ssh_user         = ubuntu
#     private_key_path = ./config/secrets/sample-key"""


class Test(TestCase):
    def test_store_terraform_infra(self):
        """
        Test that we can store a terraform infra
        """
        machines = [Machine(disks=[Disk(provider="aws", type="ebs", subtype="gp2", size=100, region="eu-west-1",
                                        zone="eu-west-1a", name="disk1")])]
        config = TerraformConfig(machines=machines, name="test_terraform_infra", project_id="000-test", networks=[])
        # store the terraform infra
        TerraformStorage.store_terraform_infra(config)
        # check that the terraform infra has been stored
        file_exists = os.path.isfile("./config/terraform_configs/test_terraform_infra/main.tf")
        self.assertTrue(file_exists)
        TerraformStorage.delete_terraform_infra("test_terraform_infra")
        self.assertFalse(os.path.isfile("./config/terraform_configs/test_terraform_infra/main.tf"))

    def test_get_all_config_names(self):
        """
        Test that we can get all the config names
        """
        if not os.path.isfile("./config/terraform_configs/test_terraform_infra.tf"):
            machines = [Machine(disks=[Disk(provider="aws", type="ebs", subtype="gp2", size=100, region="eu-west-1",
                                            zone="eu-west-1a", name="disk1")])]
            config = TerraformConfig(machines=machines, name="test_terraform_infra", project_id="000-test", networks=[])
            # store the terraform infra
            TerraformStorage.store_terraform_infra(config)
        config_names = TerraformStorage.get_all_config_names()
        self.assertTrue(len(config_names) > 0)
        TerraformStorage.delete_terraform_infra("test_terraform_infra")
        self.assertFalse(os.path.isfile("./config/terraform_configs/test_terraform_infra.tf"))

    # def test_terraform_infra_content(self):
    #     """
    #     Test that we can get the content of a terraform infra
    #     """
    #     if not os.path.isfile("./config/terraform_configs/test_terraform_infra.tf"):
    #         machines = [Machine(disks=[Disk(provider="aws", type="ebs", subtype="gp2", size=100, region="eu-west-1",
    #                                         zone="eu-west-1a", name="disk1")])]
    #         config = TerraformConfig(machines=machines, name="test_terraform_infra", project_id="000-test", networks=[])
    #         # store the terraform infra
    #         TerraformStorage.store_terraform_infra(config)
    #     with open("./config/terraform_configs/test_terraform_infra.tf", "r") as file:
    #         content = file.read()
    #     self.assertIn(content, expected_content)
    #     TerraformStorage.delete_terraform_infra("test_terraform_infra.tf")
    #     self.assertFalse(os.path.isfile("./config/terraform_configs/test_terraform_infra.tf"))

    def test_render_content_templates(self):
        """
        Test the render content template method
        """
        machines = [Machine(disks=[Disk(provider="aws", type="ebs", subtype="gp2", size=100, region="eu-west-1",
                                        zone="eu-west-1a", name="disk1")])]
        networks = [Network(name="a_network", subnet="192.168.0.0/24", firewall_rules=[FirewallRule(name="test", rules=[Rule()])])]
        config = TerraformConfig(machines=machines, name="test_terraform_infra", project_id="000-test", networks=networks)
        assert(TerraformStorage.render_content_templates(config) != "")
