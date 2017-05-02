import re
from string_helper import getLeadingWhitespace, commasInArgs

PARSE_COMMAND_PATTERN = "((is something)|(else if)|([a-zA-Z]))\w+"
PARSE_GO_PATTERN = "(?i)\s*go\s+(\w+)\s+for\s+([\w\.]+)(\s+(\w+))?"
PARSE_TURN_PATTERN = "(?i)\s*turn\s+(\w+)\s+for\s+([\w\.]+)"
PARSE_WHILE_PATTERN = "(?i)\s*while\s+(.+):"
PARSE_IF_PATTERN = "(?i)\s*if\s+(.+):"
PARSE_ELIF_PATTERN = "(?i)\s*else\s+if\s+(.+):"
PARSE_STORE_PATTERN = "(?i)\s*store\s+(.*)\s+in\s+(\w+)"
PARSE_STORESTRING_PATTERN = "(?i)\s*store\s+\"(.*)\"\s+in\s+(\w+)"
PARSE_DISPLAY_PATTERN = "(?i)\s*display\s+(.+)"
PARSE_TASK_PATTERN = "(?i)\s*create\s+task\s+(\w+)(\s+using\s+(.*))?"
PARSE_EQUALS_PATTERN = "(?i)\s*(.+)\s*equals\?\s*(.+)"
PARSE_SET_PATTERN = "(?i)\s*set\s+(\w+)\s+to\s+(\w+)"
PARSE_RUN_PATTERN = "(?i)\s*run\s+(\w+)\s+with\s+(.*)"


def getCommand(line):
    match = re.search(PARSE_COMMAND_PATTERN, line)
    return match.group(0).lower()


def parseGo(line):
    match = re.search(PARSE_GO_PATTERN, line)
    if not match:
        raise Exception("Go line has improper syntax")
    direction = match.group(1)
    time = match.group(2)
    """
    units = match.group(3)
    if units:
        units = ", \"%s\""
    """
    return (direction, time)


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
    "Store <value> in <name>"
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
    "Display <value>/<name>"
    match = re.search(PARSE_DISPLAY_PATTERN, line)
    if not match:
            raise Exception("Display line has improper syntax")
    arg = match.group(1)
    return arg


def parseTask(line):
    "Create task <name> (using <param1> ... <paramN>)"
    match = re.search(PARSE_TASK_PATTERN, line)
    if not match:
        raise Exception("task line has improper syntax")
    name = match.group(1)
    params = match.group(2)
    return (name, commasInArgs(params))


def parseEquals(line):
    "<left> equals? <right>"
    match = re.search(PARSE_EQUALS_PATTERN, line)
    if not match:
            raise Exception("Equals line has improper syntax")
    left = match.group(1)
    right = match.group(2)
    return (left, right)


def parseSet(line):
    "Set <name> to <value>"
    match = re.search(PARSE_SET_PATTERN, line)
    if not match:
            raise Exception("Set line has improper syntax")
    name = match.group(1)
    value = match.group(2)
    return (name, value)

def parseRun(line):
    match = re.search(PARSE_RUN_PATTERN, line)
    if not match:
        raise Exception("Run line has improper syntax")
    method = match.group(1)
    args = match.group(2)
    return (method, commasInArgs(args))

class Writer:
    lines = []
    marks = []

    def mark(self):
        self.marks.append(len(self.lines))

    # indent = [""]
    def __init__(self, outputFileName):
        self.outputFileName = outputFileName
        self.fileOut = open(outputFileName, "w")
        self.inline = False

    def getPython(self, line):
        command = getCommand(line).lower()
        if re.search(".*times\s*", line):
            return ""
        if not command:
            return ""
        elif command == "go":
            return "controller.move(\"%s\", %s)" % parseGo(line)
        elif command == "turn":
            return "controller.turn(\"%s\", %s)" % parseTurn(line)
        elif command == "do":
            self.mark()
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
        elif command == "create":
            fun, args = parseTask(line)
            args = args.replace("using", "") if args else ""
            args = args.strip()
            return "def %s(%s):" % (fun,args)
        elif command == "equals?":
            return "%s == %s" % parseEquals(line)
        elif command == "set":
            return "%s = %s" % parseSet(line)
        elif command == "run":
            return "%s(%s)" % parseRun(line)
        elif command == "python:" or command == "python":
            assert 0==0
        else:
            return "#Failed to parse: %s" % line

    def convert(self, line):
        if self.inline:
            self.lines.append(getLeadingWhitespace(self.lines[-1]) + line.strip())
            return
        ws = getLeadingWhitespace(line)
        line = line.strip()
        self.lines.append(ws + self.getPython(line))


    def formatLine(self, *args):
        if not self.marks:
            raise Exception("Cannot format a non existing line")
        i = self.marks.pop()
        self.lines[i] = self.lines[i] % args
        return self.lines[i]
        # def popLine():
        #     if lines[-1].rstrip()[-1] == ":":
        #         indent.pop()
        #     lines.pop()

    def printLines(self):
        for line in self.lines:
            print(line)

    def close(self):
        self.fileOut.write("from RobotController import controller\n")
        for line in self.lines:
            self.fileOut.write(line + "\n")
        self.fileOut.close()