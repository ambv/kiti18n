# -*- coding: utf-8 -*-
# pl.wikisource.org/wiki/Unicode/Cyrylica

l2c = {
    u'a': u'\u0430',
    u'\u0E04': u'\u044D', # a umlaut -> 3
    u'\u0105': u'\u043E'+u'\u043D', #oh
    u'b': u'\u0431',
    u'c': u'\u0446',
    u'\u0107': u'\u0447', # ć
    u'd': u'\u0434',
    u'e': u'\u0435',         #u'\u044D',
    u'\u0119': u'\u0435'+ u'\u043D', #eh
    u'\u0F06': u'\u0451', #german o umlaut na cyrylica e
    u'f': u'\u0444',
    u'g': u'\u0433',
    u'h': u'\u0445',
    u'x': u'\u0445',
    u'i': u'\u0438',
    u'j': u'\u0439',
    u'k': u'\u043A',
    u'l': u'\u043B',#+ u'\u044C',
    u'\u0142': u'\u043B',
    u'm': u'\u043C',
    u'n': u'\u043D',
    u'\u0144': u'\u043D'+u'\u044C', # hb
    u'o': u'\u043E',
    u'\u00F6': u'\u044E',
    u'\u00F3': u'\u043E',
    u'p': u'\u043F',
    #u'q': u'\u044F',
    u'q': u'\u043A',
    u'r': u'\u0440',
    u's': u'\u0441',
    u'\u015b': u'\u0441',
    u't': u'\u0442',
    u'u': u'\u0443', #u na y
    u'\u0F0C': u'\u044E', # u niemieckie na ju russian
    u'v': u'\u0432',
    u'w': u'\u0432', # 432
    u'y': u'\u044B',
    u'z': u'\u0437',
    u'\u017A': u'\u0437',
    u'\u017C': u'\u0436',
    u'#': u'\u044A',
    u'A': u'\u0410',
    u'\u0C04': u'\u042D', # a umlaut -> 3
    u'\u0104': u'\u041E'+u'\u041D', # OH
    u'B': u'\u0411',
    u'C': u'\u0426',
    u'\u0106': u'\u0427',
    u'D': u'\u0414',
    u'E': u'\u042D',
    u'\u0118': u'\u0415' + u'\u041D', # EH
    u'\u0D06': u'\u0401', #german o umlaut na cyrylica e
    u'F': u'\u0424',
    u'G': u'\u0413',
    u'H': u'\u0425',
    u'X': u'\u0425',
    u'I': u'\u0418',
    u'J': u'\u0419',
    u'K': u'\u041A',
    u'L': u'\u041B', # + u'\u042C', bez miekkiego
    u'\u0141': u'\u041B',
    u'M': u'\u041C',
    u'N': u'\u041D',
    u'O': u'\u041E',
    u'\u00D6': u'\u042E',
    u'\u00D3': u'\u041E',
    u'P': u'\u041F',
    #u'Q': u'\u042F',
    u'Q': u'\u041A',
    u'R': u'\u0420',
    u'S': u'\u0421',
    u'\u015A': u'\u0421',
    u'T': u'\u0422',
    u'U': u'\u0423',
    u'\u0D0C': u'\u042E', # U niemieckie na ju russian
    u'V': u'\u0412',       # new u'V' mapping
    u'W': u'\u0412',
    u'Y': u'\u042B',
    u'Z': u'\u0417',
    u'\u0179': u'\u0417', 	#Ź
    u'\u017B': u'\u0416', 	#Ż
    u'\u0027': u'\u044C', 	#Ż
    u"`": u'\u044C',    # u'mjadkij' instead of .that //what3v3r - until we'l translate /ru to /ru ;)
    u"u'": '\u044Cu',    # 'mjadkiju' instead of .that //what3v3r - until we'l translate /ru to /ru ;)
    #u'"': u'\u042C',    # u'mjadkij' instead of .that //what3v3r - until we'l translate /ru to /ru ;)
}

