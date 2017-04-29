import re

def getLeadingWhitespace(str):
    length = len(str) - len(str.lstrip())
    return str[:length]

def whitespaceValid(line, indentation, startOfBlock):
    ws = getLeadingWhitespace(line)
    prev = indentation[-1]
    if startOfBlock:
        return len(prev) < len(ws) and prev == ws[:len(prev)]
    else:
        indentation = indentation[:] #Don't want to modify the original
        while len(ws) < len(prev) and indentation:
            prev = indentation.pop()
        return prev == ws

def commasInArgs(args):
    #Spec changed, this is easiest fix
    return args

def processComments(line):
    return re.sub("#.*", "", line)