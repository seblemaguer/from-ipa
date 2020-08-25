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

# Pandas TSV
import pandas as pd
import numpy as np

########################################################################################################

# Load Categories
with open("./data/categories.yaml") as f_yaml:
    cat_map = load(f_yaml, Loader=Loader)

cat_set = []
for cat in cat_map:
    cat_set.extend(cat_map[cat])
cat_set = set(cat_set)

# Load DataFrame
df = pd.read_csv("data/table.tsv", sep="\t")

ph_data = dict()
for _, r in df.iterrows():
    validate = []
    undefined = []
    ph = None

    for k, v in r.iteritems():
        if k != "Phoneme":
            if k not in cat_set:
                print("%s is not a known category!" % k)

        if (isinstance(v,float)) and (np.isnan(v)):
            continue
        elif k == "Phoneme":
            ph = v
        elif v == "0":
            undefined.append(k)
        else:
            validate.append(k)


    ph_data[ph] = {"Validate": validate, "Undefined": undefined}


with open("data/list_ph.yaml", "w") as f_yaml:
    dump(ph_data, f_yaml, Dumper=Dumper)
