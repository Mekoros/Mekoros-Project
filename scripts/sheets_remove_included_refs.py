# -*- coding: utf-8 -*-
"""
Code stump to walk through all sources on sheets to find various settings
"""

from mekoros.model import *
from mekoros.system.database import db

db.sheets.update({}, {"$unset": {"included_refs": ""}}, multi=True)

