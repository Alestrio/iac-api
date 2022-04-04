#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from models.Disk import Disk


class Machine:
    """
    Machine class
    """
    def __init__(self, disks: list[Disk], gcp_zone="us-central1-a", aws_zone="eu-west-3", gcp_network="default",
                 aws_network="", gcp_machine_type="e2-micro", aws_machine_type="t2.micro",
                 gcp_machine_image="debian-10-buster-v20200101", aws_machine_image="ami-045fa58af83eb0ff4",
                 cpu=0, memory=0, machine_name="machine",):
        """
        Machine class constructor

        :param disks: List of Disk objects, disks to be attached to the machine \
        :param gcp_zone: Zone of the GCP machine, default is us-central1-a
        :param aws_zone: Zone of the AWS machine, default is eu-west-3
        :param gcp_network: Network of the GCP machine, default is "default"
        :param aws_network: Network of the AWS machine, default is empty
        :param gcp_machine_type: Machine type, default is e2-micro
        :param aws_machine_type: Machine type, default is t2.micro
        :param gcp_machine_image: The image to use for the GCP machine, default is debian-10-buster-v20200101
        :param aws_machine_image: The image to use for the AWS machine, default is a debian 9 stretch image
        :param cpu: The number of CPUs to allocate to the machine, default is 0, using the machine type
        :param memory: The amount of memory to allocate to the machine, default is 0, using the machine type
        :param machine_name: The name of the machine, default is "machine"
        """
        if cpu == 0 or memory == 0:
            self.gcp_type = gcp_machine_type
            self.aws_type = aws_machine_type
        else:
            self.cpu = cpu
            self.memory = memory
        self.gcp_machine_image = gcp_machine_image
        self.aws_machine_image = aws_machine_image
        self.name = machine_name
        self.gcp_zone = gcp_zone
        self.aws_zone = aws_zone
        self.gcp_network = gcp_network
        self.aws_network = aws_network
        self.disks = disks
