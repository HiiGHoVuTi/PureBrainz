
#%%
import sys
with open(sys.argv[1]) as f:
    code = f.read()

#%%
from Module import modules
from Lexer import lex
from Parser import parse
from Interpreter import interpret

#%%
def evaluate(code):
    code = modules(code)
    return interpret(parse(lex(code)))


def main(x):
    evaluate(x)

#%%
if __name__ == "__main__":
    main(code)
# %%
