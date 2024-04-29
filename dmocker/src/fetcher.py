"""
Interface for the communication with the remote Docker engine.
"""
import docker
import paramiko

from .container_info import ContainerInfo


class Fetcher:

    def __init__(self, server: str):
        self.server = server
        try:
            self.client = docker.APIClient(f'ssh://{server}')
        except paramiko.ssh_exception.AuthenticationException:
            self.client = docker.APIClient(f'ssh://{server}', use_ssh_client=True, version='1.41')

    def get_containers(self, all_containers: bool = False, name: str = ''):
        """ Get the list of containers. """
        print(f'Server: {self.server}')
        print('ID'.ljust(20), 'IMAGE'.ljust(40), 'STATUS'.ljust(30), 'NAME')
        for container in self.client.containers(all=all_containers, filters={'name': name}):
            info = ContainerInfo(container)
            print(info.id.ljust(20), info.image.ljust(40), info.status.ljust(30), info.name)
        self.client.close()

    def get_logs(self, container_id: str, logs_num: int = 10, follow: bool = False):
        """ Get logs of the container. """
