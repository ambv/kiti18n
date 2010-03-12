from uconv import any as uconv
from custom import any as custom
from custom import cyrillic_countries 

def any(lang, input, force=False, input_lang=''):
    if force or lang in cyrillic_countries:
        return custom(lang, input, force, input_lang)
    else:
        return uconv(lang, input, force, input_lang)
