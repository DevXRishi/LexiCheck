"""Character-by-character lexer for the small LexiCheck language."""

from dataclasses import dataclass, asdict


@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

    def to_dict(self):
        return asdict(self)


KEYWORDS = {"int", "float", "char", "if", "else", "while", "print"}
TWO_CHAR_OPERATORS = {"==", "!=", "<=", ">=", "&&", "||"}
ONE_CHAR_OPERATORS = set("+-*/%=<>!")
DELIMITERS = set("(){};,")


def tokenize(source):
    """Return (tokens, errors); each error has message, line, and column."""
    tokens, errors = [], []
    i, line, column, length = 0, 1, 1, len(source)

    def advance():
        nonlocal i, line, column
        ch = source[i]
        i += 1
        if ch == "\n":
            line, column = line + 1, 1
        else:
            column += 1
        return ch

    while i < length:
        ch = source[i]
        if ch in " \t\r\n":
            advance()
            continue
        start_line, start_col = line, column
        if ch == "/" and i + 1 < length and source[i + 1] == "/":
            while i < length and source[i] != "\n":
                advance()
            continue
        if ch.isalpha() or ch == "_":
            start = i
            while i < length and (source[i].isalnum() or source[i] == "_"):
                advance()
            value = source[start:i]
            tokens.append(Token("KEYWORD" if value in KEYWORDS else "IDENTIFIER", value, start_line, start_col))
            continue
        if ch.isdigit():
            start = i
            while i < length and source[i].isdigit():
                advance()
            kind = "INTEGER"
            if i < length and source[i] == ".":
                kind = "FLOAT"
                advance()
                if i >= length or not source[i].isdigit():
                    # Consume adjacent numeric dots so malformed forms report once.
                    while i < length and (source[i].isdigit() or source[i] == "."):
                        advance()
                    value = source[start:i]
                    errors.append({"message": f"Malformed numeric literal '{value}'.", "line": start_line, "column": start_col})
                    continue
                while i < length and source[i].isdigit():
                    advance()
                if i < length and source[i] == ".":
                    while i < length and (source[i].isdigit() or source[i] == "."):
                        advance()
                    value = source[start:i]
                    errors.append({"message": f"Malformed numeric literal '{value}'.", "line": start_line, "column": start_col})
                    continue
            tokens.append(Token(kind, source[start:i], start_line, start_col))
            continue
        if ch in ('"', "'"):
            quote = advance()
            start = i
            closed = False
            while i < length:
                if source[i] == "\\":
                    advance()
                    if i < length:
                        advance()
                    continue
                if source[i] == quote:
                    closed = True
                    break
                if source[i] == "\n":
                    break
                advance()
            value = source[start:i]
            if closed:
                advance()
                if quote == "'" and len(value) != 1:
                    errors.append({"message": "Character literal must contain exactly one character.", "line": start_line, "column": start_col})
                else:
                    tokens.append(Token("STRING" if quote == '"' else "CHARACTER", value, start_line, start_col))
            else:
                errors.append({"message": f"Unterminated {'string' if quote == chr(34) else 'character'} literal.", "line": start_line, "column": start_col})
            continue
        pair = source[i:i + 2]
        if pair in TWO_CHAR_OPERATORS:
            advance(); advance()
            tokens.append(Token("OPERATOR", pair, start_line, start_col))
        elif ch in ONE_CHAR_OPERATORS:
            advance()
            tokens.append(Token("OPERATOR", ch, start_line, start_col))
        elif ch in DELIMITERS:
            advance()
            tokens.append(Token("DELIMITER", ch, start_line, start_col))
        else:
            advance()
            errors.append({"message": f"Invalid character {ch!r}.", "line": start_line, "column": start_col})
    return tokens, errors
