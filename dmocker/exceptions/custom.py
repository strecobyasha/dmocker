
PS_EXAMPLE_MSG = 'Command "ps" may be called without flags or with the flag "a". ' \
                 'Examples: "dmocker server1 -t ps", "dmocker server1 -t ps a"'
LOGS_EXAMPLE_MSG = 'Command "logs" requires id or name of the container' \
                   'Example: "dmocker server1 -t logs container_id"'
LOGS_NUMBER_EXAMPLE_MSG = 'Command "logs" may be called with the number of last logs to display. ' \
                          'Example: "dmocker server1 -t logs container_id 20"'
LOGS_FOLLOW_EXAMPLE_MSG = 'Command "logs" may be called with the flag "follow". ' \
                          'Example: "dmocker server1 -t logs container_id 20 f"'


class WrongFlagException(Exception):

    def __init__(self, flag: str):
        super().__init__(f'Unsuitable flag: {flag}. {PS_EXAMPLE_MSG}')


class TooManyFlagsException(Exception):

    def __init__(self, flags: list):
        super().__init__(f'Too many flags: {flags}. {PS_EXAMPLE_MSG}')


class TooManyServersException(Exception):

    def __init__(self, servers: list):
        super().__init__(f'Too many servers: {servers}. Specify only one server.')


class NotEnoughArgsException(Exception):

    def __init__(self):
        super().__init__(f'Not enough arguments. {LOGS_EXAMPLE_MSG}')


class LogsNumberException(Exception):

    def __init__(self, num: str):
        super().__init__(f'Logs number format error: {num}. {LOGS_NUMBER_EXAMPLE_MSG}')


class LogsFollowException(Exception):

    def __init__(self, flag: str):
        super().__init__(f'Logs follow task format error: {flag}. {LOGS_FOLLOW_EXAMPLE_MSG}')


class TooManyParamsException(Exception):

    def __init__(self, params: list):
        super().__init__(f'Too many parameters: {params}. {LOGS_FOLLOW_EXAMPLE_MSG}')
