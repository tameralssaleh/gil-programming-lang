
class Env(object):
    def __init__(self, variables=None):
        if variables is None:
            variables = {}
        self.variables = variables