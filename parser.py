"""Recursive-descent syntax checker for LexiCheck's educational grammar."""


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.errors = []

    def current(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def value(self):
        token = self.current()
        return token.value if token else None

    def report(self, message, token=None):
        token = token or self.current()
        self.errors.append({"message": message, "line": token.line if token else (self.tokens[-1].line if self.tokens else 1),
                            "column": token.column if token else None})

    def match(self, value):
        if self.value() == value:
            self.position += 1
            return True
        return False

    def expect(self, value, message=None):
        if not self.match(value):
            self.report(message or f"Expected '{value}'.")
            return False
        return True

    def parse_program(self):
        while self.current():
            old = self.position
            self.parse_statement()
            if self.position == old:
                self.report("Unexpected token; unable to continue.")
                self.position += 1
        return self.errors

    def parse_statement(self):
        token = self.current()
        if not token:
            return
        if token.value in ("int", "float", "char"):
            self.parse_declaration()
        elif token.value == "if":
            self.parse_if_statement()
        elif token.value == "while":
            self.parse_while_statement()
        elif token.value == "print":
            self.parse_print_statement()
        elif token.value == "{":
            self.parse_block()
        elif token.type == "IDENTIFIER":
            self.parse_assignment()
        else:
            self.report(f"Unexpected token '{token.value}' at start of statement.", token)
            self.position += 1

    def parse_block(self):
        self.expect("{")
        while self.current() and self.value() != "}":
            old = self.position
            self.parse_statement()
            if old == self.position:
                self.position += 1
        self.expect("}", "Missing closing brace '}'.")

    def parse_declaration(self):
        self.position += 1  # type keyword
        if not self.current() or self.current().type != "IDENTIFIER":
            self.report("Expected an identifier after the type keyword.")
            self.recover_statement()
            return
        self.position += 1
        if self.match("="):
            self.parse_expression()
        self.expect(";", "Missing semicolon after declaration.")

    def parse_assignment(self):
        self.position += 1
        if not self.expect("=", "Expected '=' in assignment."):
            self.recover_statement()
            return
        self.parse_expression()
        self.expect(";", "Missing semicolon after assignment.")

    def parse_print_statement(self):
        self.position += 1
        self.expect("(", "Expected '(' after print.")
        self.parse_expression()
        self.expect(")", "Missing closing parenthesis after print expression.")
        self.expect(";", "Missing semicolon after print statement.")

    def parse_if_statement(self):
        self.position += 1
        self.expect("(", "Expected '(' after if.")
        self.parse_expression()
        self.expect(")", "Missing closing parenthesis after if condition.")
        self.parse_statement()
        if self.match("else"):
            self.parse_statement()

    def parse_while_statement(self):
        self.position += 1
        self.expect("(", "Expected '(' after while.")
        self.parse_expression()
        self.expect(")", "Missing closing parenthesis after while condition.")
        self.parse_statement()

    def recover_statement(self):
        while self.current() and self.value() not in (";", "}"):
            self.position += 1
        self.match(";")

    def parse_expression(self):
        self.parse_or()

    def parse_or(self):
        self.parse_and()
        while self.match("||"):
            self.parse_and()

    def parse_and(self):
        self.parse_comparison()
        while self.match("&&"):
            self.parse_comparison()

    def parse_comparison(self):
        self.parse_additive()
        while self.value() in ("==", "!=", "<", ">", "<=", ">="):
            self.position += 1
            self.parse_additive()

    def parse_additive(self):
        self.parse_multiplicative()
        while self.value() in ("+", "-"):
            self.position += 1
            self.parse_multiplicative()

    def parse_multiplicative(self):
        self.parse_unary()
        while self.value() in ("*", "/", "%"):
            self.position += 1
            self.parse_unary()

    def parse_unary(self):
        if self.value() in ("!", "+", "-"):
            self.position += 1
            self.parse_unary()
        else:
            self.parse_primary()

    def parse_primary(self):
        token = self.current()
        if not token:
            self.report("Missing operand.")
        elif token.type in ("IDENTIFIER", "INTEGER", "FLOAT", "STRING", "CHARACTER"):
            self.position += 1
        elif self.match("("):
            self.parse_expression()
            self.expect(")", "Missing closing parenthesis in expression.")
        else:
            self.report(f"Invalid expression: unexpected token '{token.value}'.", token)
            # Leave statement delimiters for their owning parse method.
            if token.value not in (";", ")", "}", "{"):
                self.position += 1


def parse(tokens):
    return Parser(tokens).parse_program()
