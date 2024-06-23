import django
django.setup()
import os
import json
from mekoros.model import *
from mekoros.system import exceptions
from mekoros.system.database import db


db.media.drop()

directory = 'data/tmp/pockettorah_audio/'
for filename in os.listdir(directory):
    with open(directory + filename) as json_file:
        data = json.load(json_file)
        data["source"] = "PocketTorah"
        data["source_he"] = "\"פאקט\"-תורה"
        data["description_he"] = "הקלטות שמע של פרשות השבוע באמצעות \"פאקט-תורה\" בסגנון הקריאה של א. בינדר ול.אוורי."

        db.media.save(data) # saves a single record
        db.media.ensure_index("ref.mekoros_ref")
