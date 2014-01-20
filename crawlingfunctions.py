from urllib import urlopen

def finduniquepages(listofpages):
    uniquepages = []
    for p in listofpages:
        if not p in uniquepages:
            uniquepages = uniquepages + [p]

    return uniquepages

def findlinksonpage(pagename):
    html = urlopen("http://en.wikipedia.org/wiki/"+pagename).read()

    split1 = html.split("\"")

    pages = []

    for chunk in split1:
        if chunk.startswith("/wiki/") and (not ":" in chunk and not "#" in chunk and not "%" in chunk):
            pages = pages + [chunk[6:]]

    uniquepages = finduniquepages(pages)

    return uniquepages
