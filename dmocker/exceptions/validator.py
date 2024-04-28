from .custom import WrongFlagException, TooManyFlagsException


def validate(args):
    task = args.task[0]
    match task:
        case 'ps':
            if len(args.task) == 2 and args.task[1] != 'a':
                raise WrongFlagException(args.task[1])
            elif len(args.task) > 2:
                raise TooManyFlagsException(args.task[1:])
