import unittest

from lexer import tokenize
from parser import parse


def syntax_errors(source):
    tokens, lexical = tokenize(source)
    if lexical:
        raise AssertionError(f"Unexpected lexical errors: {lexical}")
    return parse(tokens)


class ParserTests(unittest.TestCase):
    def test_valid_declarations(self):
        self.assertEqual(syntax_errors("int age = 20; float price = 12.5; char initial = 'A';"), [])

    def test_valid_assignment(self):
        self.assertEqual(syntax_errors("age = age + 1;"), [])

    def test_arithmetic_precedence_and_parentheses(self):
        self.assertEqual(syntax_errors("int result = (a + 2) * 3 % 5;"), [])

    def test_if_else(self):
        self.assertEqual(syntax_errors("if (age >= 18 && ready || !blocked) { print(age); } else print(0);"), [])

    def test_while(self):
        self.assertEqual(syntax_errors("while (age < 25) { age = age + 1; }"), [])

    def test_print(self):
        self.assertEqual(syntax_errors("print(value + 2);"), [])

    def test_missing_semicolon(self):
        self.assertTrue(any("semicolon" in e["message"] for e in syntax_errors("int age = 20")))

    def test_missing_parenthesis(self):
        self.assertTrue(any("parenthesis" in e["message"] for e in syntax_errors("if (a > 2 { print(a); }")))

    def test_missing_brace(self):
        self.assertTrue(any("brace" in e["message"] for e in syntax_errors("while (a < 3) { a = a + 1;")))

    def test_invalid_expression(self):
        self.assertTrue(syntax_errors("int value = 4 + ;"))

    def test_prompt_valid_example(self):
        source = """int age = 20;
float price = 12.5;
int result = age + 5 * 2;
print(result);
if (age >= 18) { print(age); } else { print(0); }
while (age < 25) { age = age + 1; }"""
        self.assertEqual(syntax_errors(source), [])


if __name__ == "__main__":
    unittest.main()
