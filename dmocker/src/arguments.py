"""
Add arguments to the ArgumentParser.
"""

COMMAND_PADDING = 70

epilog = f''' Examples:
    {"dmocker server".ljust(COMMAND_PADDING)} list containers running on the server
    {"dmocker server1 server2... serverN".ljust(COMMAND_PADDING)} list containers running on multiple servers
    {"dmocker server1 server2... serverN -t ps".ljust(COMMAND_PADDING)} list containers running on multiple servers
    {"dmocker server1 server2... serverN -t ps a".ljust(COMMAND_PADDING)} list all containers on multiple servers
    {"dmocker server1 server2... serverN -n container_name_filter".ljust(COMMAND_PADDING)} \
list containers running on multiple servers, filtered by container_name_filter
    {"dmocker server -t logs container_id".ljust(COMMAND_PADDING)} show last 10 logs from the container
    {"dmocker server -t logs container_id 20".ljust(COMMAND_PADDING)} show last 20 logs from the container
    {"dmocker server -t logs container_id f".ljust(COMMAND_PADDING)} show last 10 logs from the container and follow
    {"dmocker server -t logs container_id 20 f".ljust(COMMAND_PADDING)} show last 20 logs from the container and follow
    '''


def add_arguments(parser):
    parser.add_argument(
        'servers',
        action='store',
        type=str,
        nargs='*',
        help='List of remote servers',
    )
    parser.add_argument(
        '-t',
        '--task',
        action='store',
        type=str,
        nargs='*',
        help='Task name with parameters. '
             'Available tasks: ps [a] (requires at least one server);'
             'logs [container_id or container_name] [logs_num] [follow] (requires exactly one server)',
    )
    parser.add_argument(
        '-n',
        '--name',
        type=str,
        default='',
        help='Name of the container (or part of the name) to filter the list. Used with the task "ps"'
    )
