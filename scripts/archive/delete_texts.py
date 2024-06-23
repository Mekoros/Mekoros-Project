# -*- coding: utf-8 -*-
"""
Delete texts
"""

import sys
import os

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, p)
sys.path.insert(0, p + "/mekoros")
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from mekoros.texts import delete_text
from mekoros.system.database import db


texts = (
    "Parshat Bereshit",
    "RCA Ketubah Text",
    "Igrot Moshe ",
    "Derashos Maharal miPrague",
    "Sheiltot DeRav Achai",
    )

for text in texts:
    delete_text(text)