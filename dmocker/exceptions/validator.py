"""
Validate parameters, that were passed to the main function.
"""
from .custom import WrongFlagException, TooManyFlagsException, NotEnoughArgsException, LogsNumberException, \
    LogsFollowException, TooManyParamsException, TooManyServersException


def validate(args):
    if (task := args.task[0]) == 'ps':
        # Task format: dmocker server1 server2... serverN -t ps [a]
        if len(args.task) == 2 and args.task[1] != 'a':
            raise WrongFlagException(args.task[1])
        elif len(args.task) > 2:
            raise TooManyFlagsException(args.task[1:])
    elif task == 'logs':
        # Task format: dmocker server -t logs container [logs_num] [follow]
        if len(args.servers) > 1:
            raise TooManyServersException(args.servers)
        elif len(args.task) == 1:
            raise NotEnoughArgsException()
        elif len(args.task) > 2 and (not args.task[2].isdigit() and args.task[2] != 'f'):
            raise LogsNumberException(args.task[2])
        elif len(args.task) == 4 and args.task[3] != 'f':
            raise LogsFollowException(args.task[3])
        elif len(args.task) > 4:
            raise TooManyParamsException(args.task[1:])
