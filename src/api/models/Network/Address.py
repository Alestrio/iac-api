#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional, Union

from pydantic import BaseModel


class Address(BaseModel):
    name: str
    subnetwork_name: Optional[str] = None
    address_type: Optional[str] = None
    address: Optional[str] = None
    gcp_region: Optional[str] = None

    @staticmethod
    def from_google_address(google_dict: dict):
        return Address(
            name=google_dict["name"],
            address_type=google_dict["type"],
            address=google_dict["natIP"] if "natIP" in google_dict else None,
        )
