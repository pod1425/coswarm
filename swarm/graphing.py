import math
import re

import numpy as np


class MathExpression:

    def __init__(self, expression):
        self.expression = expression
        self.tokens = self._tokenize(expression)  # Tokenize input
        print(self.tokens)
        self.postfix = self._shunting_yard(self.tokens)  # Convert to postfix notation
        print(self.postfix)
        self.variables = {}  # Stores values for variables

    def set_variable(self, var, value):
        """Assigns a value to a variable."""
        if len(var) == 1 and var.isalpha():
            self.variables[var] = value
        else:
            raise ValueError("Variable names must be single lowercase letters.")

    def evaluate(self):
        """Evaluates the expression using postfix notation."""
        stack = []

        for token in self.postfix:
            if re.match(r"^\d+(\.\d+)?$", token):  # Numeric token (integer or float)
                stack.append(float(token))  # Convert string to float
            elif re.match(r"^[a-z]$", token):  # Variable (single letter)
                if token in self.variables:
                    stack.append(self.variables[token])
                else:
                    raise ValueError(f"Variable '{token}' is not set.")
            elif token in {"+", "-", "*", "/", "^"}:  # Operators
                if len(stack) < 2:
                    raise ValueError("Invalid expression.")
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                elif token == "/":
                    stack.append(a / b)
                elif token == "^":
                    stack.append(a ** b)
            elif token in {"sin", "cos", "tan", "ctg", "abs", "log", "sqrt"}:  # Functions
                if not stack:
                    raise ValueError("Invalid expression.")
                x = stack.pop()
                if token == "sin":
                    stack.append(math.sin(x))
                elif token == "cos":
                    stack.append(math.cos(x))
                elif token == "tan":
                    stack.append(math.tan(x))
                elif token == "ctg":
                    stack.append(1 / math.tan(x))
                elif token == "abs":
                    stack.append(abs(x))
                elif token == "log":
                    stack.append(math.log(x))  # Natural log (log base e)
                elif token == "sqrt":
                    stack.append(math.sqrt(x))  # Square root
            else:
                raise ValueError(f"Unknown token: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression.")

        return stack[0]

    def _tokenize(self, expression):
        """Splits a mathematical expression string into tokens, supporting functions and variables."""
        # Updated token pattern to catch valid functions and variables
        token_pattern = r"\d+\.\d+|\d+|[a-z]+|sin|cos|tan|ctg|abs|log|sqrt|[+\-*/^()]"

        # Find all the tokens
        tokens = re.findall(token_pattern, expression.replace(" ", ""))

        # Check for invalid multi-letter tokens
        for token in tokens:
            if len(token) > 1 and token not in {'abs', 'log', 'sqrt', 'sin', 'cos', 'tan', 'ctg', '+', '-', '*', '/',
                                                '^', '(', ')'}:
                raise ValueError(f"Invalid token: {token}")

        return tokens

    def _shunting_yard(self, tokens):
        """Converts infix tokens to postfix notation, supporting functions, variables, and operators."""
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}  # Left or right associative
        functions = {'sin', 'cos', 'tan', 'ctg', 'abs', 'log', 'sqrt'}

        output_queue = []
        operator_stack = []

        for token in tokens:
            if re.match(r"^\d+(\.\d+)?$", token):  # Number
                output_queue.append(token)
            elif re.match(r"^[a-z]$", token):  # Variable (single letter)
                output_queue.append(token)
            elif token in functions:  # Function (sin, cos, tan, ctg, abs, log, sqrt)
                operator_stack.append(token)
            elif token in precedence:  # Operator
                while (operator_stack and operator_stack[-1] != '(' and
                       operator_stack[-1] != '|'
                       and (precedence.get(operator_stack[-1], 0) > precedence[token] or
                            (precedence.get(operator_stack[-1], 0) == precedence[token] and associativity[
                                token] == 'L'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':  # Left parenthesis
                operator_stack.append(token)
            elif token == ')':  # Right parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()  # Remove '(' from stack

        while operator_stack:  # Pop remaining operators
            output_queue.append(operator_stack.pop())

        return output_queue


def get_graph_points(fx, x_start, x_end, num_points):
    x_values = np.linspace(x_start, x_end, num_points, dtype=int)
    expr = MathExpression(fx)
    y_values = []
    for x in x_values:
        expr.set_variable("x", x)
        y_values.append(expr.evaluate())

    # Return list of coordinate pairs
    return list(zip(x_values, y_values))

def approx_equals(ideal: float, actual: float, tolerance: float):
    return ideal - tolerance < actual < ideal + tolerance
