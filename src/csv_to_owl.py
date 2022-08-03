import types, os 

import pandas as pd

from owlready2 import *

kb_dnp_sub = pd.read_csv(os.path.join('..','data','external','kb_dnp_sub.csv'))

groups = list(set(kb_dnp_sub.loc[:,"GROUP"]))

def lowerplusgroup(aStr):
    #Don't shadow reserved keywords (like str). It can have unintended consequences
    aStr = aStr.lower().replace(" ", "_").replace("-", "_")
    aStr = f'{aStr}_group'
    return aStr

groups = sorted(list(map(lowerplusgroup, groups)))

# print(groups)

onto = get_ontology("http://test.org/onto.owl")

# create the continuant class
class continuant(Thing):
    namespace = onto

# create new group classes under continuant class named after groups in csv file
for group in groups:
    with onto:
        NewClass = types.new_class(group, (continuant,))

# print(list(onto.classes()))

# create subclass under each group class in two different ways
# way 1
# for group in groups:
#     name = "onto."+group
#     with onto:
#         NewClass = types.new_class("subclass", (eval(name),))

# way 2
# for group in groups:
#     name = "onto."+group
#     class subclass(eval(name)):
#         namespace = onto

# get the values of column 'STANDRADISED MAPPING TERM' that align with GROUP Weightloss
weightloss_standardised_mapping_term = list(set(kb_dnp_sub.loc[kb_dnp_sub['GROUP'] == 'Weightloss', 'STANDRADISED MAPPING TERM']))

def lowerplussmt(str):
    str = str.lower().replace(" ", "_").replace("-", "_")
    str = str+"_standardised_mapping_term"
    return str

weightloss_standardised_mapping_term = sorted(list(map(lowerplussmt, weightloss_standardised_mapping_term)))

# print(weightloss_standardised_mapping_term)

# add standardised mapping terms under weightloss class
for term in weightloss_standardised_mapping_term:
    name = "onto."+"weightloss"+"_group"
    with onto:
        NewClass = types.new_class(term, (eval(name),))

groups_original = list(set(kb_dnp_sub.loc[:,"GROUP"]))

def lowerplusterm(str):
    str = str.lower().replace(" ", "_").replace("-", "_")
    str = str+"_term"
    return str

def lowerplusentity(str):
    str = str.lower().replace(" ", "_").replace("-", "_")
    str = str+"_entity"
    return str

for group in groups_original:
    standardised_mapping_term = list(set(kb_dnp_sub.loc[kb_dnp_sub['GROUP'] == group, 'STANDRADISED MAPPING TERM']))
    for term1 in standardised_mapping_term:
        name1 = "onto."+lowerplusgroup(group)
        with onto:
            NewClass = types.new_class(lowerplussmt(term1), (eval(name1),))
        terms = list(set(kb_dnp_sub.loc[kb_dnp_sub['STANDRADISED MAPPING TERM'] == term1, 'TERMS']))
        for term2 in terms:
            name2 = "onto."+lowerplussmt(term1)
            with onto:
                NewClass = types.new_class(lowerplusterm(term2), (eval(name2),))
            entities = list(set(kb_dnp_sub.loc[kb_dnp_sub['TERMS'] == term2, 'ENTITY']))
            for entity in entities:
                name3 = "onto."+lowerplusterm(term2)
                with onto:
                    NewClass = types.new_class(lowerplusentity(entity), (eval(name3),))

onto.save(file = "kb_dnp_sub2.owl")
