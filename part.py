# -*- coding: utf-8 -*-
import re
import copy
from dictionaries import *

bug = False

class Part(object):
    """
    Represents Part of a compound Word: Root, Prefix (Pref) or Suffix (Suff).
    """
    def __init__(self, string):
        """
        self.string: a string representing Part of a Word
        """
        self.string = string

class Pref(Part):
    """
    Represents a prefix, composed of one or more "simple" prefixes.
    Not necessarily the beginning of a word if the entire word is a compound word.
    """
    def __init__(self, each_pref):
        """
        each_pref: a list of strings that form a compound prefix, or a list with a single prefix string
        self.each_pref: see above
        self.length: number of "simple" prefixes in each_pref
        self.string: a concatenated string of the entire compound prefix
        """
        self.each_pref = each_pref
        self.length = self.create_length()
        self.string = self.create_string()

    def create_length(self):
        """
        Returns number of simple prefixes in each_pref.
        """
        try:
            return len(self.each_pref)
        except TypeError:
            return 0

    def create_string(self):
        """
        Concatenates each string in self.each_pref.
        Returns string representing entire compound prefix.
        """
        string = ''
        for frag in self.each_pref:
            string += frag
        return string

    def ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex):
        """
        Uses dictionary of prefix ipa translations to create ipa for each prefix in self.each_pref.
        Places stress before final separable prefix.
        Handles special cases: "hin", "her", "dar", "vor".
        Returns ipa for entire compound prefix
        """
        newipa = ''

        # if each_pref is empty, return empty string
        if self.length == 0:
            return newipa

        # iterate over each_pref
        for i in range(self.length):

            # add first prefix
            if i == 0:
                newipa += prefixes[self.each_pref[i]]

            # add the rest of the prefixes
            else:

                # remove stress from first prefix if it has one
                if newipa[0] == "ˈ":
                    newipa = newipa[1:]

                # check if previous pref was special case: 'hin', 'her', 'dar' or 'vor'

                # hin
                if self.each_pref[i-1] == 'hin':
                    temp = prefixes[self.each_pref[i]]
                    if temp[1] == "ʔ".decode('utf8'):
                        newipa = newipa[:-1] + "ˈn".decode('utf8') + temp[2:]
                    else:
                        newipa += temp

                # her
                elif (self.each_pref[i-1] == 'her'):
                    temp = prefixes[self.each_pref[i]]
                    if temp[1] == "ʔ".decode('utf8'):
                        newipa = newipa[:-4] + "ɛˈɾ".decode('utf8') + temp[2:]
                    else:
                        newipa += temp

                # dar vor
                elif (self.each_pref[i-1] in ['dar', 'vor']):
                    temp = prefixes[self.each_pref[i]]
                    if temp[1] == "ʔ".decode('utf8'):
                        newipa = newipa[:-1] + "ˈɾ".decode('utf8') + temp[2:]
                    else:
                        newipa += temp
                else:
                    newipa += prefixes[self.each_pref[i]]

        # change primary stress to secondary if wordindex != 0
        if (wordindex != 0) and (newipa[0] == "ˈ".decode('utf8')):
            newipa = "ˌ".decode('utf8') + newipa[1:]

        # show Part type if debugging is on
        if bug == True:
            return 'Pref: ' + newipa + ' '
        else:
            return newipa

