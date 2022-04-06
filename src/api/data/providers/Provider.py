#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.

# Create an abstract class for data providers
from abc import abstractmethod


class Provider:
    def __init__(self):
        """
        Constructor
        """
        pass

    @abstractmethod
    def get_deployed_instances(self):
        """
        Returns a list of instances that are deployed on the provider
        :return: list[Machine]
        """
        pass

    @abstractmethod
    def get_deployed_networks(self):
        """
        Returns a list of networks that are deployed on the provider
        :return: list[Network]
        """
        pass
