
from ply import lex

reserved = (
    "VAR",
    "FUNC",
    "IF",
    "ELSE",
    "FOR",
    "RETURN",
    "TRUE",
    "FALSE",
    "NIL",
    "STRUCT",
    "NEW",
    "TRY",
    "CATCH",
    "RAISE",
)

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

tokens = reserved + (
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "COMMA",
    "COLON",
    "SEMI",
    "EQ",
    "NOT_EQ",
    "GREATER_EQ",
    "GREATER",
    "LESS_EQ",
    "LESS",
    "ASSIGN",
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "NUMBER",
    "NAME",
    "STRING",
    "AND",
    "OR",
    "NOT",
    "DOT",
)

t_ignore = " \t"

literals = [
    "=",
    "+",
    "-",
    "*",
    "/",
    "(",
    ")",
    ",",
    "{",
    "}",
    ";",
    ">",
    "<",
    '"',
    ".",
    "!",
    "@",
]

# Tokens

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_COMMA = r","
t_COLON = r":"
t_SEMI = r";"
t_EQ = r"=="
t_GREATER_EQ = r">="
t_GREATER = r">"
t_LESS_EQ = r"<="
t_LESS = r"<"
t_NOT_EQ = r"!="
t_ASSIGN = r"="
t_PLUS = r"\+"
t_MINUS = r"\-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"/"
t_AND = r"&&"
t_OR = r"\|\|"
t_NOT = r"!"
t_DOT = r"."


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_NAME(t):
    r"[A-Za-z_][\w_]*"
    t.type = reserved_map.get(t.value, "NAME")
    return t

def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_comment(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")


def t_STRING(t):
    r'".*?"'
    t.value = t.value[1:-1]
    return t


def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

def reset_lineno():
    lexer.lineno = 1

# Build the lexer
lexer = lex.lex()
