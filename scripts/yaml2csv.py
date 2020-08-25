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

# Data frame
import pandas as pd

# Load phonetic list
with open("data/list_ph.yaml") as f_yaml:
    ph = load(f_yaml, Loader=Loader)

# Load Categories
with open("data/categories.yaml") as f_yaml:
    cat_map = load(f_yaml, Loader=Loader)

# Generate category lists
cat_list = ["Phoneme"]
for cat in cat_map:
    cat_list.extend(cat_map[cat])

# Generate DataFrame
matrix = []
for p in ph:
    tmp_list = [p]
    for cat in cat_list[1:]:
        if cat in ph[p]["Undefined"]:
            tmp_list.append("0")
        elif cat in ph[p]["Validate"]:
            tmp_list.append("+")
        else:
            tmp_list.append("")

    matrix.append(tmp_list)
df = pd.DataFrame(matrix, columns=cat_list)

# Save the TSV file
df.to_csv("data/table.tsv", index=False, sep="\t")
