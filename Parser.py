
#%%
def parse(tokens):
    tree = []

    tokens.extend([" ", " "])

    index = 0
    while index < len(tokens):
        offset = 1

        if tokens[index] in "+-><.,":
            tree.append(tokens[index])

        elif "#" in tokens[index] and "*" in tokens[index+2]:
            while tokens[index+offset] is not ")":
                offset+=1
            params = [p for p in "".join(tokens[index+2:index+offset]).split("*") 
                if p is not ""]
            par_off = offset
            offset += 1
            if tokens[index+offset] is not "{":
                return
            closed = 0
            offset+=1
            while closed < 1:
                if tokens[index+offset] is "}":
                    closed += 1
                if tokens[index+offset] is "{":
                    closed -= 1
                offset+=1
            body = parse(tokens[index+par_off: index+offset])
            tree.append(["D", tokens[index][1:], params, body])

        elif ":" in tokens[index] and tokens[index+1] is "(":
            while tokens[index+offset] is not ")":
                offset+=1
            params = [p for p in "".join(tokens[index+2:index+offset]).split("*") 
                if p is not ""]
            tree.append(["F", tokens[index][1:], params])

        elif tokens[index] == "#" or tokens[index] == "@":
            while tokens[index+offset] in "0123456789":
                offset+=1
            tree.append([tokens[index], "".join(tokens[index+1:index+offset])])

        elif "#" in tokens[index] or "@" in tokens[index] or "*" in tokens[index]:
            tree.append([tokens[index][0], tokens[index][1:]])

        elif tokens[index] in "0123456789$%":
            while tokens[index+offset] in "0123456789":
                if tokens[index] in "$%":
                    break
                offset+=1
            num_off = offset
            while tokens[index+offset] != "(" and tokens[index+offset] not in "+-><":
                offset+=1
            str_off = offset
            if tokens[index+offset] == "(":
                closed = 0
                offset+=1
                while closed < 1:
                    if tokens[index+offset] is ")":
                        closed += 1
                    if tokens[index+offset] is "(":
                        closed -= 1
                    offset+=1
                token_type = tokens[index] if tokens[index] in "$%" else "N"
                sec_off = num_off if num_off == str_off else str_off
                tree.append([token_type, "".join(tokens[index:index+sec_off]), 
                    parse(tokens[index+num_off:index+offset])])
            if tokens[index+1] in "+-><":
                tree.append(["N", *tokens[index:index+offset+1]])
                offset+=1

        elif tokens[index] == "[":
            while tokens[index+offset] is not "]":
                offset+=1
            tree.append(["W", parse(tokens[index+1:index+offset+1])])

        elif "\"" in tokens[index]:
            tree.append(["S", tokens[index][1:-1]])

        elif tokens[index] in "!?":
            if tokens[index+offset] == "{":
                closed = 0
                offset+=1
                while closed < 1:
                    if tokens[index+offset] is "}":
                        closed += 1
                    if tokens[index+offset] is "{":
                        closed -= 1
                    offset+=1
            tree.append([tokens[index], parse(tokens[index+2:index+offset-1])])

        index+=offset

    return tree
# %%
