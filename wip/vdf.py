def to_dict(vdf):
    if vdf.endswith('.vdf'):
        with open(vdf,'r') as f:
            vdf = f.read(vdf)

    splited = vdf.replace('\n','').replace('\t','').split('"')
    splited.remove('')


    newl = []
    iss = False
    for el in splited:
        if el == '{':
            newl.append(':')
            newl.append(el)
        elif el == '}':
            iss = False
            newl.append(el)
            newl.append(',')
        elif el == '':
            if iss:
                newl.append(',')
            else:
                newl.append(':')
            iss = not iss
        else:
            newl.append(f'"{el}"')

    dicstr=''
    for el in newl:
        dicstr +=el
    dicstr = dicstr.replace('""','"').replace('}"','}')

    return eval('{'+dicstr+'}')
