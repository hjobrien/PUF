import re
def getCommand(line):
    match = re.search("(is something)|(else if)|[a-zA-Z]\w+")

class Writer:
    lines = []
    indent = [""]
    def __init__(outputFileName):
        this.outputFileName = outputFileName

    def convert(line):
        def parse(line):
            return ""
    

    def popLine():
        if lines[-1].rstrip()[-1] == ":":
            indent.pop()
        lines.pop()
