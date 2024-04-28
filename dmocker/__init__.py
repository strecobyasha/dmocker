import argparse

from .src.connector import Connector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('device', type=str)
    parser.add_argument('task', action='store', type=str, nargs='*')
    args = parser.parse_args()
    username = args.device
    connector = Connector(username)
    if not args.task:
        connector.get_containers_docker()
    else:
        match args.task[0]:
            case 'ps':
                connector.get_containers_docker()
            case _:
                connector.get_containers_docker()
