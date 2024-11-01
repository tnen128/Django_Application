# kpi_app/interpreter.py

import re
import shlex
from .interfaces import ExpressionEvaluator

class ASTNode:
    """Base class for AST nodes."""
    pass

class UnaryOp(ASTNode):
    """AST node for unary operators (e.g., -x)."""
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class BinOp(ASTNode):
    """AST node for binary operators (e.g., x + y)."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(ASTNode):
    """AST node for numbers."""
    def __init__(self, value):
        self.value = value

class RegexOp(ASTNode):
    """AST node for regex matching."""
    def __init__(self, pattern):
        self.pattern = pattern

class CustomInterpreter(ExpressionEvaluator):
    """Interpreter that evaluates arithmetic and regex expressions with AST support."""

    def __init__(self):
        # Define operator precedence
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }

    def evaluate_expression(self, expression, attr_value):
        """Entry point to evaluate expressions with ATTR replacement."""
        try:
            # Check if expression includes 'Regex'
            if "Regex(" in expression:
                return self.evaluate_regex(expression, attr_value)
            
            # Handle arithmetic by replacing ATTR and tokenizing
            expression = expression.replace("ATTR", str(attr_value))
            if re.match(r"^[\d+\-*/().\s]+$", expression):  # Simplify if expression is basic arithmetic
                return eval(expression)

            # Otherwise, parse and evaluate with AST
            tokens = self.tokenize(expression)
            ast = self.parse(tokens)
            return self.evaluate_ast(ast)

        except Exception as e:
            raise ValueError(f"Error evaluating expression: {e}")

    def evaluate_regex(self, expression, attr_value):
        """Evaluate regex expressions with full regex support."""
        match = re.match(r"Regex\(ATTR, '(.+?)'\)", expression)
        if match:
            pattern = match.group(1)
            try:
                regex_ast = RegexOp(pattern)
                return self.evaluate_ast(regex_ast, attr_value)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {pattern} - {e}")
        raise ValueError("Invalid regex expression format")

    def tokenize(self, expression):
        """Tokenize the expression into numbers, operators, and parentheses."""
        tokens = shlex.split(expression)
        return [token for token in tokens if token]

    def parse(self, tokens):
        """Parse tokens into an AST with precedence handling."""
        def parse_expression(precedence=0):
            node = parse_primary()
            while tokens and tokens[0] in self.precedence and self.precedence[tokens[0]] >= precedence:
                op = tokens.pop(0)
                next_precedence = self.precedence[op] + 1
                right = parse_expression(next_precedence)
                node = BinOp(left=node, op=op, right=right)
            return node

        def parse_primary():
            if not tokens:
                raise ValueError("Unexpected end of expression")
            token = tokens.pop(0)
            if token.isdigit() or '.' in token:
                return Num(float(token))
            elif token == '(':
                node = parse_expression()
                if not tokens or tokens.pop(0) != ')':
                    raise ValueError("Mismatched parentheses")
                return node
            elif token == '-':
                return UnaryOp('-', parse_primary())
            else:
                raise ValueError(f"Unexpected token: {token}")

        return parse_expression()

    def evaluate_ast(self, node, attr_value=None):
        """Evaluate the AST recursively based on node type."""
        if isinstance(node, Num):
            return node.value
        elif isinstance(node, UnaryOp):
            expr_val = self.evaluate_ast(node.expr)
            return -expr_val if node.op == '-' else expr_val
        elif isinstance(node, BinOp):
            left_val = self.evaluate_ast(node.left)
            right_val = self.evaluate_ast(node.right)
            if node.op == '+':
                return left_val + right_val
            elif node.op == '-':
                return left_val - right_val
            elif node.op == '*':
                return left_val * right_val
            elif node.op == '/':
                if right_val == 0:
                    raise ValueError("Division by zero error")
                return left_val / right_val
            else:
                raise ValueError(f"Unknown operator: {node.op}")
        elif isinstance(node, RegexOp):
            return "True" if re.fullmatch(node.pattern, str(attr_value)) else "False"
        else:
            raise ValueError(f"Unknown AST node: {type(node)}")
