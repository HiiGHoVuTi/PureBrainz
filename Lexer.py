
#%%
import re
def lex(text):
    tokens = []
    #exp = r"\+|\-|\<|\>|\[|\]|\{|\}|\(|\)|#|.|@|[0-9]|=|~|/|:|\?|\!|\*|,|[a-z]|[A-Z]|§|$|\""
    #stripped = "".join(re.findall(exp, text))
    
    stripped = re.sub(r"\|", "", text)
    clean = []
    string_allowed = 0
    val_char = "+-<>[]{}()0123456789=~/?!.,$%"
    for char in stripped:
        if char in "@#*\"$:":
            clean.append(char)
            string_allowed = 1
            if char is '"':
                string_allowed = 2
        elif string_allowed is 2:
            string_allowed = 2
            clean.append(char)
        elif char in val_char:
            clean.append(char)
            string_allowed = 0
        elif string_allowed is 1:
            if char == " ":
                string_allowed = 0
                continue
            string_allowed = 1
            clean.append(char)
        
    clean = "".join(clean)
    clean+=" "
    index = 0
    while index < len(clean):
        if clean[index] == " ":
            index+=1
            continue
        if clean[index] in val_char:
            tokens.append(clean[index])
        elif clean[index] is '"':
            base = index
            index+=1
            while clean[index] is not '"':
                index+=1
            tokens.append(clean[base:index+1])
        else:
            buffer = ""
            buffer+=clean[index]
            index+=1
            while clean[index] not in val_char+"*":
                buffer += clean[index]
                index+=1
                if index >= len(clean):
                    break
                if clean[index] in "@#\":":
                    #index+=1
                    break
            tokens.append(buffer)
            #if clean[index-1] in "@#":
            #    tokens.append(clean[index-1])
            continue
        index+=1
    tokens = [re.sub(r"\s+", "", t) if "\"" not in t else t for t in tokens]
    tokens = [t for t in tokens if t != ""]
    return tokens

# %%
