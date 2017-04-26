import re
from string_helper import getLeadingWhitespace

PARSE_COMMAND_PATTERN = "((is something)|(else if)|([a-zA-Z]))\w+"
PARSE_GO_PATTERN = "(?i)\s*go\s+(\w+)\s+for\s+([\w\.]+)(\s+(\w+))?"
PARSE_TURN_PATTERN = "(?i)\s*turn\s+(\w+)\s+degrees\s+([\w\.]+)"
PARSE_WHILE_PATTERN = "(?i)\s*while\s+(.+):"
PARSE_IF_PATTERN = "(?i)\s*if\s+(.+):"
PARSE_ELIF_PATTERN = "(?i)\s*else\s+if\s+(.+):"
PARSE_STORE_PATTERN = "(?i)\s*store\s+(\w+)\s+in\s+(\w+)"
PARSE_STORESTRING_PATTERN = "(?i)\s*store\s+\"(\w+)\"\s+in\s+(\w+)"
PARSE_DISPLAY_PATTERN = "(?i)\s*display\s+(.+)"
PARSE_TASK_PATTERN = "(?i)\s*create\s+task\s+(\w+)\s+\(+using\s+(.*)\)"
PARSE_EQUALS_PATTERN = "(?i)\s*(.+)\s*equals\?\s*(.+)"
PARSE_SET_PATTERN = "(?i)\s*set\s+(\w+)\s+to\s+(\w+)"


def getCommand(line):
    match = re.search(PARSE_COMMAND_PATTERN, line)
    return match.group(0).lower()


def parseGo(line):
    match = re.search(PARSE_GO_PATTERN, line)
    if not match:
        raise Exception("Go line has improper syntax")
    direction = match.group(1)
    time = match.group(2)
    units = match.group(3)
    if units:
        units = ", \"%s\"" % units
    return (direction, time, units)


def parseTurn(line):
    match = re.search(PARSE_TURN_PATTERN, line)
    if not match:
        raise Exception("Turn line has improper syntax")
    angle = match.group(1)
    direction = match.group(2)
    return (angle, direction)

def parseWhile(line):
    match = re.search(PARSE_WHILE_PATTERN, line)
    if not match:
        raise Exception("While line has improper syntax")
    arg = match.group(1)
    return arg


def parseIf(line):
    match = re.search(PARSE_IF_PATTERN, line)
    if not match:
        raise Exception("If line has improper syntax")
    arg = match.group(1)
    return arg


def parseElseIf(line):
    match = re.search(PARSE_ELIF_PATTERN, line)
    if not match:
        raise Exception("else if line has improper syntax")
    arg = match.group(1)
    return arg


def parseStore(line):
    match1 = re.search(PARSE_STORE_PATTERN, line)
    match2 = re.search(PARSE_STORESTRING_PATTERN, line)
    if not match1 and not match2:
        raise Exception("store line has improper syntax")
    if match1:
        value = match1.group(1)
        name = match1.group(2)
        return (name, value)
    else:
        value = match2.group(1)
        name = match2.group(2)
        return (name, value)


def parseDisplay(line):
    match = re.search(PARSE_DISPLAY_PATTERN, line)
    if not match:
            raise Exception("Display line has improper syntax")
    arg = match.group(1)
    return arg


def parseTask(line):
    match = re.search(PARSE_TASK_PATTERN, line)
    if not match:
        raise Exception("task line has improper syntax")
    name = match.group(1)
    params = match.group(2)
    return (name, params)


def parseEquals(line):
    match = re.search(PARSE_EQUALS_PATTERN, line)
    if not match:
            raise Exception("Equals line has improper syntax")
    left = match.group(1)
    right = match.group(2)
    return (left, right)


def parseSet(line):
    match = re.search(PARSE_SET_PATTERN, line)
    if not match:
            raise Exception("Set line has improper syntax")
    name = match.group(1)
    value = match.group(2)
    return (name, value)


class Writer:
    lines = []

    # indent = [""]
    def __init__(self, outputFileName):
        self.outputFileName = outputFileName

    def getPython(self, line):
        command = getCommand(line).lower()
        if not command:
            return ""
        elif command == "go":
            return "self.move(\"%s\", new Duration(%s%s))" % parseGo(line)
        elif command == "turn":
            return "self.move(%s, %s)" % parseTurn(line)
        elif command == "do":
            return "for _ in range(%s):"
        elif command == "while":
            return "while %s:" % parseWhile(line)
        elif command == "if":
            return "if %s" % parseIf(line)
        elif command == "elif":
            return "elif %s" % parseElseIf(line)
        elif command == "else":
            return "else:"
        elif command == "store":
            return "%s = %s" % parseStore(line)
        elif command == "display":
            return "print(%s)" % parseDisplay(line)
        elif command == "task":
            return "def %s(%s):" % parseTask(line)
        else:
            return "Failed to parse: %s" % line

    def convert(self, line):
        ws = getLeadingWhitespace(line)
        line = line.strip()
        self.lines.append(ws + self.getPython(line))

    def formatLine(self, i, *args):
        if i >= len(self.lines):
            raise Exception("Cannot format a non existing line")
        self.lines[i] = self.lines[i] % args
        return self.lines[i]
        # def popLine():
        #     if lines[-1].rstrip()[-1] == ":":
        #         indent.pop()
        #     lines.pop()

    def printLines(self):
        for line in self.lines:
            print(line)
