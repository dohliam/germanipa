from text import Text

if __name__ == "__main__":
    while True:
        sentinel = '/' # ends when this string is seen
        print 'Enter a German text below.\nThen type "/" and hit enter.\n'
        a = '\n'.join(iter(raw_input, sentinel))
        if a == "":
            break
        print a
        b = Text(a.decode('utf8'))
        b.print_ipa()