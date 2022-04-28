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

    @abstractmethod
    def get_machines(self):
        """
        Returns a list of machines that are available on the provider
        :return: list[Machine]
        """
        pass

    @abstractmethod
    def get_simple_machines(self):
        """
        Returns a list of machines that are available on the provider
        :return: list[SimpleMachine]
        """
        pass

    @staticmethod
    def set_zone(zone):
        """
        Sets the zone for the provider
        :param zone:
        :return:
        """
        pass

    @staticmethod
    def get_zone():
        """
        Returns the zone for the provider
        :return:
        """
        pass

    @abstractmethod
    def get_available_projects(self):
        """
        Returns a list of projects that are available on the provider
        :return: list[Project]
        """
        pass

    @staticmethod
    def get_project():
        """
        Returns the project for the provider
        :return:
        """
        pass

    @staticmethod
    def set_project(project):
        """
        Sets the project for the provider
        :param project:
        :return:
        """
        pass
