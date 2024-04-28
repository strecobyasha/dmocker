
EXAMPLE_MSG = 'Command "ps" may be called without flags or with the flag "a". ' \
              'Examples: "dmocker server1 ps", "dmocker server1 ps a"'


class WrongFlagException(Exception):

    def __init__(self, flags):
        super().__init__(f'Unsuitable flag: {flags}. {EXAMPLE_MSG}')


class TooManyFlagsException(Exception):

    def __init__(self, flags):
        super().__init__(f'Too many flags: {flags}. {EXAMPLE_MSG}')
