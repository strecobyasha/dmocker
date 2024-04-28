import docker

from .container_info import ContainerInfo


class Connector:

    def __init__(self, username: str):
        self.client = docker.APIClient(f'ssh://{username}')

    def get_containers_docker(self):
        print('ID'.ljust(20), 'IMAGE'.ljust(30), 'STATUS'.ljust(30), 'NAME')
        for container in self.client.containers():
            info = ContainerInfo(container)
            print(info.id.ljust(20), info.image.ljust(30), info.status.ljust(30), info.name)
