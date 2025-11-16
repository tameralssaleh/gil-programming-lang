
class Env(object):
    def __init__(self, variables=None, functions=None, parent=None):
        self.variables = variables or {} # Store nested dicts as "name": {"type": type, "value": value}
        self.functions = functions or {}
        self.parent = parent or None

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            raise NameError(f"Variable '{name}' not found")

    def set_variable(self, name, value):
        self.variables[name] = value
