import re


class IndentManager:

    def __init__(self, use_tabs=False):
        self.__use_tabs = use_tabs
        self.__curr_indent = 0
        # keeps a record of the indent level for each level, so if one level can't be both 2 and 4 spaces
        self.indent_record = []

    def get_indent_level(self):
        """
        :return: a 0-based indent level of the code currently
        """
        return len(self.indent_record) - 1

    def check_line(self, line):
        """
        :param line: raw source code line to test
        :return: true if the indent level is valid, false otherwise
        """
        line = line.replace('\t', '  ')
        tokens = re.compile('[^\s]+').split(line)
        indent = len(tokens[0])

        if indent > self.indent_record[-1]:
            self.indent_record.append(indent)
        else:
            for i in range(len(self.indent_record), 0, -1):
                indent_level = self.indent_record[i]
                if indent_level == indent:
                    self.__curr_indent = indent_level
                    return True
                else:
                    self.indent_record.pop()
            # no previous indent level found, invalid indent
            return False