class Suff(Part):
    """
    Represents a suffix, composed of one or more "simple" suffixes.
    Not necessarily the beginning of a word if the entire word is a compound word.
    """
    def __init__(self, each_suff):
        """
        each_suff: list containing all suffix strings that occur successively in a word.
        self.each_suff: see above.
        self.length: the number of strings in each_suff.
        self.string: string representing the entire compound Suff.
        """
        self.each_suff = each_suff
        self.length = self.create_length()
        self.string = self.create_string()

    def create_length(self):
        """
        Returns the number of simple suffixes in each_suff
        """
        try:
            return len(self.each_suff)
        except TypeError:
            return 0

    def create_string(self):
        """
        Concatenates each string in each_suff.
        Returns string containing entire compound suffix.
        """
        strin = ''
        for frag in self.each_suff:
            strin += frag
        return strin

    def ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex):
        """
        Uses dictionary of suffix ipa translations to create ipa for each suffix in self.each_suff.
        Returns ipa for entire compound suffix
        """
        newipa = ''
        if self.length == 0:
            return newipa

        # TODO suffixes that end in R

        # iterate over each suff in each_suff
        for i in range(self.length):

            # look up ipa in suffix dictionary
            try:
                newipa += suffixes[self.each_suff[i]]
            except KeyError:
                newipa += stressed_suffixes[self.each_suff[i]]

            # special case: "ig"
            if (self.each_suff[i] == 'ig'):

                # and its not end of element
                if (i < (self.length -1)):

                    # and next letter is a vowel
                    if (self.each_suff[i+1][0] in vowels):

                        # change ipa to g
                        newipa = newipa[:-1] + 'g'

                    # else if next syllable has ich sound
                    elif ("ich" in self.each_suff[i+1]):

                        # change ipa to 'k'
                        newipa = newipa[:-1] +'k'

        if bug == True:
            return 'Suff: ' + newipa + ' '
        else:
            return newipa

class Root(Part):
    """
    Represents Part of a Word that is not a prefix or suffix. Sometimes identical to entire Word.
    Needs to be broken down into still smaller Fragments (Frag).
    """
    def __init__(self, string):
        """
        self.string: a string representing a root of a word
        self.each_frag: a list of Frag objects
        self.length: number of Frags in root
        """
        self.string = string
        self.each_frag = self.create_each_frag()
        self.length = len(self.each_frag)

    def create_each_frag(self):
        """
        Breaks root up into Fragments (Frag): Consonant (Cons), Cluster (Clust), Vowel (Vow) or Diphthong (Diph)
        Returns each_frag, a list of Fragment objects.
        """
        # break root up and add fragments to each_frag
        each_frag = []

        # TODO double s case: need to handle here or at vowel rule

        # split string each time word switches between vowel and consonant
        each_string = re.split("([aeiouyäëïöü\']+)".decode('utf8'), self.string)
        for i in range(len(each_string)):

            # consonant strings will always be at even indexes
            if i % 2 == 0:

                # single cons = Cons
                if len(each_string[i]) == 1:
                    each_frag.append(Cons(each_string[i]))

                # multiple cons = Clust
                elif len(each_string[i]) > 1:
                    each_frag.append(Clust(each_string[i]))

            # vowel strings will always be at odd indexes
            else:

                # single vowel = Vow
                if (len(each_string[i]) == 1):
                    each_frag.append(Vow(each_string[i]))

                # multiple vowels m= Diph
                else:
                    each_frag.append(Diph(each_string[i]))

        return each_frag

    def get_each_frag(self):
        return copy.deepcopy(self.each_frag)

    def ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex):
        """
        Applies each fragment's ipa rule

        Passes in the following arguments when applying each Frag's ipa rule:

            //Information about Word and Parts//
            self.finalstress: boolean denoted whether or note the Word has a stressed suffix.
            ipa: list of ipa strings for the preceding Word Parts.
                (does not include ipa for previous Frags in Root)
            each_part: list of Part objects for entire Word.
            wordlength: number of Parts in each_part.
            wordindex: the Root's index in self.each_part.

            //Infortmation about Root and Frags//
            newipa: ipa string of Root so far.
            self.each_frag: list of Frags for entire Root.
            self.length: number of Frags in Root.
            i: index of Frag in self.each_frag.

        Returns ipa string for entire root.
        """
        newipa = ''

        # iterate of each frag in root
        for i in range(self.length):

            # apply frag's ipa_rule
            newipa += self.each_frag[i].ipa_rule(finalstress, ipa, each_part, wordlength, wordindex, newipa, self.each_frag, self.length, i)

        # return ipa for root
        return newipa


