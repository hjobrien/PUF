class Parser:

    EXTENSION = ".prgm"
    INDENT = "    "

    __indent_level = 0

    def __init__(self):
        i = 0

    """function reads in a user-written file and writes the parsed, python only version to a
        different .py file. This IO will likeley only be done when the run button is pressed"""
    def parse(self, fileName):
        pyFileName = fileName + ".py"
        fileName += self.EXTENSION
        userfile = open(fileName, 'r') # should only read their file
        pyFile = open(pyFileName, 'w')
        lines = userfile.readlines()
        for line in lines:
            pyFile.write(lineConverter(line))

    def lineConverter(self, line):
        pyLine = line
        pyLine = self.INDENT * self.__indent_level + pyLine
        if("while " in line and " do " in line):
            pyLine = pyLine.replace(" do ", ":\n")
            self.__indent_level += 1
        elif():
        else:

        #pads the string to reflect the current indent level
