# -*- coding: utf-8 -*-
__author__ = 'stevenkaplan'
from mekoros.helper.schema import *
from mekoros.model import JaggedArrayNode

if __name__ == "__main__":
    map = {}
    map["Tomer Devorah 1"] = "Tomer Devorah, Introduction"
    for i in range(17):
        map["Tomer Devorah {}".format(i+2)] = 4

    x = JaggedArrayNode()
    x.add_primary_titles("HI", "HI")