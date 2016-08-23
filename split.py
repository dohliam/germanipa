with open("wordlist.txt") as f:
    language = [line.rstrip().decode('utf8') for line in f]


def split_word(word):
    for i in range(len(word)):
        if word[:i] in language:
            if word[i:] in language:
                return [word[:i], word[i:]]
            else:
                split = split_word(word[i:])
                if len(split) > 1:
                    return [word[:i]] + split
    return [word]

