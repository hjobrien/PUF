from writer import *

class JsonLine:
    def __init__(self):
        self.type = ""
        self.id = -69
        self.prev = -1
        self.parent = -420
        self.primary = "Primary Descriptor Not Set"
        self.secondary = "Secondary descriptor not set"
        self.tertiary = "Tertiary descriptor not set"
        self.line = "foo->bar()"

    def __str__(self):
        return '''
        {
        "type"  :   "%s",
        "id"    :   %i,
        "prev"  :   %i,
        "parent"    :   %i,
        "primary"   :   "%s",
        "secondary" :   "%s",
        "tertiary"  :   "%s"
        "line"      :   "%s"
        }
        ''' % (self.type, self.id, self.prev, self.parent, self.primary, self.secondary, self.tertiary, self.line)


def toJson(line):
    '''
    :param line: Line of code to convert to json object for visualization
    :return: an INCOMPLETE   JsonLine object without the prev, parent, or id filled in
    '''
    command = getCommand(line).lower()
    type, primary, secondary, tertiary = None, None, None, None
    if not command:
        return "{\"Type\": \"Error\"}"
    elif command == "go":
        type = "Movement"
        primary, secondary, tertiary = parseGo(line)
    elif command == "turn":
        type = "Movement"
        primary = "Turn"
        secondary, tertiary = parseTurn(line)
    elif command == "do":
        type = "Control"
        primary = "do loop"
        secondary, tertiary = None, None
    elif command == "while":
        type = "Control"
        primary = "While"
        secondary = parseWhile(line)
        tertiary = None
    elif command == "if":
        type = "Control"
        primary = "If statement"
        secondary = parseIf(line)
        tertiary = None
    elif command == "elif":
        type = "Control"
        primary = "Else If Statement"
        secondary = parseElseIf(line)
        tertiary = None
    elif command == "else":
        type = "Control"
        primary = "Else statement"
        secondary = None
        tertiary = None
    else:
        return "{\"Type\": \"Error\"}"
