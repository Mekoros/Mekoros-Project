# -*- coding: utf-8 -*-

from mekoros.system.database import db
from mekoros.export import prepare_text_for_export, write_text_doc_to_disk

texts = db.texts.find({"versionTitle": "JPS 1985 English Translation"})

for text in texts:
    write_text_doc_to_disk(
        prepare_text_for_export(text)
    )
