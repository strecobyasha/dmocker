"""
Interface for the communication with the remote Docker engine.
"""
import docker

from .container_info import ContainerInfo


class Connector:

    def __init__(self, server: str):
        self.server = server
        self.client = docker.APIClient(f'ssh://{server}')

    def get_containers(self):
        """ Get the list of the running containers. """
        print(f'Server: {self.server}')
        print('ID'.ljust(20), 'IMAGE'.ljust(40), 'STATUS'.ljust(30), 'NAME')
        for container in self.client.containers():
            info = ContainerInfo(container)
            print(info.id.ljust(20), info.image.ljust(40), info.status.ljust(30), info.name)
        print('\n')
