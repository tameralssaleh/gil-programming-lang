
class Env(object):
    def __init__(self, variables=None, functions=None):
        self.variables = variables or {}
        self.functions = functions or {}

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            raise NameError(f"Variable '{name}' not found")

    def set_variable(self, name, value):
        self.variables[name] = value