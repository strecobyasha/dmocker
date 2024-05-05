"""
Interface for the communication with the remote Docker engine.
"""
import os
import urllib.parse

import docker
import paramiko
from docker.transport import SSHHTTPAdapter

from .container_info import Columns, ContainerInfo


SSHHTTPAdapter_create_paramiko_client = SSHHTTPAdapter._create_paramiko_client


def custom_ssh_http_adapter(self, base_url):
    """ Set ssh port from ssh/config file in a case of non-standard port. """
    SSHHTTPAdapter_create_paramiko_client(self, base_url)
    base_url = urllib.parse.urlparse(base_url)
    ssh_config_file = os.path.expanduser('~/.ssh/config')
    if os.path.exists(ssh_config_file):
        conf = paramiko.SSHConfig()
        with open(ssh_config_file) as f:
            conf.parse(f)
        host_config = conf.lookup(base_url.hostname)
        if base_url.port == 22 and 'port' in host_config:
            self.ssh_params['port'] = host_config['port']
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


SSHHTTPAdapter._create_paramiko_client = custom_ssh_http_adapter


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
        print(
            'ID'.ljust(Columns.ID_COLUMN_WIDTH),
            'IMAGE'.ljust(Columns.IMAGE_COLUMN_WIDTH),
            'STATUS'.ljust(Columns.STATUS_COLUMN_WIDTH),
            'NAME',
        )
        for container in self.client.containers(all=all_containers, filters={'name': name}):
            info = ContainerInfo(container)
            print(
                info.id.ljust(Columns.ID_COLUMN_WIDTH),
                info.image.ljust(Columns.IMAGE_COLUMN_WIDTH),
                info.status.ljust(Columns.STATUS_COLUMN_WIDTH),
                info.name,
            )
        self.client.close()

    def get_logs(self, container: str, logs_num: int = 10, follow: bool = False):
        """ Get logs of the container. """
        print(f'Server: {self.server}, container: {container}')
        logs = self.client.logs(container, tail=logs_num, stream=follow)
        if follow:
            try:
                for log in logs:
                    print(log.decode())
            except KeyboardInterrupt:
                self.client.close()
        else:
            for log in logs.decode().split('\n'):
                print(log)
            self.client.close()
