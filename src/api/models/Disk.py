#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional

from pydantic import BaseModel


class Disk(BaseModel):
    """
    That class represents a disk. It is independent of the provider.
    """
    id: Optional[str]
    provider: str = "aws"
    aws_type: str = "gp2"
    aws_subtype: str = "standard"
    gcp_type: str = "pd-standard"
    gcp_subtype: str = "standard"
    size: int = 10  # GB
    aws_region: str = "eu-central-1"
    gcp_region: str = "europe-west1"
    aws_zone: str = "eu-central-1a"
    gcp_zone: str = "europe-west1-b"
    name: str = "disk"
