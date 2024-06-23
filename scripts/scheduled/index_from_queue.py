# -*- coding: utf-8 -*-
#!/usr/local/bin/python

import sys
import os
import django
django.setup()

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
sys.path.insert(0, path + "/mekoros")

from mekoros.settings import *
from mekoros.search import index_from_queue

index_from_queue()