class Frag(object):
    """
    Represents a Fragment of a Root of a Word: Consonant (Cons), Cluster (Clust), Vowel (Vow) or Diphthong (Diph).
    """
    def __init__(self, string):
        """
        self.string: a string representing the Fragment
        """
        self.string = string

    def ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, alreadystress=False, nextletter=''):
        """
        Parent function for all Fragment ipa rules.

        Adds stress if beginning of word/element, and sets the following variables:
            self.newipa = ipa string with any inital stress markings
            self.prevfrag = Type of previous Frag in Root. Equals None if beginning of Root.
            self.nextfrag = Type of the next Frag in Root. Equals None if end of Root.
            self.nextpart = Type of the next Part in Word. Only set if Frag is end of Root.
            self.nextletter = Next letter in the Root and/or Word.
            self.endofel = Boolean specifying whether the Frag is the end of an element.

        If a Fragment calls another Fragment's ipa rule (ex: Cons rule used within Cluster rule),
            arguments alreadystress and nextletter can be passed in.

        Each Frag subclass calls this function before continuing to apply its individual ipa rules.
        """
        newipa = ''
        prevfrag = None
        nextfrag = None
        nextpart = None
        endofel = None

        # if Frag is beginning of Root and we haven't set stress yet
        if (alreadystress == False) and (rootindex == 0) and (not finalstress):

            # if Frag beginning of Word, give primary stress
            if (wordindex == 0):
                newipa += "ˈ".decode('utf8')

            # else not beginning of word
            else:

                # if Frag follows FIRST Prefix
                if (wordindex == 1) and (type(each_part[wordindex - 1]) == Pref):

                    # if Prefix has primary stress, give Frag secondary stress
                    if 'ˈ'.decode('utf8') in ipa[0]:

                        newipa += "ˌ".decode('utf8')

                    # or if Prefix is unaccented, give Frag primary stress
                    else:
                        newipa += "ˈ".decode('utf8')

                # if doesn't follow first prefix (or any prefix), give secondary stress
                else:
                    newipa += "ˌ".decode('utf8')

        # else if not beginning of root, set prevfrag
        elif (rootindex > 0):
            prevfrag = type(each_frag[rootindex -1])

        # if not end of root, look at next frag for its type and first letter, set end of element to False
        if (rootindex < (rootlength-1)):
            nextfrag = type(each_frag[rootindex + 1])
            if nextletter == '':
                nextletter = each_frag[rootindex+1].string[0]
            endofel = False

        # if it is the end of both root and word, end of element must be True

        elif (wordindex == (wordlength - 1)):
            endofel = True

        # end of root but not end of word, investigate further
        else:
            # look to next part for its type and first letter
            nextpart = type(each_part[wordindex+1])
            if nextletter == '':
                nextletter = each_part[wordindex+1].string[0]

            # if next part type is not suffix, Frag is end of element
            if (nextpart != Suff):
                endofel = True

            # else next part is suff, and first suff is a proper suffix, thus Frag is end of root
            else:
                endofel = False

        self.newipa = newipa
        self.prevfrag = prevfrag
        self.nextfrag = nextfrag
        self.nextpart = nextpart
        self.nextletter = nextletter
        self.endofel = endofel


class Cons(Frag):
    """
    Represents a Fragment which is a single consonant.
    """
    def __init__(self, string):
        """
        self.string: a string containing a single consonant.
        """
        Frag.__init__(self, string)

    def ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, alreadystress = False, nextletter=''):
        """
        Returns ipa for Cons, including any necessary stresses
        """
        # Use Frag parent ipa rule to set stress and get extra variables (newipa, prevfrag, nextfrag, nextpart, nexletter, endofel)
        Frag.ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, alreadystress, nextletter)

        # if next part is stressed suffix, add stress before the consonant
        if finalstress and (rootindex == (rootlength-1)) and (self.nextpart == Suff):
            self.newipa += "ˈ".decode('utf8')

        # if only one ipa possibility
        if self.string in 'fjklmnpwxzß'.decode('utf8'):
            self.newipa += normal_consonants[self.string]

        # if b, d, g, s (voiced/unvoiced)
        # TODO way to use these rules for some clust combos?
        # TODO bdgs might be followed by consonant -- need to add that stuff to rule
        # TODO Eleanor word exceptions
        elif self.string in 'bdgsv':

            if (self.endofel) or (self.nextletter in consonants):
                self.newipa += bdgs_uv[self.string]
            else:
                self.newipa += bdgs_v[self.string]

        # c
        elif self.string == 'c':
            if self.nextletter in 'aou':
                self.newipa += 'k'
            else:
                self.newipa += 'ts'

        # h
        elif self.string == 'h':
            if rootindex == 0:
                self.newipa += 'h'
            else:
                pass
        # t
        elif self.string == 't':

            # "ts" if precedes "io"
            if self.nextletter == "i":
                if (rootindex < (rootlength - 1)) and (each_frag[rootindex+1].string == 'io'):
                    self.newipa += "ts"
                elif (rootindex == (rootlength - 1)) and (each_part[wordindex+1].string.startswith("ion")):
                    self.newipa += "ts"

                # otherwise just "t"
                else:
                    self.newipa += "t"
            else:
                self.newipa += "t"
        # q
        elif self.string == 'q':
            if self.nextletter == 'u':
                self.newipa += 'kv'
            else:
                self.newipa += 'Q NO U?'

        # r
        # TODO 'er'
        # TODO vanish them if at end of short word
        elif self.string == 'r':
            self.newipa += "ɾ".decode('utf8')

        # some other consonant I forgot
        else:
            self.newipa += "CONSONANT UNACCOUNTED FOR"

        # return the ipa
        if bug == True:
            return "Cons: " + self.newipa + ' '
        else:
            return self.newipa

