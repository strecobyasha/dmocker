import argparse
import threading

from .exceptions.validator import validate
from .src.arguments import add_arguments, epilog
from .src.fetcher import Fetcher


def get_connections(servers: list) -> list:
    """ Establish connections to the remote servers. """
    connections = list()
    threads = [
        threading.Thread(target=lambda server: connections.append(Fetcher(server)), args=(server,))
        for server in servers
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
    return connections


def router():
    """ Define and initiate the task based on passed parameters. """
    parser = argparse.ArgumentParser(
        description='A controller for remote Docker containers',
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_arguments(parser)
    args = parser.parse_args()
    # Validate params before establishing connections.
    if args.task:
        validate(args)
    connections = get_connections(args.servers)
    # Execute the Docker command on the remote servers.
    if not args.task:
        [fetcher.get_containers(name=args.name) for fetcher in connections]
    elif (task := args.task[0]) == 'ps':
        # List of containers.
        if len(args.task) == 1:
            [fetcher.get_containers(name=args.name) for fetcher in connections]
        else:
            [fetcher.get_containers(all_containers=True, name=args.name) for fetcher in connections]
    elif task == 'logs':
        # Container logs.
        logs_num, follow = 10, False
        if len(args.task) > 2:
            try:
                logs_num = int(args.task[2])
            except ValueError:
                logs_num = 10
                follow = True
            else:
                if len(args.task) == 4:
                    follow = args.task[3] == 'f'
        connections[0].get_logs(args.task[1], logs_num, follow)
