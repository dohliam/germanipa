import sys
from text import Text

if __name__ == "__main__":
    a = sys.argv[1]
    b = Text(a.decode('utf8'))
    b.print_dict_ipa()
