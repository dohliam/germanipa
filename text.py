# -*- coding: utf-8 -*-
from part import *
from split import split_word
import re
import string

import json

with open('wiktionary.json') as f:
    wiktionary = json.load(f)

class Text(object):
    """
    Represents an entire German text.
    """
    def __init__(self, user_input):
        """
        self.fulltext: a string representing the entire german text
        self.each_line: a list containing each Line object of text
        """
        self.fulltext = user_input
        self.each_line = self.create_each_line(self.fulltext)

    def create_each_line(self, fulltext):
        """
        fulltext: a string containing multiple lines of text
        Returns each_line, a list containing multiple Line objects
        """
        each_string = fulltext.splitlines()
        each_line = []
        for line in each_string:
            each_line.append(Line(line))
        return each_line

    def print_ipa(self):
        """
        Prints each Line of text with ipa underneath.
        """
        for line in self.each_line:
            if not (line.adjustedline.isspace() or (line.adjustedline == '')):
                print (line.adjustedline)
                print (line.ipa)
                print (' ')
            else:
                print (line.adjustedline)


class Line(object):
    """
    Represents one line of a German text.
    """
    def __init__(self, line):
        """
        self.full_line: a string of german text
        self.each_word: a list containing Word objects and strings of punctuation/whitespace
        self.ipa: a string of ipa for the entire line
        """
        self.full_line = line
        self.adjustedline = ''
        self.each_word = self.create_each_word(self.full_line)
        self.ipa = self.create_ipa(self.each_word)


    def create_each_word(self, full_line):
        """
        Splits a line at each occurrence of punctuation or whitespace
        Returns a list of Word objects alternating with strings of punctuation/whitespace
        """
        if full_line.isspace():
            return None

        each_word = []

        punc = string.punctuation.replace("\'", "")
        punc += '1234567890'
        wordlist = re.split("([" + punc + "|\s]+)", full_line)

        for i in range(len(wordlist)):
            if i % 2 == 0:  # even numbered index is Word or empty string
                if wordlist[i] != '':
                    each_word.append(Word(wordlist[i]))
                else:
                    each_word.append(wordlist[i])
            else:
                each_word.append(wordlist[i])

        return each_word

    def create_ipa(self, each_word):
        """
        Concatenates each Word's ipa into one string
        Sets Line.adjustedline to be a string whose words line up properly with Line.ipa
        Returns a string of ipa for the entire Line
        """
        # check if line is blank
        if each_word is None:
            return ''

        # declare ipa and adjustedline
        ipa = ''
        adjustedline = ''

        # combine words and punctuation and figure out length
        for w in range(len(each_word)):
            if isinstance(each_word[w], Word):
                try:
                    combo = each_word[w].fullword + each_word[w+1]
                except IndexError:
                    combo = each_word[w].fullword

                textlen = len(combo)  # length of word + punctuation/whitespace
                ipalen = len(each_word[w].ipa) + 1  # length of ipa + one space

                # does ipa have leading accents or glottals?
                accents = ["ˈʔ".decode('utf8'), "ˈ".decode('utf8')]
                frontlen = len(filter(each_word[w].ipa.startswith,accents+[''])[0])
                adjustedline += ' ' * frontlen

                # calculate difference in length
                diff = ipalen - (textlen + frontlen)

                if diff == 0:  # same length
                    ipa += each_word[w].ipa + ' '
                    adjustedline += combo

                elif diff > 0:  # ipa is longer
                    ipa += each_word[w].ipa + ' '
                    adjustedline += combo
                    adjustedline += ' ' * diff

                else:  # line is longer
                    ipa += each_word[w].ipa + ' '
                    adjustedline += combo
                    ipa += ' ' * -diff
        self.adjustedline = adjustedline
        return ipa

