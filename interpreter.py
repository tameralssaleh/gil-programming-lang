from nodes import *

class Interpreter:
    def __init__(self):
        self.variables = {}  # symbol table | DONT USE THIS


    def visit(self, node):
        """Dispatch method based on node type"""
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode): 
            return node.value
        elif isinstance(node, CharNode):
            return node.value
        elif isinstance(node, BooleanNode):
            return self.eval_boolean(node.value)
        elif isinstance(node, IdentifierNode):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise NameError(f"Undefined variable '{node.name}'")
        # elif isinstance(node, NullableIdentifierNode):
        #     if node.name in self.variables:
        #         return self.variables[node.name]
        #     else:
        #         return None
        elif isinstance(node, BinOpNode):
            left = self.visit(node.left)
            right = self.visit(node.right)
            return self.eval_binop(left, node.op, right)
        elif isinstance(node, UnaryOpNode):
            value = self.visit(node.operand)
            if node.op == "NOT":
                return not value
            else:
                raise ValueError(f"Unknown unary operator {node.op}")

        elif isinstance(node, DefineNode):
            value = self.visit(node.value)
            self.variables[node.name] = value
            return value
        elif isinstance(node, AssignNode):
            value = self.visit(node.value)
            if node.name in self.variables:
                self.variables[node.name] = value
                return value
            else:
                raise NameError(f"Undefined variable '{node.name}' must be defined before assignment.")
        else:
            raise TypeError(f"Unknown node type: {type(node)}")

    def eval_binop(self, left, op, right):
        if op == "ADD":
            return left + right
        elif op == "SUB":
            return left - right
        elif op == "MUL":
            return left * right
        elif op == "DIV":
            return left / right
        elif op == "FDIV":
            return left // right
        elif op == "MOD":
            return left % right
        elif op == "EQ":
            return left == right
        elif op == "NEQ":
            return left != right
        elif op == "LT":
            return left < right
        elif op == "LTE":
            return left <= right
        elif op == "GT":
            return left > right
        elif op == "GTE":
            return left >= right
        elif op == "AND":
            return bool(left) and bool(right)
        elif op == "OR":
            return bool(left) or bool(right)
        elif op == "NOT":
            return not left
        else:
            raise ValueError(f"Unknown operator {op}")
        
    def eval_boolean(self, value):
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            raise ValueError(f"Invalid boolean value: {value}")