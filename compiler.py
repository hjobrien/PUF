from string_helper import getLeadingWhitespace, whitespaceValid, processComments
from writer import getCommand, Writer
from json_helper import toJson, JsonLine
import re

inFileName = "complicated_example"
outFileName = "hivc.py"
jsonFileName = "hivc.json"

# out = open(outFileName, "w")
# out.write("import library")
def _main():
    indentation = [""]
    prevRelLine = [None]  # Previous relevant line
    startOfBlock = False
    line_no = 1

    writer = Writer(outFileName)
    jOut = open(jsonFileName, "w")
    jOut.write("[")

    for line in open(inFileName, "r"):
        if not len(line.strip()):
            continue
        line = processComments(line)
        if line_no != 1:
            jOut.write(",")
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
            writer.formatLine(line.replace("times", "").strip())
        elif prevRelLine[-1] != None and prevRelLine[-1][0] == "python":
            writer.inline = False
        else:
            try:
                writer.convert(line)
            except Exception:
                # print("Error parsing line: %i" % line_no)
                assert 0==0
            if not writer.inline:
                jsonObj = toJson(line)
                jsonObj.id = line_no
                jsonObj.prev = line_no - 1  #Dis shit is hacked together as fuck
                jsonObj.indent = len(ws)
                jOut.write(str(jsonObj))

        if prevRelLine[-1] != None:
            prevRelLine.pop()
        try:
            command = getCommand(line)
        except Exception:
            # print("Error parsing line: %i" % line_no)
            assert 0 == 0
        if command == "python":
            writer.inline = True
        # print(prevRelLine[-2] if len(prevRelLine) > 1 else "Top")
        startOfBlock = startsBlock(command)
        if startOfBlock:
            prevRelLine.append((command, line_no))
        line_no += 1


    # writer.printLines()
    writer.close()
    jOut.write("]")
    jOut.close()


_blockStarters = ["create", "python:", "do", "if", "else", "else if", "python"]


def startsBlock(command):
    return command.lower() in _blockStarters


_main()
