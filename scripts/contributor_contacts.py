# -*- coding: utf-8 -*-
#!/usr/bin/python2.6

import sys
import os
import pymongo

from mekoros.model import *
from mekoros.settings import *
from mekoros.system.database import db


out = ""

contributors = HistorySet().distinct("user")
sheet_makers = db.sheets.distinct("owner")
users        = contributors + sheet_makers

for uid in users:
    user =  UserProfile(id=uid)
    tags =  ["Textual Contributor"] if uid in contributors else []
    tags += ["Source Sheet Maker"] if uid in sheet_makers else [] 
    tags =  ", ".join(tags)
    out += "%s\t%s\t%s\t%s\n" % (user.first_name, user.last_name, user.email, tags)

print(out)

f = open('../tmp/contacts.csv', 'w+')
f.write(out)
f.close()
