#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os
from unittest import TestCase

from data.storage import TerraformStorage
from models.Disk import Disk
from models.Machine import Machine
from models.TerraformConfig import TerraformConfig


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
        file_exists = os.path.isfile("./config/terraform_configs/test_terraform_infra.tf")
        self.assertTrue(file_exists)
        # remove the terraform infra
        # os.remove("./config/terraform_configs/test_terraform_infra.tf")

    def test_get_all_config_names(self):
        """
        Test that we can get all the config names
        """
        if len(os.listdir("./config/terraform_configs")) == 0:
            machines = [Machine(disks=[Disk(provider="aws", type="ebs", subtype="gp2", size=100, region="eu-west-1",
                                            zone="eu-west-1a", name="disk1")])]
            config = TerraformConfig(machines=machines, name="test_terraform_infra", project_id="000-test")
            # store the terraform infra
            TerraformStorage.store_terraform_infra(config)
        config_names = TerraformStorage.get_all_config_names()
        self.assertTrue(len(config_names) > 0)
