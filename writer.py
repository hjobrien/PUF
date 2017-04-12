import re
from string_helper import getLeadingWhitespace
def getCommand(line):
    match = re.search("(is something)|(else if)|[a-zA-Z]\w+")
	return match.lower()

def parseGo(line):
	match = re.search("(?i)\s*go\s+(\w+)\s+for\s+([\w\.]+)(\s+(\w+))?", line)
	if not match:
		raise Exception("Go line has improper syntax")
	direction = match.group(1)
	time = match.group(2)
	units = match.group(3)
	if units:
		units = ", \"%s\"" % units
	return "self.move(\"%s\", new Duration(%s%s))" % direction, time, units

def parseTurn(line):
	match = re.search("(?i)\s*turn\s+(\w+)\s+degrees\s+([\w\.]+)", line)
	if not match:
		raise Exception("Turn line has improper syntax")
	angle = match.group(1)
	direction = match.group(2)
	return "self.move(%s, %s)" % angle, direction

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
			elif command == "go":
				return parseGo(line)
			elif command == "turn":
				return parseTurn(line)
            return ""
		ws = getLeadingWhitespace(line)
		line = line.strip()
		lines.append(ws + parse(line))

    # def popLine():
    #     if lines[-1].rstrip()[-1] == ":":
    #         indent.pop()
    #     lines.pop()