class Clust(Frag):
    """
    Represents Fragment which is string of consonants.
    """
    def __init__(self, string):
        """
        self.string:  string containing successive consonants.
        self.length: number of characters in self.string.
        """
        Frag.__init__(self, string)
        self.length = len(self.string)

    def ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, alreadystress = False, nextletter=''):
        """
        Returns the ipa for the Cluster, including any necessary stresses.
        """
        # Use Frag parent ipa rule to set stress and get extra variables (newipa, prevfrag, nextfrag, nextpart, nexletter, endofel)
        Frag.ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, alreadystress, nextletter)

        # if easy cluster
        if self.string in easy_clusters.keys():
            self.newipa += easy_clusters[self.string]

        # if can be treated as single consonant: "kk", "bb", "dt", "dd", "gg"
        elif self.string in ["kk", "bb", "dt", "dd", "gg"]:

            # use Cons ipa rule on second consonant in the string
            self.newipa += Cons(self.string[1]).ipa_rule(finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True)

        # short clusters that can go more than one way: "ch","sch", "sp", "st"

        # "ch"
        elif self.string == "ch":
            if (self.prevfrag == Vow):
                if (each_frag[rootindex - 1].string == 'a') or (each_frag[rootindex - 1].string == 'o') or (each_frag[rootindex - 1].string == 'u'):
                    self.newipa += "x"
                else:
                    self.newipa += "ç".decode('utf8')
            elif (self.prevfrag == Diph) and (each_frag[rootindex - 1].string == 'au'):
                self.newipa += "x"
            else:
                self.newipa += "ç".decode('utf8')

        #"chs"
        # TODO verbs and genitive endings where it is not "ks"!!
        elif self.string == "chs":
            self.newipa += "ks"

        # "sp"
        elif self.string == "sp":
            if rootindex == 0:
                self.newipa += "ʃp".decode('utf8')
            else:
                self.newipa += "sp"

        # "st"
        elif self.string == "st":
            if rootindex == 0:
                self.newipa += "ʃt".decode('utf8')
            else:
                self.newipa += "st"

        # "sch"
        # TODO check suffix "chen" -- might have some false positives
        elif self.string == "sch":
            self.newipa += "ʃ".decode('utf8')

        # else more complex, needs to be broken down more
        else:

            # look for common clust at beginning and end
            front = len(filter(self.string.startswith,all_clust+[''])[0])
            back = len(filter(self.string.endswith,all_clust+[''])[0])

            # if clust found at beginning
            if front > 0:

                # use clust ipa rule on front, set already stressed to True so we don't get a double stress
                self.newipa += Clust(self.string[:front]).ipa_rule(finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True)

                # if rest is just one cons, use cons ipa rule
                if ((self.length - front) == 1):
                    self.newipa += Cons(self.string[front:]).ipa_rule(finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True)

                # otherwise use clust ipa rule again
                else:
                    self.newipa += Clust(self.string[front:]).ipa_rule(finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True)

            # else if clust found at end
            elif back > 0:

                # if first part is just one cons, apply Cons ipa rule
                if ((self.length - front) == 1):
                    self.newipa += Cons(self.string[:-back]).ipa_rule(False, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True, self.string[1])
                    self.newipa += Clust(self.string[-back:]).ipa_rule(finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True)

                # otherwise use clust ipa rule
                else:
                    self.newipa += Clust(self.string[:-back]).ipa_rule(False, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True, self.string[-back])
                    self.newipa += Clust(self.string[-back:]).ipa_rule(finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True)

                    # else none found, use Cons rule on each consonant in clust

            # TODO what if we get something like Cons + Clust + Cons? Do these exist?

            # no clusters found, use Cons ipa rule on each Cons
            else:
                conscount = self.length
                for c in range(conscount-1):
                    self.newipa += Cons(self.string[c]).ipa_rule(False, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True, self.string[c+1])
                self.newipa += Cons(self.string[conscount-1]).ipa_rule(finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, True)

        if bug == True:
            return "Clust: " + self.newipa + ' '
        else:
            return self.newipa

