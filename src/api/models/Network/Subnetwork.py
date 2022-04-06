#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional

from pydantic import BaseModel


class Subnetwork(BaseModel):
    name: str
    network_name: str
    ip_cidr_range: Optional[str]
    gcp_region: Optional[str]
    aws_region: Optional[str]
