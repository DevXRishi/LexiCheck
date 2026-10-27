const VALID_EXAMPLE = `int age = 20;
float price = 12.5;
int result = age + 5 * 2;
print(result);

if (age >= 18) {
    print(age);
} else {
    print(0);
}

while (age < 25) {
    age = age + 1;
}`;

const SYNTAX_EXAMPLE = `int age = 20
int result = age + ;
if (age > 18 {
    print(age);
}`;

const LEXICAL_EXAMPLE = `int number = 12.3.4;
int result = @5;`;
const editor = document.querySelector('#source-code');
const results = document.querySelector('#results');
const message = document.querySelector('#request-message');
const analyzeButton = document.querySelector('#analyze-button');

document.querySelector('#valid-example').addEventListener('click', () => { editor.value = VALID_EXAMPLE; message.textContent = ''; });
document.querySelector('#error-example').addEventListener('click', () => { editor.value = SYNTAX_EXAMPLE; message.textContent = ''; });
document.querySelector('#clear-button').addEventListener('click', () => { editor.value = ''; results.hidden = true; message.textContent = ''; });
analyzeButton.addEventListener('click', analyzeCode);

function make(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

async function analyzeCode() {
  analyzeButton.disabled = true;
  message.className = 'request-message';
  message.textContent = 'Analyzing source code…';
  try {
    const response = await fetch('/analyze', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source_code: editor.value })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'The server could not analyze this request.');
    renderResults(data);
    message.textContent = '';
  } catch (error) {
    message.className = 'request-message error';
    message.textContent = `Could not reach the analyzer. ${error.message} Check that Flask is running, then try again.`;
  } finally {
    analyzeButton.disabled = false;
  }
}

function renderResults(data) {
  results.hidden = false;
  const summary = data.summary;
  const badge = document.querySelector('#result-badge');
  badge.textContent = data.success ? 'VALID PROGRAM' : 'ISSUES FOUND';
  badge.className = data.success ? 'result-badge' : 'result-badge invalid';
  const cards = [
    ['Total tokens', summary.total_tokens, false], ['Keywords', summary.keywords, false],
    ['Identifiers', summary.identifiers, false], ['Operators', summary.operators, false],
    ['Delimiters', summary.delimiters, false], ['Lexical errors', summary.lexical_errors, summary.lexical_errors > 0],
    ['Syntax errors', summary.syntax_errors, summary.syntax_errors > 0]
  ];
  const grid = document.querySelector('#summary-grid');
  grid.replaceChildren(...cards.map(([label, count, alert]) => {
    const card = make('div', `summary-card${alert ? ' alert' : ''}`);
    card.append(make('span', '', label), make('strong', '', String(count)));
    return card;
  }));

  document.querySelector('#token-count').textContent = `${data.tokens.length} TOKENS`;
  const body = document.querySelector('#token-rows');
  body.replaceChildren();
  for (const [index, token] of data.tokens.entries()) {
    const row = document.createElement('tr');
    const typeClass = token.type.toLowerCase();
    [String(index + 1), token.value, token.type, String(token.line), String(token.column)].forEach((value, cellIndex) => {
      const cell = document.createElement('td');
      cell.textContent = value;
      if (cellIndex === 1) cell.className = 'token-value';
      if (cellIndex === 2) cell.className = `token-type ${typeClass}`;
      row.append(cell);
    });
    body.append(row);
  }
  document.querySelector('#no-tokens').hidden = data.tokens.length !== 0;
  renderErrors('#lexical-errors', '#lexical-count', data.lexical_errors);
  renderErrors('#syntax-errors', '#syntax-count', data.syntax_errors);
  const success = document.querySelector('#success-message');
  success.hidden = !data.success;
  success.textContent = data.success ? '✓ No lexical or syntax errors. The program matches the supported grammar.' : '';
  results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderErrors(listSelector, countSelector, errors) {
  const list = document.querySelector(listSelector);
  document.querySelector(countSelector).textContent = String(errors.length);
  list.replaceChildren();
  if (!errors.length) {
    list.append(make('li', 'empty-error', 'No errors found.'));
    return;
  }
  for (const error of errors) {
    const item = make('li', 'error-item');
    const location = `Line ${error.line}${error.column == null ? '' : `, column ${error.column}`}`;
    item.append(make('span', 'error-location', location), document.createTextNode(error.message));
    list.append(item);
  }
}
