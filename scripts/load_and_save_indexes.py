
from mekoros.model import *

for indx in IndexSet():
    try:
        indx.save()
    except Exception as e:
        print("Caught exception: {}".format(e))