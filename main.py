from parser import Parser
from lexer import Lexer
from interpreter import Interpreter

lexer = Lexer()
interpreter = Interpreter()

example_code: list[str] = [
    "define num1 int 7",
    "define x int 10",
    "define y int 20",
    "define num1 int 55"
    "assign num1 100 ; reassign num1 to 100",
    "(x + y) * 2",
    "define result int (x + y) * 2",
    "5 && 4"
    "1 || 0"
    "0 || 0"
    "true && false"
    "define is_valid bool true"
]

def format_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


for ex in example_code:
    try:
        tokens = lexer.tokenize(ex)
        parser = Parser(tokens)
        ast = parser.parse()
        result = interpreter.visit(ast)
        print(format_value(result))
    except Exception as e:
        result = f"Error: {e}"
        print(result)

