class EnvParse:
    def __init__(self, source):
        self.data = {}

        with open(source) as file_:
            for line in file_:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip()
                if v.startswith('"') or v.endswith('"'):
                    v = v.strip('"')
                else:
                    v = v.strip("'")
                self.data[k] = v

config = EnvParse()


def json_parser(value):
    if value.startswith("'") and value.endswith("'"):
        value = value.strip("'")
    return json.loads(value)
