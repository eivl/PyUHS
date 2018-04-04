"""
Psudocode for UHS88a

if i<32
  return i
endif
if i<80
  return 2*i-32
else
  return 2*i-127
endif

File composition

Line  Content
1    "UHS", a magic marker indicating a UHS file.
2    "Borrowed Time", the main title
3    "73" the line number of the first hint (meaning line 77)
4    "143" the line number of the last hint (meaning line 147)
[end of header]



[directory tree]
5    "gHrGtGs iqrGr"="Opening Scene"
6    "23" the line number jumped to when selecting this link (meaning line 27)
[...]
25   "kIpHHtGs jH JDr apyr"="Wrapping Up the Case"
26   "69" -- this is the last entry of the main directory, since a link above linked to line 27.
27   "kDpJ Bw d Bw tG JDr wCCtqr"="What do I do in the office" (note: no question mark)
28   "73" link destination line no (meaning line 77)
29   "4w{ Bw d ryqpHr CIwv JDr JDzsy"="How do I escape from the thugs" (note: no question mark)
30   "76" link destination line no (meaning line 80)
[...]
75   "4w{ Bw d pIIryJ 3pIGDpv"="How do I arrest Farnham" (note: no question mark)
76   "141" link destination line no (meaning line 145)
[end of directory tree]



[hints]
77   This is the first hint line, as indicated in the header.
[...]
147  This is the last hint line, as indicated in the header.
"""
test_string = "|wz pIr zytGs Bwry GwJ yzHHwIJ'  ;tytJ JDr j4i {rA ytJr pJ"


class UhsError(LookupError):
    """raise this if there is a lookup error somewhere"""


class UHS:
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        self.lines = self.read_file()

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
        if self.lines[0] != 'UHS':
            raise UhsError('The file you read is not valid')
        pass
