"""
Test options to get the list of containers.
"""
import sys
import unittest
from unittest.mock import patch

from dmocker import main
from dmocker.exceptions.custom import WrongFlagException

result = None
GET_RUNNING_MSG = 'get running containers'
GET_ALL_MSG = 'get all containers'

"""
tasks (params): ps (a: None, a), logs (container_id: id; tail: 10, N; follow: None, f)  
"""


class MockConnector:

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get_containers(cls, all_containers=False):
        global result
        if all_containers:
            result = GET_ALL_MSG
        else:
            result = GET_RUNNING_MSG


class TestArgParser(unittest.TestCase):

    def setUp(self):
        global result
        result = None

    @patch('dmocker.Connector', MockConnector)
    def test_get_running_containers(self):
        sys.argv = ['main.py'] + ['server1', 'server2']
        main()
        self.assertTrue(result == GET_RUNNING_MSG)

    @patch('dmocker.Connector', MockConnector)
    def test_get_running_containers_task(self):
        sys.argv = ['main.py'] + ['server1', 'server2', '-t', 'ps']
        main()
        self.assertTrue(result == GET_RUNNING_MSG)

    @patch('dmocker.Connector', MockConnector)
    def test_get_all_containers(self):
        sys.argv = ['main.py'] + ['server1', 'server2', '-t', 'ps', 'a']
        main()
        self.assertTrue(result == GET_ALL_MSG)

    @patch('dmocker.Connector', MockConnector)
    def test_get_containers_wrong_flag(self):
        flag = 'b'
        sys.argv = ['main.py'] + ['server1', 'server2', '-t', 'ps', flag]
        with self.assertRaises(WrongFlagException) as context:
            main()
        self.assertTrue(context.exception.args == WrongFlagException(flag).args)
