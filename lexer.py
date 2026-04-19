import ply.lex as lex

# Keywords definition
reserved = {
    'MODEL': 'MODEL',
    'INPUT': 'INPUT',
    'FEATURE': 'FEATURE',
    'extract': 'EXTRACT',
    'TRAIN': 'TRAIN',
    'model': 'R_MODEL',
    'USING': 'USING',
    'threshold': 'R_THRESHOLD',
    'THRESHOLD': 'THRESHOLD',
    'IF': 'IF',
    'ELSE': 'ELSE',
    'THEN': 'THEN',
    'ALERT': 'ALERT',
    'LOG': 'LOG'
}

# List of token names
tokens = [
    'IDENTIFIER',
    'NUMBER',
    'STRING_LITERAL',
    'GT',
    'LT',
    'EQ',
    'COMMA'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_GT = r'>'
t_LT = r'<'
t_EQ = r'=='
t_COMMA = r','

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"[^"]*"'
    t.value = t.value[1:-1] # Remove quotes
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\r'

# Error handling rule
def t_error(t):
    print(f"Lexical error: Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
