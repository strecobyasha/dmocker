"""
Test options to get the list of containers.
"""
import sys
import unittest
from unittest.mock import patch

from dmocker import main
from dmocker.exceptions.custom import TooManyServersException, NotEnoughArgsException, LogsNumberException, \
    LogsFollowException, TooManyParamsException

result = None
CONTAINER_ID = 'f068b5bdb7af'


class MockConnector:

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get_logs(cls, container_id: str, logs_num: int = 10, follow: bool = False):
        global result
        result = (container_id, logs_num, follow)


class TestArgParser(unittest.TestCase):

    def setUp(self):
        global result
        result = None

    @patch('dmocker.Connector', MockConnector)
    def test_get_logs(self):
        sys.argv = ['main.py', 'server1', '-t', 'logs', CONTAINER_ID]
        main()
        self.assertTrue(result == (CONTAINER_ID, 10, False))

    @patch('dmocker.Connector', MockConnector)
    def test_get_logs_number(self):
        sys.argv = ['main.py', 'server1', '-t', 'logs', CONTAINER_ID, '20']
        main()
        self.assertTrue(result == (CONTAINER_ID, 20, False))

    @patch('dmocker.Connector', MockConnector)
    def test_get_logs_number_follow(self):
        sys.argv = ['main.py', 'server1', '-t', 'logs', CONTAINER_ID, '20', 'f']
        main()
        self.assertTrue(result == (CONTAINER_ID, 20, True))

    @patch('dmocker.Connector', MockConnector)
    def test_get_logs_many_servers(self):
        servers = ['server1', 'server2']
        sys.argv = ['main.py', *servers, '-t', 'logs']
        with self.assertRaises(TooManyServersException) as context:
            main()
        self.assertTrue(context.exception.args == TooManyServersException(servers).args)

    @patch('dmocker.Connector', MockConnector)
    def test_get_logs_missed_container_id(self):
        sys.argv = ['main.py', 'server1', '-t', 'logs']
        with self.assertRaises(NotEnoughArgsException) as context:
            main()
        self.assertTrue(context.exception.args == NotEnoughArgsException().args)

    @patch('dmocker.Connector', MockConnector)
    def test_get_logs_number_value_error(self):
        logs_number = '10s'
        sys.argv = ['main.py', 'server1', '-t', 'logs', CONTAINER_ID, logs_number]
        with self.assertRaises(LogsNumberException) as context:
            main()
        self.assertTrue(context.exception.args == LogsNumberException(logs_number).args)

    @patch('dmocker.Connector', MockConnector)
    def test_get_logs_follow_value_error(self):
        follow_value = 'true'
        sys.argv = ['main.py', 'server1', '-t', 'logs', CONTAINER_ID, '20', follow_value]
        with self.assertRaises(LogsFollowException) as context:
            main()
        self.assertTrue(context.exception.args == LogsFollowException(follow_value).args)

    @patch('dmocker.Connector', MockConnector)
    def test_get_logs_too_many_params(self):
        params = [CONTAINER_ID, '20', 'f', 'another_param']
        sys.argv = ['main.py', 'server1', '-t', 'logs', *params]
        with self.assertRaises(TooManyParamsException) as context:
            main()
        self.assertTrue(context.exception.args == TooManyParamsException(params).args)
