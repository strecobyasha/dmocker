

class ContainerInfo:

    def __init__(self, info):
        self.info = info

    @property
    def id(self):
        return self.info['Id'][:12]

    @property
    def image(self):
        return self.info['Image']

    @property
    def status(self):
        return self.info['Status']

    @property
    def name(self):
        return self.info['Names'][0].replace('/', '')