l2c.update({
    u'CH': l2c[u'H'],
    u'Ch': l2c[u'H'],
    u'CZ': u'\u0427',
    u'Cz': u'\u0427',
    u'IA': u'\u042F',
    u'Ia': u'\u042F',
    u'IE': u'\u0415',
    u'Ie': u'\u0415',
    u'IO': u'\u0451',
    u'Io': u'\u0451',
    u'JA': u'\u042F',
    u'Ja': u'\u042F',
    u'JE': u'\u042D', #415? 
    u'Je': u'\u042D', #415? 
    u'JO': u'\u0401', # XXX: sure?
    u'Jo': u'\u0401', # XXX: sure?
    u'JU': u'\u042E',
    u'Ju': u'\u042E',
    u'KH': l2c[u'H'],
    u'Kh': l2c[u'H'],
    u'L`a': l2c[u'L'] + l2c[u'a'],  
    u'L`e': l2c[u'L'] + l2c[u'e'],  
    u'L`i': l2c[u'L'] + l2c[u'i'],  
    u'L`o': l2c[u'L'] + l2c[u'o'],  
    u'L`u': l2c[u'L'] + l2c[u'u'],  
    u'L`y': l2c[u'L'] + l2c[u'y'],  
    u'L\'a': l2c[u'L'] + l2c[u'a'],  
    u'L\'e': l2c[u'L'] + l2c[u'e'],  
    u'L\'i': l2c[u'L'] + l2c[u'i'],  
    u'L\'o': l2c[u'L'] + l2c[u'o'],  
    u'L\'u': l2c[u'L'] + l2c[u'u'],  
    u'L\'y': l2c[u'L'] + l2c[u'y'],  
    u'La': l2c[u'L'] + l2c[u'a'],
    u'Le': l2c[u'L'] + l2c[u'e'],
    u'Li': l2c[u'L'] + l2c[u'i'],
    u'Lo': l2c[u'L'] + l2c[u'o'],
    u'LE': l2c[u'L'] + l2c[u'e'],
    u'Le': l2c[u'L'] + l2c[u'e'],
    u'LU': l2c[u'L'] + u'\u044E',
    u'Lu': l2c[u'L'] + u'\u044E',
    u'RZ': u'\u0416',
    u'Rz': u'\u0416',
    u'SH': u'\u0428',
    u'Sh': u'\u0428',
    u'SHH': u'\u0429',
    u'Shh': u'\u0429',
    u'SZ': u'\u0428',
    u'Sz': u'\u0428',
    u'TS': l2c[u'C'],
    u'Ts': l2c[u'C'],
    u'YA': u'\u042F',
    u'Ya': u'\u042F',
    u'YE': u'\u0415',
    u'Ye': u'\u0415',
    u'YU': u'\u042E',
    u'Yu': u'\u042E',
    u'ZH': u'\u0416',
    u'Zh': u'\u0416',
    u'ch': l2c[u'h'],
    u'cz': u'\u0447',
    u'ey': l2c[u'e'] + l2c[u'j'], # only at the end
    u'ia': u'\u044F',
    u'ie': l2c[u'e'],
    u'io': u'\u0451',
    u'iy': l2c[u'i'] + l2c[u'j'],
    u'i\u00F3': u'\u0451',
    u'i\u0119': l2c[u'e'] + l2c[u'n'],
    u'ja': u'\u044F',
    u'je': u'\u044D', #435?
    u'jo': u'\u0451',
    u'ju': u'\u044E',
    u'kh': l2c[u'h'],
    u'l`a': l2c[u'l'] + l2c[u'a'], 
    u'l`e': l2c[u'l'] + l2c[u'e'], 
    u'l`i': l2c[u'l'] + l2c[u'i'], 
    u'l`o': l2c[u'l'] + l2c[u'o'], 
    u'l`u': l2c[u'l'] + l2c[u'u'], 
    u'l`y': l2c[u'l'] + l2c[u'y'], 
    u'l\'a': l2c[u'l'] + l2c[u'a'], 
    u'l\'e': l2c[u'l'] + l2c[u'e'], 
    u'l\'i': l2c[u'l'] + l2c[u'i'], 
    u'l\'o': l2c[u'l'] + l2c[u'o'], 
    u'l\'u': l2c[u'l'] + l2c[u'u'], 
    u'l\'y': l2c[u'l'] + l2c[u'y'], 
    u'la': l2c[u'l'] + l2c[u'a'], 
    u'le': l2c[u'l'] + l2c[u'e'],
    u'lo': l2c[u'l'] + l2c[u'o'], 
    u'li': l2c[u'l'] + l2c[u'i'], 
    u'lu': l2c[u'l'] + u'\u044E',
    u'ly': l2c[u'l'] + l2c[u'y'], 
    u'rz': u'\u0436',
    u'sh': u'\u0448',
    u'shh': u'\u0449',
    u'shch': u'\u0449',
    u'sz': u'\u0448',
    u'ts': l2c[u'c'],
    u'ya': u'\u044F',
    u'ye': l2c[u'e'],
    u'yo': u'\u0451',
    u'yu': u'\u044E',
    u'yy': l2c[u'y'] + l2c[u'j'],
    u'zh': u'\u0436', 
    u'##': u'\u042A',
})

cyrillic_countries = set(['ba', 'bg', 'by', 'mk', 'rs', 'ru', 'ua'])
c_convert_countries = set(['au', 'ca', 'en', 'gb', 'us', 'uk'])

cyrillic_updates = {
    u'CH': u'\u0427', 
    u'Ch': u'\u0427', 
    u'ch': u'\u0447', 
    u'aya': l2c[u'a'] + u'\u0447',
    u'ay': l2c[u'a'] + l2c[u'j'], #at the end 
    u'ia': l2c[u'i'] + u'\u044F',
    u'lu': l2c[u'l'] + l2c[u'u'],
}

def any(lang, input, force=False, input_lang=''):
    if not (force or lang in cyrillic_countries):
        return input

    trans_dict = dict(l2c)

    if input_lang in cyrillic_countries:
        trans_dict.update(cyrillic_updates)
    
    if input_lang in c_convert_countries:
        trans_dict.update({u'c': l2c[u'k'], u'C': l2c[u'K']})
    
    transformations = list(l2c.keys())
    transformations.sort(lambda x, y: len(y) - len(x) or cmp(x, y))

    result = input

    for t in transformations:
        result = result.replace(t, trans_dict[t])

    return result

if __name__ == '__main__':
    import sys
    print any(sys.argv[2], sys.argv[1].decode('utf-8'))
