import re
from nodes import *

class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f"Token<kind:{self.kind}, value:{self.value}>"

class Lexer:
    def __init__(self):
        self.position = 0
        self.current_char = None
        self.text = ""
        self.tokens = []
        self.token_specs = [
            ("DEFINE", r"DEFINE"),
            ("TYPE", r"INT|FLOAT|STRING|CHAR"),
            ("NUMBER", r"\d+(\.\d*)?"),
            ("STRING", r'"[^"]*"'),
            ("CHAR", r"'.'"),
            ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
            ("ASSIGN", r"="),
            ("COMMENT", r";"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("COMMA", r","),
            ("ADD", r"\+"),
            ("SUB", r"-"),
            ("MUL", r"\*"),
            ("DIV", r"/"),
            ("FDIV", r"//"),
            ("WHITESPACE", r"\s+"),
            ("NEWLINE", r"\n")
        ]

        self.token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in self.token_specs)

    def tokenize(self, text):
        # Remove semicolon comments
        text = re.sub(r";[^\n]*", "", text)
        self.text = text
        self.position = 0
        self.tokens = []

        for match in re.finditer(self.token_regex, text):
            kind = match.lastgroup
            value = match.group()
            if kind in ("WHITESPACE", "NEWLINE"):
                continue
            elif kind == "NUMBER":
                value = float(value) if '.' in value else int(value)
            elif kind == "STRING":
                value = value[1:-1]  # Remove quotes
            elif kind == "CHAR":
                value = value[1]  # Remove quotes
            self.tokens.append(Token(kind, value))

        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self) -> Token:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, kind):
        token: Token = self.current_token()
        if token and token.kind == kind:
            self.position += 1
            return token
        raise SyntaxError(f"Expected token {kind}, got {token}")

    # --- Parsing entry point ---
    def parse(self):
        token: Token = self.current_token()
        if token is None:
            return None

        if token.kind == "DEFINE":
            return self.parse_define()
        else:
            return self.parse_expr()

    # --- DEFINE num INT 301 ---
    def parse_define(self):
        self.eat("DEFINE")
        name = self.eat("IDENTIFIER").value
        type_token = self.eat("TYPE").value
        value_node = self.parse_expr()
        return DefineNode(name, type_token, value_node)

    # --- Expression grammar ---
    # expr   -> term ((ADD|SUB) term)*
    # term   -> factor ((MUL|DIV|FDIV) factor)*
    # factor -> NUMBER | IDENTIFIER | '(' expr ')'

    def parse_expr(self):
        node = self.parse_term()
        while self.current_token() and self.current_token().kind in ("ADD", "SUB"):
            op = self.eat(self.current_token().kind).kind
            right = self.parse_term()
            node = BinOpNode(node, op, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token() and self.current_token().kind in ("MUL", "DIV", "FDIV"):
            op = self.eat(self.current_token().kind).kind
            right = self.parse_factor()
            node = BinOpNode(node, op, right)
        return node

    def parse_factor(self):
        token = self.current_token()

        if token.kind == "NUMBER":
            self.eat("NUMBER")
            return NumberNode(token.value)
        elif token.kind == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return IdentifierNode(token.value)
        elif token.kind == "STRING":
            self.eat("STRING")
            return StringNode(token.value)
        elif token.kind == "CHAR":
            self.eat("CHAR")
            return CharNode(token.value)
        elif token.kind == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_expr()
            self.eat("RPAREN")
            return node
        else:
            raise SyntaxError(f"Unexpected token {token}")
        
class Interpreter:
    def __init__(self):
        self.variables = {}  # symbol table

    def visit(self, node):
        """Dispatch method based on node type"""
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, CharNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise NameError(f"Undefined variable '{node.name}'")
        elif isinstance(node, BinOpNode):
            left = self.visit(node.left)
            right = self.visit(node.right)
            return self.eval_binop(left, node.op, right)
        elif isinstance(node, DefineNode):
            value = self.visit(node.value)
            self.variables[node.name] = value
            return value
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
        elif op == "=":  # for DEFINE expressions if used as BinOpNode
            return right
        else:
            raise ValueError(f"Unknown operator {op}")

lexer = Lexer()

example = "4 + 5 * (3 - 1) / 2"

tokens = lexer.tokenize(example)
print("Tokens:", tokens)
parser = Parser(tokens)
ast = parser.parse()
print("AST:", ast)

interp = Interpreter()
interp.visit(ast) 
print("Result:", interp.visit(ast))