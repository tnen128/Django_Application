# kpi_app/utils.py

class CustomInterpreter:
    """Custom interpreter to evaluate arithmetic expressions and regex-like patterns."""

    OPERATORS = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y
    }

    def evaluate_expression(self, expression, attr_value):
        """Evaluates arithmetic expressions with ATTR substitution and supports regex-like matching."""
        if expression.startswith("Regex("):
            return self.evaluate_regex(expression, attr_value)
        return self.evaluate_arithmetic(expression, attr_value)

    def evaluate_arithmetic(self, expression, attr_value):
        """Evaluates arithmetic expressions with ATTR substitution."""
        expression = expression.replace("ATTR", str(attr_value))
        tokens = self.tokenize(expression)
        return self.parse_tokens(tokens)

    def evaluate_regex(self, expression, attr_value):
        """Custom regex-like matching without using regex library."""
        # Extract pattern from Regex(ATTR, 'pattern')
        _, pattern = expression.split("Regex(ATTR, '")
        pattern = pattern.rstrip("')")
        return "True" if self.custom_match(str(attr_value), pattern) else "False"

    def custom_match(self, string, pattern):
        """Simple pattern matching function to support wildcards."""
        if '*' in pattern:
            start, end = pattern.split('*')
            return string.startswith(start) and string.endswith(end)
        return string == pattern

    def tokenize(self, expression):
        """Tokenizes arithmetic expressions into components."""
        return expression.replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ').split()

    def parse_tokens(self, tokens):
        """Evaluates a tokenized arithmetic expression."""
        result = float(tokens.pop(0))
        while tokens:
            op = tokens.pop(0)
            num = float(tokens.pop(0))
            result = self.OPERATORS[op](result, num)
        return result
