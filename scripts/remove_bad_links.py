from mekoros.model import *

links = LinkSet({})
for link in links:
    try:
        link.save()
    except:
        print(link.contents())
        link.delete()