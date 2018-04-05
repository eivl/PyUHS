import json


class UhsError(LookupError):
    """raise this if there is a lookup error somewhere"""


class UHS:
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        self.lines = self.read_file()
        self.offset = 2
        self.structure = {}
        self.hints = self.generate_UHS88a_structure()

    def check_UHS88a_line(self, line: str):
        try:
            int(line)
            return int(line) + self.offset
        except ValueError:
            return self.decode_UHS88a(line)

    def read_file(self) -> list:
        with open(self.filename) as f:
            return [line.rstrip('\n') for line in f]

    def decode_UHS88a(self, mystr: str) -> str:
        result = []
        for i in mystr:
            code = ord(i)
            if code < 32:
                result.append(chr(code))
            elif code < 80:
                result.append(chr(2*code-32))
            else:
                result.append(chr(2*code-127))
        return ''.join(result)

    def generate_UHS88a_structure(self) -> dict:
        hint_file = {}
        main = {}
        body = {}
        main_generating = True
        body_generating = False
        stopsign = False
        body_lines = []
        tmp = []
        hints = {}
        hint_dir = {}
        if self.lines[0] != 'UHS':
            raise UhsError('The file you read is not valid')
        else:
            self.lines.pop(0)
        hint_file["Title"] = self.lines.pop(0)
        for i, l in enumerate(self.lines, start=1):
            self.structure[i] = self.check_UHS88a_line(l)
        for k, v in self.structure.items():
            if k is 1:
                hint_file["First Hint Line"] = v
                continue
            elif k is 2:
                hint_file["Last Hint Line"] = v
                continue
            if main_generating:
                if k < hint_file["First Hint Line"] and k % 2 == 1:
                    main[v] = self.structure[k+1]

                elif len(main) is 1:
                    stopsign = next(iter(main.values())) - 1
                elif k == stopsign:
                    main_generating = False
                    body_generating = True
                else:
                    continue
            elif body_generating:
                if not body_lines:
                    body_lines = list(main.values())
                    body_lines_iterator = iter(main.values())
                    body_keys = list(main.keys())
                    next(body_lines_iterator)
                    next_body_line = next(body_lines_iterator)
                if k < hint_file["First Hint Line"] and k % 2 == 1:
                    if next_body_line == k:
                        body.update({body_keys[0]: tmp[:]})
                        tmp.clear()
                        body_lines.pop(0)
                        body_keys.pop(0)
                        try:
                            next_body_line = next(body_lines_iterator)
                        except StopIteration:
                            pass
                    elif len(body_keys) is 1:
                        tmp.append((v, self.structure[k+1]))
                        body.update({body_keys[0]: tmp[:]})
                    tmp.append((v, self.structure[k+1]))
                    if self.structure[k+1] + self.offset < hint_file["Last Hint Line"]:
                        hint_dir.update({v: (self.structure[k+1],
                                             self.structure[k+3])})
                    else:
                        hint_dir.update({v: (self.structure[k+1],
                                             hint_file["Last Hint Line"])})
                elif k >= hint_file["First Hint Line"] and k <= hint_file["Last Hint Line"]:
                    hints.update({k: v})
        hint_file["Main"] = body
        hint_file["Hints"] = hints
        hint_file["Directory"] = hint_dir
        return hint_file

f = UHS('BORWDT.UHS')
print(json.dumps(f.hints, indent=4))
