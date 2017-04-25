from writer import *

def toJson(line, prevRelLine):
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
    else:
        return "Failed to parse: %s" % line

