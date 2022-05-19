#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Literal, Optional

from models.Network.Network import Network
from math import ceil


class AWSNetwork(Network):
    zone: str = "us-east-1"
    vpc_only: bool = False
    availability_zones: int = 2
    private_subnet_count: int = 2
    public_subnet_count: int = 2
    ip_cidr_range: str = "10.0.0.0/16"
    nat_gateway: Literal["ONE", "EACH", "NONE"] = "NONE"
    vpc_s3_out: bool = False
    dns_hostnames: bool = False
    dns_resolution: bool = False
    PROVIDER: Optional[Literal["AWS"]] = "AWS"

    def create_subnets_cidr_ranges(self):
        """
        Create the subnets cidr
        Uses the number of private subnets and splits the ip_cidr_range by mask
        example for a 10.0.0.0/24 and 3 private subnets:
        subnet 1 : 10.0.0.0/26
        subnet 2 : 10.0.0.64/26
        subnet 3 : 10.0.0.128/26
        :return: an array of cidrs
        """
        cidrs = []
        bits_to_borrow = ceil(self.private_subnet_count / 2)  # example: 2subnets 1bits, 3subnets 2bits, 4subnets 2bits
        cidr_mask = self.ip_cidr_range.split("/")[1]
        cidr_mask = int(cidr_mask)
        new_mask = cidr_mask + bits_to_borrow
        # Now, we have to split the ip_cidr_range by mask
        # First, we will convert the base cidr to a proper int by using bit shifting
        base_cidr = self.ip_cidr_range.split("/")[0]
        base_cidr = base_cidr.split(".")
        base_cidr = int(base_cidr[0]) << 24 | int(base_cidr[1]) << 16 | int(base_cidr[2]) << 8 | int(base_cidr[3])
        # Then, we are doing the AND operation to get the base cidr
        base_cidr = base_cidr & (2 ** (32 - new_mask) - 1)

        # Now, with the borrowed bits, we can split the cidr
        for i in range(bits_to_borrow + 1):
            cidr_to_append = base_cidr + (2 ** (32 - new_mask) * i)
            # convert the cidr to a proper format
            cidr_to_append = str(cidr_to_append >> 24 & 255) + "." + str(cidr_to_append >> 16 & 255) + "." + str(
                cidr_to_append >> 8 & 255) + "." + str(cidr_to_append & 255) + "/" + str(new_mask)
            cidrs.append(cidr_to_append)
        return cidrs

            

if __name__ == "__main__":
    net = AWSNetwork()
    net.create_subnets_cidr_ranges()
        