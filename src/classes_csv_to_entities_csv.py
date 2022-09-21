import types, os
import pandas as pd
from owlready2 import *

# filename = "kb_dnp_sub_curated"
# filename = "kb_dnp_symp_curated"
filename = "kb_dnp_sub_symp_curated"

kb_dnp = pd.read_csv(os.path.join('..','data','external', filename+'.csv'))


def lowerplus(aStr):
    #Don't shadow reserved keywords (like str). It can have unintended consequences
    aStr = str(aStr)
    aStr = aStr.lower().replace(" ", "_").replace("-", "_")
    return aStr

def lowerplusgroup(aStr):
    aStr = lowerplus(aStr)
    aStr = f'{aStr}_group'
    return aStr

def lowerplussmt(astr):
    astr = lowerplus(astr)
    astr = astr+"_standardized_mapping_term"
    return astr

def lowerplusstl(astr):
    astr = lowerplus(astr)
    astr = astr+"_standardized_textual_label"
    return astr

def lowerplustm(astr):
    astr = lowerplus(astr)
    astr = astr+"_textual_mention"
    return astr

domains = ["chemical_substance_domain", "symptom_domain"]


groups = sorted(list(set(kb_dnp.loc[:,"GROUP"])))
groups = sorted(list(map(lowerplusgroup, groups)))

standardized_mapping_terms = sorted(list(set(kb_dnp.loc[:,"STANDARDIZED MAPPING TERM"])))
standardized_mapping_terms = sorted(list(map(lowerplussmt, standardized_mapping_terms)))

standardized_textual_labels = sorted(list(set(kb_dnp.loc[:,"STANDARDIZED TEXTUAL LABEL"])))
standardized_textual_labels = sorted(list(map(lowerplusstl, standardized_textual_labels)))

textual_mentions = sorted(list(set(kb_dnp.loc[:,"TEXTUAL MENTION"])))
textual_mentions = sorted(list(map(lowerplustm, textual_mentions)))

classes = domains + textual_mentions + standardized_textual_labels + standardized_mapping_terms + groups

data = []
for i in range(len(classes)):
    data = data + [["Q"+str(i+1), classes[i], "description"]]

df = pd.DataFrame(data)
df.to_csv('entities.csv', index=False, header=False)
