

class IndentManager:

    def __init__(self):
        self.indentRecord = [0]
        self._opensBlock = False
        self._new_block = False
        self._blockStarters = ["create", "python:", "do", "if", "else", "else if"]

    def getIndentLevel(self):
        """
        :return: a 0-based indent level of the code currently
        """
        return len(self.indentRecord) - 1

    def startsBlock(self, command):
        return command.lower() in self._blockStarters

    def checkLine(self, line):
        """
        :param line: raw source code line to test
        :return: true if the indent level is valid, false otherwise
        """
        if(self._opensBlock):
            self._new_block = True
            self._opensBlock = False
        else:
            self._new_block = False

        for keyword in self._blockStarters:
            if line.index(keyword) != -1:
                self._opensBlock = True

        whitespace = getLeadingWhitespace(line)
        if whitespace != self.indentRecord[-1]:
            if self.isValidIndent(whitespace, self.indentRecord[-1]):
                self.indentRecord.append(whitespace)

        return whitespaceValid(line, whitespace, self.indentRecord[-1])


    def isValidIndent(self, indent, lastIndent):
        return indent.index(lastIndent) != 0 and self._new_block


def getLeadingWhitespace(line):
    length = len(line) - len(line.lstrip())
    return line[:length]


def whitespaceValid(line, indentation, startOfBlock):
    ws = getLeadingWhitespace(line)
    prev = indentation[-1]
    if startOfBlock:
        return len(prev) < len(ws) and prev == ws[:len(prev)]
    else:
        indentation = indentation[:]  # Don't want to modify the original
        while len(ws) < len(prev) and indentation:
            prev = indentation.pop()
        return prev == ws
