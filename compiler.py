from string_helper import getLeadingWhitespace, whitespaceValid
from writer import getCommand
import re

inFileName = "samplecode.hlf"
outFileName = "samplecode.py"


# out = open(outFileName, "w")
# out.write("import library")
def _main():
    indentation = [""]
    prevRelLine = [None]  # Previous relevant line
    startOfBlock = False
    line_no = 1

    for line in open(inFileName, "r"):
        if not len(line.strip()):
            continue

        assert whitespaceValid(line, indentation, startOfBlock), "Error: Invalid whitespace on line: %i" % line_no
        if startOfBlock:
            indentation.append(getLeadingWhitespace(line))
            prevRelLine.append(None)
        ws = getLeadingWhitespace(line)
        while indentation and ws != indentation[-1]:
            indentation.pop()
            temp = prevRelLine.pop()
            assert temp == None, "Error, failed to properly close %s" % temp
        if prevRelLine[-1] != None and [-1][0] == "Do":
            0 == 0
            # TODO: Go back to the latest Do statement and fill in the params of the for loop
        if prevRelLine[-1] != None:
            prevRelLine.pop()

        command = getCommand(line)

        line_no += 1
        startOfBlock = startsBlock(command)
        if startOfBlock:
            t = (command, line_no)
            prevRelLine.append(t)


_blockStarters = ["create", "python:", "do", "if", "else", "else if"]


def startsBlock(command):
    return command.lower() in _blockStarters


_main()
