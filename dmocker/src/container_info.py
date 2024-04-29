"""
Configuration for the information about each container.
"""


class Columns:
    ID_COLUMN_WIDTH = 30
    IMAGE_COLUMN_WIDTH = 40
    STATUS_COLUMN_WIDTH = 30


class ContainerInfo:

    def __init__(self, info):
        self.info = info

    @property
    def id(self):
        return self.info['Id'][:12]

    @property
    def image(self):
        if len(self.info['Image']) > Columns.IMAGE_COLUMN_WIDTH - 10:
            return self.info['Image'][:Columns.IMAGE_COLUMN_WIDTH - 10] + '...'
        return self.info['Image']

    @property
    def status(self):
        return self.info['Status']

    @property
    def name(self):
        return self.info['Names'][0].replace('/', '')
