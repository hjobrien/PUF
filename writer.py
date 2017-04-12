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

def parseDoWhile(line):
	return "for _ in range(%s):"

def parseWhile(line):
	match = re.search("(?i)\s*while\s+(.+):", line)
	if not match:
		raise Exception("While line has improper syntax")
	arg = match.group(1)
	return "while %s:" % arg



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
			elif command == "do":
				return parseDoWhile(line)
			elif command == "while":
				return parseWhile(line)
            return ""
		ws = getLeadingWhitespace(line)
		line = line.strip()
		lines.append(ws + parse(line))

	def formatLine(i, *args):
		if i >= len(lines):
			raise Exception("Cannot format a non existing line")
		lines[i] = lines[i] % args
		return lines[i]
    # def popLine():
    #     if lines[-1].rstrip()[-1] == ":":
    #         indent.pop()
    #     lines.pop()
