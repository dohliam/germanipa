# -*- coding: utf-8 -*-

vowels = ('a', 'e', 'i', 'o', 'u', 'y', 'ä', 'ë', 'ï', 'ö', 'ü')
consonant = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 'ß']
consonants = [x.decode('utf8') for x in consonant]
exceptions = []
bdgs_uv = {"b": "p", "d": "t", "g": "k", "s": "s", "v": "f"}
bdgs_v = {"b": "b", "d": "d", "g": "g", "s": "z", "v": "v"}
al_clust = ["ch", "sp", "st", "sch", "zz", "tz", "pf", "ps", "ph", "th", "ck", "ß", "ng", "nk", "tsch", "ʧ", "kk", "bb", "dt", "dd", "gg", "bl", "br", "dr", "gl", "gr", "bn", "dl", "dn"]
all_clust = []
for s in al_clust:
    all_clust.append(s.decode('utf8'))
ipa_prefixes = {
    "ab" : "ˈʔap",
    "an" : "ˈʔan",
    "auf" : "ˈʔaof",
    "aus" : "ˈʔaos",
    "be" : "bə",     ###unaccented
    "da" : "da",
    "ein" : "ˈʔaen",
    "emp" : "ʔɛmp",   ###unaccented
    "ent" : "ʔɛnt",   ###unaccented
    "er" : "ʔɛːɐ",     ###unaccented
    "fern" : "ˈfɛɾn",
    "fort" : "ˈfɔɾt",
    "ge": "gə" ,     ###unaccented
    "her" : "ˈheːɐ̯",
    "hin" : "ˈhɪn",
    "miss" : "ˈmɪs",
    "mit" : "ˈmɪt",
    "nach" : "ˈnax",
    "um" : "ˈʔʊm",
    "un" : "ˈʔʊn",
    "vor" : "ˈfoːɐ̯",
    "vorbei" : "foːɐ̯ˈbae",
    "ver" :  "fɛːɐ̯",  ###unaccented
    "weg" : "ˈvɛk",
    "zer" : "tsɛːɐ̯", ###unaccented
    "zu" : "ˈtsuː"
}

ipa_insep_prefixes = {
    "be" : "bə",     ###unaccented
    "emp" : "ʔɛmp",   ###unaccented
    "ent" : "ʔɛnt",   ###unaccented
    "er" : "ʔɛːɐ",     ###unaccented
    "ge": "gə" ,     ###unaccented
    "ver" :  "fɛːɐ̯",  ###unaccented
    "zer" : "tsɛːɐ̯", ###unaccented
}

# Not added: "eich", "ich" "eig", "or", "us", "ma"

ipa_suffixes = {
    "bar" : "baːɐ̯",
    "chen" : "çɘn",
    "haft" : "haft",
    "heit" : "haet",
    "keit" : "kaet",
    "lein" : "laen",
    "lich" : "lɪç",
    "ling" : "lɪŋ",
    "los" : "loːs",
    "nis" : "nɪs",
    "sal" : "zaːl",
    "sam" : "zaːl",
    "schaft" : "ʃaft",
    "sis" : "zɪs",
    "tum" : "tuːm",
    "e" : "ə",
    "ei" : "ae",
    "er" : "ɐ̯",
    "en" : "ən",
    "em" : "əm",
    "es" : "əs",
    "et" : "ət",
    "ig" : "ɪç",
    "in" : "ɪn",
    #"um" : "ʊm",
    "ung" : "ʊŋ"
}

# TODO "ie" ending: difference between greek and latin words
ipa_stressed_suffixes = {
    "al" : "al",
    "an" : "an",
    "ar" : "aɽ",
    "ant" : "ɑnt",
    "anz" : "ants",
    "ast" : "ast",
    "ent" : "ɛnt",
    "enz" : "ents",
    "ett" : "kɛt",
    "ion" : "ĭoːn",
    "ie" : "iː/jə",
    "ien" : "iːən",
    "ieren" : "iːɾen",
    "iere" : "iːɾe",
    "ierst" : "iːɾst",
    "iert" : "iːɾt",
    "ier" : "iːɐ̯",
    "il" : "iːl",
    "ismus" : "ɪsmʊs",
    "ist" : "ɪst",
    "it" : "iːt",
    "iv" : "iːf",
    "on" : "oːn",
    "ur" : "uːɐ",
    "ment" : "mɛnt",
    "tät" : "ˈtɛːt",
    #"tion" : "tsĭoːn",
    #"sion" : "zĭoːn"
}

ipa_endings = {
    "e" : "ə",
    "er" : "ɐ̯",
    "en" : "ən",
    "em" : "əm",
    "es" : "əs",
    "et" : "ət"
}


ipa_closed_vowels = {
    "a" : "ɑ",
    "e" : "e",
    "i" : "i",
    "o" : "o",
    "u" : "u",
    "y" : "y",
    "ä" : "ɛ",
    "ë" : "e",
    "ï" : "i",
    "ö" : "ø",
    "ü" : "y"
}

ipa_open_vowels = {
    "a" : "a",
    "e" : "ɛ",
    "i" : "ɪ",
    "o" : "ɔ",
    "u" : "ʊ",
    "y" : "ʏ",
    "ä" : "ɛ",
    "ë" : "ɛ",
    "ï" : "ɪ",
    "ö" : "œ",
    "ü" : "ʏ"
}

ipa_consonants = {
    'b',
    'c',
    'd',
    'f',
    'g',
    'h',
    'j',
    'k',
    'l',
    'm',
    'n',
    'p',
    'q',
    'r',
    's',
    't',
    'v',
    'w',
    'x',
    'z',
    'ß'
}

ipa_normal_consonants = {
    "f" : "f",
    "j" : "j",
    "k" : "k",
    "l" : "l",
    "m" : "m",
    "n" : "n",
    "p" : "p",
    "t" : "t",
    "v" : "f",
    "w" : "v",
    "x" : "ks",
    "z" : "ts",
    "ß" : "s"
}

ipa_diphthongs = {
    "ie" : "iː",
    "au" : "ao",
    "ei" : "ae",
    "ey" : "ae",
    "ay" : "ae",
    "eu" : "ɔø",
    "äu" : "ɔø",
    "aa" : "aː"
}

ipa_easy_clusters = {
    "tt" : "t",
    "zz" : "ts",
    "tz" : "ts",
    "pf" : "pf",
    "ps" : "ps",
    "ph" : "f",
    "th" : "t",
    "ck" : "k",
    "ß" : "s",
    "gn" : "gn",
    "ng" : "ŋ",
    "nk" : "ŋk",
    "tsch" : "ʧ",
    #blends
    "bl" : "bl",
    "br" : "br",
    "dr" : "dɾ",
    "gl" : "gl",
    "gr" : "gɾ",
    # eleanor extras
    "bn" : "bn",
    "dl" : "dl",
    "dn" : "dn"
}

prefixes = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_prefixes.items()}
insep_prefixes = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_insep_prefixes.items()}
suffixes = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_suffixes.items()}
stressed_suffixes = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_stressed_suffixes.items()}
endings = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_endings.items()}
closed_vowels = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_closed_vowels.items()}
open_vowels = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_open_vowels.items()}
normal_consonants = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_normal_consonants.items()}
diphthongs = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_diphthongs.items()}
easy_clusters = {k.decode('utf8'): v.decode('utf8') for k, v in ipa_easy_clusters.items()}
