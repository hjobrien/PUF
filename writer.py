import re
from string_helper import getLeadingWhitespace
def getCommand(line):
    match = re.search("(is something)|(else if)|[a-zA-Z]\w+")

def parseGo(line):
	match = re.search("(?i)\s*go\s+(\w+)\s+for\s+([\w\.]+)(\s+(\w+))?", s)
	if not match:
		raise Exception("Go line has improper syntax")
	direction = match.group(1)
	time = match.group(2)
	units = match.group(3)
	if units:
		units = ", \"%s\"" % units
	return "self.move(\"%s\", new Duration(%s%s))" % direction, time, units


class Writer:
    lines = []
    # indent = [""]
    def __init__(outputFileName):
        this.outputFileName = outputFileName

    def convert(line):
        def parse(line):
			command = getCommand(line).lower()
			if not command:
				return ""
			elif command == "go"

            return ""
		ws = getLeadingWhitespace(line)
		line = line.strip()
		lines.append(ws + parse(line))

    # def popLine():
    #     if lines[-1].rstrip()[-1] == ":":
    #         indent.pop()
    #     lines.pop()
