import json


class VersionsJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(VersionsJSONEncoder, self).__init__(*args, **kwargs)
        self.indent = 0

    def encode(self, o):
        # Special Processing for lists
        if isinstance(o, dict):
            maxKeySize = max([len(k) for k in o.keys()])
            lines = [self.indent*' ' + f'  "{key}"' + (
                (maxKeySize - len(key))*' ') + ": " + json.dumps(o[key]) + "," for key in o]
            if len(lines) > 0:
                lines[-1] = lines[-1][:-1]
            lines.insert(0, self.indent*' ' + "{")
            lines.append(self.indent*' ' + "}\n")
            return "\n".join(lines)

        return json.dumps(o)
