
#%%
from functools import partial
import sys

def interpret(tree):
    global memory
    global ptr
    global variables
    global functions
    memory = [0]
    ptr = 0
    variables = {}
    functions = {}

    memory_size = 2**16-1

    def add(n): 
        if memory[ptr] + n > memory_size:
            memory[ptr] = memory[ptr] + n - (memory_size+1)
        elif memory[ptr] + n < 0:
            memory[ptr] = (memory_size+1) - memory[ptr] + n
        else:
             memory[ptr] += n

    def move(n):
        global ptr
        if ptr + n >= len(memory):
            num = len(memory)-ptr+n
            memory.extend(([0]*num))
            ptr += n
        elif ptr + n < 0:
            ptr = (ptr + n) % len(memory)
        else:
            ptr += n

    def uni_input():
        string = input("")
        #string = string[0] if len(string) > 1 else string
        for s in string:
            uni = ord(s)
            memory[ptr] = uni
            move(1)

    def log():
        char = chr(memory[ptr])
        sys.stdout.write(char)
    
    def assign(name):
        variables[name] = ptr
    
    def goto(name, tmp, _):
        global ptr
        if name.isdigit():
            #ptr = name
            move(int(name)-ptr)
        elif name in tmp:
            #ptr = tmp[name]
            move(tmp[name]-ptr)
        elif name in variables:
            #ptr = variables[name]
            move(variables[name]-ptr)
        else: #Name is "here"
            return

    def declare(name, arguments, code):
        functions[name] = {
            "arguments": arguments,
            "code": code
        }

    def call(name, arguments, scope, iter_index):
        arguments = [ptr if arg == "here" else 
            int(arg) if arg.isdigit() else 
                variables[arg] if arg in variables else
                scope[arg] for arg in arguments]
        function = functions[name]
        scope_variables = {name:arg for name, arg in zip(function["arguments"], arguments)}
        final_scope = {**scope, **scope_variables}
        run(function["code"], final_scope, iter_index)

    def repeat(reps, code, scope, iter_index):
        for i in range(int(reps)):
            run(code, scope, i)

    def repeat_mem(name, code, scope, iter_index):
        if len(name) == 1:
            repeat(memory[ptr], code, scope, iter_index)
        elif name[1:] in variables:
            repeat(memory[variables[name[1:]]], code, scope, iter_index)
        else:
            repeat(memory[scope[name[1:]]], code, scope, iter_index)

    def repeat_iter(code, scope, iter_index):
        repeat(iter_index, code, scope, iter_index)

    def while_loop(code, scope, iter_index):
        index = 0
        while memory[ptr] is not 0:
            run(code, scope, index)
            index+=1

    #Rest of the loops

    def ternary(cond, code, scope, iter_index):
        if (memory[ptr] == 0) == cond:
            run(code, scope, iter_index)

    def string(content):
        for char in content:
            memory[ptr] = ord(char)
            move(1)
        move(-1)

    def run(instructions, scope, iter_index):
        for instr in instructions:
            {
                "+": partial(add, 1),
                "-": partial(add, -1),
                "<": partial(move, -1),
                ">": partial(move, 1),
                ",": partial(uni_input),
                ".": partial(log),
                "#": partial(assign, instr[1]) 
                    if len(instr) > 1 else 0,
                "@": partial(goto, instr[1], scope, iter_index) 
                    if len(instr) > 1 else 0,
                "N": partial(repeat, instr[1], instr[2], scope, iter_index)
                    if len(instr) > 2 else 0,
                "$": partial(repeat_mem, instr[1], instr[2], scope, iter_index) 
                    if len(instr) > 2 else 0,
                "%": partial(repeat_iter, instr[2], scope, iter_index) 
                    if len(instr) > 2 else 0,
                "W": partial(while_loop, instr[1], scope, iter_index) 
                    if len(instr) > 1 else 0,
                "S": partial(string, instr[1]) 
                    if len(instr) > 1 else 0,
                "D": partial(declare, *instr[1:]) 
                    if len(instr) > 3 else 0,
                "F": partial(call, instr[1], instr[2], scope, iter_index) 
                    if len(instr) > 2 else 0,
                "*": partial(goto, instr[1], scope, iter_index) 
                    if len(instr) > 1 else 0,
                "?": partial(ternary, False, instr[1], scope, iter_index)
                    if len(instr) > 1 else 0,
                "!": partial(ternary, True, instr[1], scope, iter_index)
                    if len(instr) > 1 else 0,
            }[instr[0]]()

    run(tree, {}, 0)
    
    return memory
    

# %%