class Word(object):
    """
    Represents one german word.
    """
    def __init__(self, string):
        '''
        self.finalstress: boolean intially set to False. If a stressed suffix is found, it is changed to True.
        self.fullword: string that is a single German word.
        self.each_simple: list of "simple" word strings that combine to form "compound" word self.fullword.
            GermanWordSplitter module splits self.fullword and returns list (can be one element).
        self.each_part: list of each Part that makes up the self.fullword (can be list of one element).
        self.length: number of Parts in each_part.
        self.ipa: string that is the IPA pronunciation of self.fullword
        '''
        self.finalstress = False
        self.fullword = string
        self.each_simple = split_word(self.fullword)
        self.each_part = self.create_each_part()
        self.length = len(self.each_part)
        self.ipa = self.create_ipa()

    def create_each_part(self):
        '''
        Searches each "simple" word for prefixes and suffixes.
        Returns a list each_part of Parts (Prefix, Suffix or Root) comprising the entire compound word.
        '''
        # initialize lists
        each_part = []
        prefix_buff = []

        # iterate over each part of word
        for part in self.each_simple:

            # TODO some rules might need to check capitalization - diminutive endings
            part = part.lower()

            # if part is less than 5 letters, no need to look for prefs and suffs
            if len(part) < 5:
                if part in prefixes.keys():  # simple word could be a separable prefix
                    each_part.append(Pref([part]))
                else:
                    each_part.append(Root(part))

            # else if part is 5 or more letters
            else:
                # check if separable prefix
                if part in prefixes.keys():

                    # hold onto prefix until we know if next part is prefix or starts with insep. prefix
                    prefix_buff.append(part)

                # if not prefix, break part into fragments
                else:
                    root = part
                    suff_buff = []

                    # TODO check for issues : herz?
                    # check for prefixes
                    while True:
                        pref = root[:len(filter(root.startswith,prefixes.keys()+[''])[0])]
                        if pref == '':
                            break
                        prefix_buff.append(pref)
                        root = root[len(filter(root.startswith,prefixes.keys()+[''])[0]):]

                    # add any buffered prefixes to each_frag and empty buffer
                    if prefix_buff != []:
                        each_part.append(Pref(prefix_buff))
                        prefix_buff = []

                    # check for suffixes
                    while True:

                        # look for stressed suffs
                        breakpoint = len(filter(root.endswith,stressed_suffixes.keys()+[''])[0])

                        # if not stressed
                        if (breakpoint == 0):

                            # look for unstressed stuffs
                            breakpoint = len(filter(root.endswith,suffixes.keys()+[''])[0])

                            # no suffs found, stop looking
                            if (breakpoint == 0):
                                break

                            # update with unstressed suff
                            else:
                                suff = root[-breakpoint:]
                                root = root[:-breakpoint]


                        # update with stressed suff
                        else:
                            suff = root[-breakpoint:]
                            root = root[:-breakpoint]
                            self.finalstress = True

                        # add suffs to buffer
                        suff_buff.insert(0, suff)

                    # add root to each_part
                    each_part.append(Root(root))

                    # add suffs to each_part
                    if suff_buff != []:
                        each_part.append(Suff(suff_buff))
        return each_part

    def create_ipa(self):
        '''
        Applies each part's ipa rule to create ipa for entire Word.
        Passes in the following arguments when applying each Part's ipa rule:
            self.finalstress: boolean denoted whether or note the Word has a stressed suffix.
            ipa: list of ipa strings for the preceding Word Parts.
            self.each_part: list of Part objects for entire Word.
            self.length: number of Parts in each_part.
            i: the specific Part's index in self.each_part.
        Returns ipa string for entire Word.
        '''
        try:
            a = wiktionary[self.fullword][0]
            b = a.split("/")
            return b[1]
        except:
            ipa = []
            for i in range(self.length):
                ipa.append(self.each_part[i].ipa_rule(self.finalstress, ipa, self.each_part, self.length, i))
            ipa_string = ''
            for partipa in ipa:
                ipa_string += partipa
            return ipa_string