from string_helper import getLeadingWhitespace, whitespaceValid
from writer import getCommand, Writer
from json_helper import toJson, JsonLine
import re

inFileName = "samplecode.hlf"
outFileName = "hankisverycool.py"
jsonFileName = "hankisverycool.json"


# out = open(outFileName, "w")
# out.write("import library")
def _main():
    indentation = [""]
    prevRelLine = [None]  # Previous relevant line
    startOfBlock = False
    line_no = 1

    writer = Writer(outFileName)
    jOut = open(jsonFileName, "w")

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
            assert temp == None or temp[0] not in ["do"], "Error, failed to properly close \"%s\" on line %i" % (temp[0], temp[1])
        if prevRelLine[-1] != None and prevRelLine[-1][0] == "do":
            writer.formatLine(prevRelLine[-1][1], re.search("\d+", line).group())
            # TODO: Go back to the latest Do statement and fill in the params of the for loop
        else:
            writer.convert(line)
            jsonObj = toJson(line)
            jsonObj.id = line_no
            jsonObj.prev = line_no - 1  #Dis shit is hacked together as fuck
            jsonObj.indent = len(ws)
            jOut.write(jsonObj)

        if prevRelLine[-1] != None:
            prevRelLine.pop()
        command = getCommand(line)
        # print(prevRelLine[-2] if len(prevRelLine) > 1 else "Top")
        line_no += 1
        startOfBlock = startsBlock(command)
        if startOfBlock:
            prevRelLine.append((command, line_no))

    writer.printLines()
    writer.close()
    jOut.close()


_blockStarters = ["create", "python:", "do", "if", "else", "else if", "python"]


def startsBlock(command):
    return command.lower() in _blockStarters


_main()
