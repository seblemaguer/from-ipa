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
import math
import pandas as pd

# Load phonetic list
with open("data/list_ph.yaml") as f_yaml:
    ph = load(f_yaml, Loader=Loader)

# Load Diacritics
with open("data/diacritics.yaml") as f_yaml:
    diac = load(f_yaml, Loader=Loader)
    for d in diac:
        if d in ph:
            raise Exception("\"%s\" should not be there!")
        ph[d] = diac[d]

# Load alphabet conversion
alphabet2ipa = dict()
ipa2alphabet = dict()
with open("alphabet/arpabet.tsv") as f_arpabet:
    for l in f_arpabet:
        elts = l.strip().split("\t")

        # Patchy patchy
        if elts[1] == "ɝ":
            elts[1] = "ɜ" + "˞"
        if elts[1] == "ɚ":
            elts[1] = "ə" + "˞"
        alphabet2ipa[elts[0].lower()] = elts[1]
        ipa2alphabet[elts[1]] = elts[0].lower()


# Generate map
cat = dict()
for lab in ipa2alphabet:
    for p in lab:
        try :
            for c in ph[p]["Validate"]:
                if c not in cat:
                    cat[c] = set()
                cat[c].add(ipa2alphabet[lab])
        except KeyError:
            print("Ouppps: %s[%s] %s" % (ipa2alphabet[lab], lab, p))

# Load separator

separator_df = pd.read_csv("separator.tsv", sep="\t")
separator_df.fillna('', inplace=True)
for _, r in separator_df.iterrows():
    for c in cat:
        tmp = "%s,%s" % (r["Right"], r["Left"])
        tmp = str(r["Left"]) + tmp.join(cat[c]) + str(r["Right"])
        line = "QS \"%s-%s\" {%s}" % (r["Prefix"], c, tmp)
        print(line)

    for p in alphabet2ipa:
        tmp = str(r["Left"]) + p + str(r["Right"])
        line = "QS \"%s-%s\" {%s}" % (r["Prefix"], p, tmp)
        print(line)

    print("")
    print("")