class Vow(Frag):
    """
    Represents a Fragment which is a single vowel
    """
    def __init__(self, string):
        """
        self.string: a string containing the single vowel character.
        """
        Frag.__init__(self, string)

    def ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, alreadystress = False, nextletter=''):
        """
        Returns the ipa for the Vowel, including any necessary stresses and glottals.
        """
        # ignore apostrophes
        if self.string == "\'":
            return ''

        # Use Frag parent ipa rule to set stress and get extra variables (newipa, prevfrag, nextfrag, nextpart, nexletter, endofel)
        Frag.ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, alreadystress, nextletter)

        # if at beginning of root, add glottal
        if rootindex == 0:
            self.newipa += "ʔ".decode('utf8')

        # Vow precedes single Cons, ipa is closed vowel
        if self.nextfrag == Cons:
            self.newipa += closed_vowels[self.string]
            if (not finalstress) and ((rootindex == 0) or (rootindex == 1)):
                self.newipa += "ː".decode('utf8')

        # Vow precedes Clust
        elif self.nextfrag == Clust:

            # 'h' closes vowel
            if self.nextletter == 'h':
                self.newipa += closed_vowels[self.string]

            # double consonant opens vowel
            else:
                self.newipa += open_vowels[self.string]

        # Vow precedes Suff
        elif self.nextfrag == Suff:

            # "ie" ending
            if (self.nextletter == 'e') and (self.string == "i"):
                self.newipa += 'j'

            # weird case - "e" is only likely Vowel here, but that would have been considered a suff/ending in Word.create_each_part
            else:
                self.newipa += closed_vowels[self.string]

        # Vow is end of word or element - like above, only likely vowel is "e" but it would be a Suff rather than Vow
        # Can't find an example of word like this, so just arbitrarily choosing closed vowel
        else:
            self.newipa += closed_vowels[self.string]

        if bug == True:
            return "Vowel: " + self.newipa + ' '
        else:
            return self.newipa

class Diph(Frag):
    """
    Represents a Fragment which is a string of consonants.
    """
    def __init__(self, string):
        """
        self.string: a string containing successive vowels.
        self.length: number of characters in self.string.
        """
        Frag.__init__(self, string)
        self.length = len(self.string)

    def ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, alreadystress = False, nextletter=''):
        """
        Returns the ipa for the Diph, including any necessary stresses and glottals.
        """
        # Use Frag parent ipa rule to set stress and get extra variables (newipa, prevfrag, nextfrag, nextpart, nexletter, endofel)
        Frag.ipa_rule(self, finalstress, ipa, each_part, wordlength, wordindex, rootipa, each_frag, rootlength, rootindex, alreadystress, nextletter)

        # most Diphs have only one ipa possibility
        try:
            self.newipa += diphthongs[self.string]

        # except the weird ones
        except KeyError:

            # check for "tion"
            if self.string == "io":
                if (each_frag[rootindex-1].string[-1] == 't') and (self.nextletter == 'n'):
                    self.newipa += "ĭo".decode('utf8')
                else:
                    self.newipa = "WEIRD DIPH"
            else:
                self.newipa = "WEIRD DIPH"

        if bug == True:
            return "Diph: " + self.newipa + ' '
        else:
            return self.newipa
