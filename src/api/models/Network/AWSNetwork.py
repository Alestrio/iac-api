#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Literal

from models.Network.Network import Network


class AWSNetwork(Network):
    zone: str = "us-east-1"
    vpc_only: bool = False
    private_subnet_count: int = 1
    public_subnet_count: int = 1
    ip_cidr_range: str = "10.0.0.0/16"
    nat_gateway: Literal["ONE", "EACH", "NONE"] = "NONE"
    vpc_s3_out: bool = False
    dns_hostnames: bool = False
    dns_resolution: bool = False


