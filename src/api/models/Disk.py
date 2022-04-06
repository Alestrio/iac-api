#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional

from pydantic import BaseModel, validator


class Disk(BaseModel):
    """
    That class represents a disk. It is independent of the provider.
    """
    id: Optional[str]
    providers: list[str] = ['gcp']
    aws_type: str = "gp2"
    aws_subtype: str = "standard"
    gcp_type: str = "pd-standard"
    gcp_subtype: str = "standard"
    size: int = 10  # GB
    aws_zone: str = "eu-central-1a"
    gcp_zone: str = "europe-west1-b"
    name: Optional[str]

    @staticmethod
    def from_google_disk(google_dict: dict):
        """
        This method creates a Disk object from a Google disk.
        :param google_dict: Google disk dict
        :return: Disk object
        """
        return Disk(
            #id=google_dict['id'],
            providers=['gcp'],
            gcp_type=google_dict['type'].split('/')[-1],
            size=google_dict['diskSizeGb'],
            #gcp_zone=google_dict['zone'].split('/')[-1],
            name=google_dict['deviceName']
        )
