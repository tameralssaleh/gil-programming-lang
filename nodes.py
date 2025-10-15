class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
        self.type_ = "INT" if isinstance(value, int) else "FLOAT"

    def __repr__(self):
        return f"NumberNode({self.type_}:{self.value})"

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode({self.name})"
    
class NullableIdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"NullableIdentifierNode({self.name})"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringNode({self.value})"
    
class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"BooleanNode({self.value})"

class CharNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"CharNode({self.value})"
    
class DefineNode(ASTNode):
    def __init__(self, name, type_, value):
        self.name = name
        self.type_ = type_
        self.value = value

class AssignNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"DefineNode(name={self.name}, type={self.type_}, value={self.value})"

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"
    
class UnaryOpNode:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
