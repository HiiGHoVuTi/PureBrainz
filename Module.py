
#%%
import re
def modules(code):
    parts = [re.sub(r"\s+", "", p) for p in code.split("|") if "~" in p]

    out = code

    for p in parts:
        if "/" in p:
            module_name = p[1:p.index("/")]
            function_name = p[p.index("/")+1:]
            module_name = module_name+".pb" if "." not in module_name else module_name
            with open(module_name) as m:
                m = m.read()
                index = m.index(function_name)
                #CHANGE THIS
                end = m[index:].index("}")
                out = out.replace(p, m[index-1:end+2])
        else:
            module_name = p[1:]
            module_name = module_name+".pb" if "." not in module_name else module_name
            with open(module_name) as m:
                m = m.read()
                out = out.replace(p, m)

    if "~" in out:
        out = modules(out) + out

    return out

# %%
