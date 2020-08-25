#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTHOR

    Sébastien Le Maguer <sebastien.lemaguer@adaptcentre.ie>

DESCRIPTION

LICENSE
    This script is in the public domain, free from copyrights or restrictions.
    Created: 20 August 2020
"""

# System/default
import sys
import os

# Yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


# Load phonetic list
with open("list_ph.yaml") as f_yaml:
    ph = load(f_yaml, Loader=Loader)

# Load Categories
with open("./categories.yaml") as f_yaml:
    cat_map = load(f_yaml, Loader=Loader)

cat_list = ["Phoneme"]
for cat in cat_map:
    cat_list.extend(cat_map[cat])

nb_cats = len(cat_list) - 1
print("\t".join(cat_list))
for p in ph:
    print("%s%s" % (p, "\t"*nb_cats))
