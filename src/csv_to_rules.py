import types, os
import pandas as pd
from owlready2 import *

# filename = "kb_dnp_sub_curated"
# filename = "kb_dnp_symp_curated"
filename = "kb_dnp_sub_symp_curated"

kb_dnp = pd.read_csv(os.path.join('..','data','external', filename+'.csv'))
# following https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
kb_dnp = kb_dnp.reset_index()

def lowerplus(aStr):
    #Don't shadow reserved keywords (like str). It can have unintended consequences
    aStr = str(aStr)
    aStr = aStr.lower().replace(" ", "_").replace("-", "_")
    return aStr

# example: {"label": "SUBSTANCE", "pattern": [{"LOWER": "testosterone"}]}
rules = []
for index, row in kb_dnp.iterrows():
    subsymp = row['SUBSTANCE/SYMPTOM']
    subsymp = lowerplus(subsymp)
    term = row['STANDARDIZED MAPPING TERM']
    term = lowerplus(term)
    rules += ['{"label": "'+subsymp.upper()+'", "pattern": [{"LOWER": "'+term.lower()+'"}]}']

with open('rules.txt', "w") as f:
    rules = sorted(list(set(rules)))
    i = len(rules)
    for rule in rules:
        i = i-1
        if i > 0:
            f.write(rule+", ")
        if i <= 0:
            f.write(rule)
