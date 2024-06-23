import django
django.setup()
from mekoros.model import library

library.rebuild_toc()