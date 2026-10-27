# LexiCheck — Lexical Analyzer & Syntax Checker

LexiCheck is a small web application for exploring the front end of a compiler. Enter a simplified C-like program to see the tokens found by a character-by-character lexer and whether a recursive-descent parser accepts the program's syntax. Submitted code is never executed.

## Problem statement

Compiler front ends turn a character stream into tokens and then check whether those tokens follow a language grammar. This project makes those two stages visible to a Computer Engineering student and reports errors in terms of source locations.

## Objectives and features

- Recognize keywords, identifiers, integer and floating-point literals, strings, characters, operators, and delimiters.
- Ignore whitespace and `//` line comments while keeping line and column locations.
- Check declarations, assignments, expressions, blocks, `if`/`else`, `while`, and `print` statements.
- Show token counts and readable lexical and syntax diagnostics.
- Keep Flask as a thin request layer; all scanning and parsing use Python code and the standard library.

## Technology stack

- Python 3 and Flask
- HTML5, CSS3, and vanilla JavaScript
- Python `unittest`

## Folder structure

```text
LexiCheck/
├── app.py
├── lexer.py
├── parser.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/index.html
├── static/style.css
├── static/script.js
└── tests/
    ├── test_lexer.py
    └── test_parser.py
```

## Prerequisites and Windows setup

Install Python 3 from [python.org](https://www.python.org/downloads/) and enable the option to add Python to PATH. In VS Code, open the `LexiCheck` folder and open **Terminal → New Terminal**. The commands below use PowerShell.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, allow scripts for the current terminal session with `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. Alternatively run the environment's interpreter without activation: `\.venv\Scripts\python.exe -m pip install -r requirements.txt`.

Start the application from the project folder:

```powershell
python app.py
```

Open **http://127.0.0.1:5000** in a browser. Stop the development server with `Ctrl+C`.

## Tests

Run the standard-library test suite from the project folder:

```powershell
python -m unittest discover -s tests -v
```

## Supported language and grammar

The language has `int`, `float`, `char`, `if`, `else`, `while`, and `print` keywords. It supports identifiers, decimal and integer literals, string and one-character literals, `//` comments, arithmetic, comparison and logical operators, and `(){};,` delimiters.

EBNF-style overview (the parser uses the same precedence levels for expressions):

```text
program       = { statement } ;
statement     = declaration | assignment | print | if | while | block ;
declaration   = ("int" | "float" | "char"), identifier, ["=", expression], ";" ;
assignment    = identifier, "=", expression, ";" ;
print         = "print", "(", expression, ")", ";" ;
if            = "if", "(", expression, ")", statement, ["else", statement] ;
while         = "while", "(", expression, ")", statement ;
block         = "{", { statement }, "}" ;
expression    = logical_or ;
logical_or    = logical_and, { "||", logical_and } ;
logical_and   = comparison, { "&&", comparison } ;
comparison    = additive, [ ("==" | "!=" | "<" | ">" | "<=" | ">="), additive ] ;
additive      = term, { ("+" | "-"), term } ;
term          = unary, { ("*" | "/" | "%"), unary } ;
unary         = ["!" | "+" | "-"], primary ;
primary       = identifier | number | string | character | "(", expression, ")" ;
```

## Example inputs and outputs

Choose **Load Valid Example**, then **Analyze Code**. It contains declarations, arithmetic precedence, print, an if-else, and a while loop; expected output is no lexical or syntax errors.

The **Load Error Example** button loads the requested malformed syntax sample:

```c
int age = 20
int result = age + ;
if (age > 18 {
    print(age);
}
```

It reports missing semicolon and expression/condition syntax errors. To inspect the lexical case, replace the editor contents with this standalone sample:

```c
int number = 12.3.4;
int result = @5;
```

It reports a malformed numeric literal and an invalid character. When lexical errors exist the parser is skipped, so syntax counts are intentionally zero and the UI does not claim syntax validation.

## Limitations

This is an educational syntax checker, not full C. It does not implement functions, arrays, pointers, declarations with multiple variables, increment operators, or preprocessor directives. It does not perform type checking, symbol-table checks, semantic analysis, code generation, or program execution. Conditions use the same expression grammar as other expressions; grammar checks are syntactic only.

## Possible future improvements

- Add line/column highlighting in the editor.
- Add more unit tests for malformed input and parser recovery.
- Add a grammar view that illustrates the parser's precedence levels.
