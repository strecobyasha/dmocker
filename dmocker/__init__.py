import argparse
import threading

from .exceptions.validator import validate
from .src.connector import Connector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('servers', action='store', type=str, nargs='*')
    parser.add_argument('-t', '--task', action='store', type=str, nargs='*')
    args = parser.parse_args()
    # Validate params
    if args.task:
        validate(args)
    # Establish connection to the remote servers.
    connections = list()
    def connect(server): connections.append(Connector(server))
    threads = [
        threading.Thread(target=connect, args=(server,))
        for server in args.servers
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
    # Execute the Docker command on the remote servers.
    if not args.task:
        [connector.get_containers() for connector in connections]
    else:
        task = args.task[0]
        match task:
            case 'ps':
                # List of containers.
                if len(args.task) == 1:
                    [connector.get_containers() for connector in connections]
                else:
                    [connector.get_containers(all_containers=True) for connector in connections]
            case _:
                [connector.get_containers() for connector in connections]
