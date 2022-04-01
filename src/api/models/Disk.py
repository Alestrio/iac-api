#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from pydantic import BaseModel


class Disk(BaseModel):
    """
    That class represents a disk. It is independent of the provider.
    """
    id: str
    provider: str
    type: str
    subtype: str
    size: int
    region: str
    zone: str
    name: str
