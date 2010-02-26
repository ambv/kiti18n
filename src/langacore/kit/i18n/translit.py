import subprocess


def any(lang, input, force=False):
    langList = set(["el", "ru", "ja", "hi", "fa", "uk", "th", "sr", "ps",
                "mk", "ko", "he", "bg", "hy", "ar"])

    if type(input) == unicode:
        input = input.encode("utf-8")

    result = input

    if force or lang.lower() in langList:
        try:
            uconv = subprocess.Popen("uconv -x Latin-%s" % lang, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            uconv.stdin.write(input)
            result = uconv.communicate()
            result = result[0]
        except:
            pass

    return result
