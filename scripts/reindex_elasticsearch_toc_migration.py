import django
django.setup()
from mekoros.model import *
from mekoros.search import index_all_of_type_by_index_name

index_all_of_type_by_index_name('text', 'text-toc-migration')