"""
Test options to get the list of containers.
"""
import sys
import unittest
from unittest.mock import patch

from dmocker import main
from dmocker.exceptions.custom import WrongFlagException, TooManyFlagsException

result = None
GET_RUNNING_MSG = 'get running containers'
GET_ALL_MSG = 'get all containers'
GET_RUNNING_FILTERED_MSG = 'get running containers filtered by name'
GET_ALL_FILTERED_MSG = 'get all containers filtered by name'


class MockConnector:

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get_containers(cls, all_containers: bool = False, name: str = ''):
        global result
        if all_containers:
            result = GET_ALL_FILTERED_MSG if name else GET_ALL_MSG
        else:
            result = GET_RUNNING_FILTERED_MSG if name else GET_RUNNING_MSG


class TestArgParser(unittest.TestCase):

    def setUp(self):
        global result
        result = None

    @patch('dmocker.Connector', MockConnector)
    def test_get_running_containers(self):
        sys.argv = ['main.py', 'server1', 'server2']
        main()
        self.assertTrue(result == GET_RUNNING_MSG)

    @patch('dmocker.Connector', MockConnector)
    def test_get_running_filtered_containers(self):
        sys.argv = ['main.py', 'server1', 'server2', '-n', 'container_name']
        main()
        self.assertTrue(result == GET_RUNNING_FILTERED_MSG)

    @patch('dmocker.Connector', MockConnector)
    def test_get_running_containers_task(self):
        sys.argv = ['main.py', 'server1', 'server2', '-t', 'ps']
        main()
        self.assertTrue(result == GET_RUNNING_MSG)

    @patch('dmocker.Connector', MockConnector)
    def test_get_running_containers_filtered_task(self):
        sys.argv = ['main.py', 'server1', 'server2', '-t', 'ps', '-n', 'container_name']
        main()
        self.assertTrue(result == GET_RUNNING_FILTERED_MSG)

    @patch('dmocker.Connector', MockConnector)
    def test_get_all_containers(self):
        sys.argv = ['main.py', 'server1', 'server2', '-t', 'ps', 'a']
        main()
        self.assertTrue(result == GET_ALL_MSG)

    @patch('dmocker.Connector', MockConnector)
    def test_get_all_containers_filtered(self):
        sys.argv = ['main.py', 'server1', 'server2', '-t', 'ps', 'a', '-n', 'container_name']
        main()
        self.assertTrue(result == GET_ALL_FILTERED_MSG)

    @patch('dmocker.Connector', MockConnector)
    def test_get_containers_wrong_flag(self):
        flag = 'b'
        sys.argv = ['main.py', 'server1', 'server2', '-t', 'ps', flag]
        with self.assertRaises(WrongFlagException) as context:
            main()
        self.assertTrue(context.exception.args == WrongFlagException(flag).args)

    @patch('dmocker.Connector', MockConnector)
    def test_get_containers_too_many_flags(self):
        flags = ['a', 'b']
        sys.argv = ['main.py', 'server1', 'server2', '-t', 'ps', *flags]
        with self.assertRaises(TooManyFlagsException) as context:
            main()
        self.assertTrue(context.exception.args == TooManyFlagsException(flags).args)
