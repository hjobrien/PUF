import re


class IndentManager:

    def __init__(self, use_tabs=False):
        self.__use_tabs = use_tabs
        self.__curr_indent = 0
        # keeps a record of the indent level for each level, so if one level can't be both 2 and 4 spaces
        self.indent_record = [0]
        self.opens_block = False
        self.new_block = False
        self._blockStarters = ["create", "python:", "do", "if", "else", "else if"]

    def get_indent_level(self):
        """
        :return: a 0-based indent level of the code currently
        """
        return len(self.indent_record) - 1

    def startsBlock(self, command):
        return command.lower() in self._blockStarters

    def check_line(self, line):
        """
        :param line: raw source code line to test
        :return: true if the indent level is valid, false otherwise
        """
        self.new_block = self.opens_block

        if self.startsBlock(line):
            self.opens_block = True

        line = line.replace('\t', '  ')
        tokens = re.compile('[^\s]+').split(line)
        indent = len(tokens[0])

        if indent > self.indent_record[-1] and self.new_block:
            self.indent_record.append(indent)
            return True
        else:
            temp_record = self.indent_record[:]
            for i in range(len(self.indent_record)-1, -1, -1):
                print(self.indent_record)
                indent_level = self.indent_record[i]
                if indent_level == indent:
                    self.__curr_indent = indent_level
                    self.indent_record = temp_record
                    return True
                else:
                    temp_record.pop()
            # no previous indent level found, invalid indent
            return False
