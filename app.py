"""Flask interface for LexiCheck. Submitted programs are analyzed, never run."""

from flask import Flask, jsonify, render_template, request

from lexer import tokenize
from parser import parse

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("source_code"), str):
        return jsonify({"error": "Send a JSON object with a string 'source_code' field."}), 400
    tokens, lexical_errors = tokenize(data["source_code"])
    syntax_errors = [] if lexical_errors else parse(tokens)
    summary = {
        "total_tokens": len(tokens),
        "keywords": sum(token.type == "KEYWORD" for token in tokens),
        "identifiers": sum(token.type == "IDENTIFIER" for token in tokens),
        "operators": sum(token.type == "OPERATOR" for token in tokens),
        "delimiters": sum(token.type == "DELIMITER" for token in tokens),
        "lexical_errors": len(lexical_errors),
        "syntax_errors": len(syntax_errors),
    }
    return jsonify({"tokens": [token.to_dict() for token in tokens], "lexical_errors": lexical_errors,
                    "syntax_errors": syntax_errors, "summary": summary,
                    "success": not lexical_errors and not syntax_errors})


if __name__ == "__main__":
    app.run(debug=True)
