import unittest

from lexer import tokenize


class LexerTests(unittest.TestCase):
    def test_keywords_and_identifiers(self):
        tokens, errors = tokenize("int counter; print(counter);")
        self.assertEqual(errors, [])
        self.assertEqual([(t.type, t.value) for t in tokens[:3]],
                         [("KEYWORD", "int"), ("IDENTIFIER", "counter"), ("DELIMITER", ";")])

    def test_numbers(self):
        tokens, errors = tokenize("42 12.5")
        self.assertEqual(errors, [])
        self.assertEqual([(t.type, t.value) for t in tokens], [("INTEGER", "42"), ("FLOAT", "12.5")])

    def test_operators_and_delimiters(self):
        tokens, errors = tokenize("a<=3 && b!=2; { }")
        self.assertEqual(errors, [])
        self.assertIn(("OPERATOR", "<="), [(t.type, t.value) for t in tokens])
        self.assertIn(("OPERATOR", "&&"), [(t.type, t.value) for t in tokens])
        self.assertIn(("DELIMITER", "{"), [(t.type, t.value) for t in tokens])

    def test_strings_and_characters(self):
        tokens, errors = tokenize('"hello" \'x\'')
        self.assertEqual(errors, [])
        self.assertEqual([t.type for t in tokens], ["STRING", "CHARACTER"])

    def test_comment_and_line_tracking(self):
        tokens, errors = tokenize("int a; // ignored\nprint(a);")
        self.assertEqual(errors, [])
        self.assertEqual(tokens[-1].line, 2)

    def test_invalid_character(self):
        tokens, errors = tokenize("int a = @;")
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["line"], 1)
        self.assertEqual(errors[0]["column"], 9)

    def test_unterminated_string(self):
        _, errors = tokenize('"unfinished')
        self.assertIn("Unterminated string", errors[0]["message"])

    def test_malformed_number(self):
        tokens, errors = tokenize("12.3.4")
        self.assertEqual(tokens, [])
        self.assertIn("Malformed numeric literal", errors[0]["message"])


if __name__ == "__main__":
    unittest.main()
