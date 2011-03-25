# based on http://stackoverflow.com/questions/804336/

import urlparse, urllib

def uni2ascii(url):
    if not isinstance(url, unicode):
        # turn string into unicode
        url = url.decode('utf8')

    # parse it
    parsed = urlparse.urlsplit(url)

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    netloc = parsed.netloc.encode('idna')
    path = '/'.join(  # could be encoded slashes!
        urllib.quote(urllib.unquote(pce).encode('utf8'),'')
        for pce in parsed.path.split('/')
    )
    query = urllib.quote(urllib.unquote(parsed.query).encode('utf8'),'=&?/')
    fragment = urllib.quote(urllib.unquote(parsed.query).encode('utf8'))

    # put it back together
    return urlparse.urlunsplit((scheme,netloc,path,query,fragment))
