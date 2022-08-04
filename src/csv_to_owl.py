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

# create the chemical compound class
class chemical_compound(continuant):
    namespace = onto

# create new group classes under continuant class named after groups in csv file
for group in groups:
    with onto:
        NewClass = types.new_class(group, (chemical_compound,))

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
# weightloss_standardised_mapping_term = list(set(kb_dnp_sub.loc[kb_dnp_sub['GROUP'] == 'Weightloss', 'STANDRADISED MAPPING TERM']))

def lowerplussmt(astr):
    astr = astr.lower().replace(" ", "_").replace("-", "_")
    astr = astr+"_standardised_mapping_term"
    return astr

# weightloss_standardised_mapping_term = sorted(list(map(lowerplussmt, weightloss_standardised_mapping_term)))

# print(weightloss_standardised_mapping_term)

# add standardised mapping terms under weightloss class
# for term in weightloss_standardised_mapping_term:
#     name = "onto."+"weightloss"+"_group"
#     with onto:
#         NewClass = types.new_class(term, (eval(name),))

groups_original = sorted(list(set(kb_dnp_sub.loc[:,"GROUP"])))

def lowerplusterm(astr):
    astr = astr.lower().replace(" ", "_").replace("-", "_")
    astr = astr+"_term"
    return astr

def lowerplusentity(astr):
    astr = astr.lower().replace(" ", "_").replace("-", "_")
    astr = astr+"_entity"
    return astr

for group in groups_original:
    standardised_mapping_term = sorted(list(set(kb_dnp_sub.loc[kb_dnp_sub['GROUP'] == group, 'STANDRADISED MAPPING TERM'])))
    for term1 in standardised_mapping_term:
        name1 = "onto."+lowerplusgroup(group)
        with onto:
            NewClass = types.new_class(lowerplussmt(term1), (eval(name1),))
        terms = sorted(list(set(kb_dnp_sub.loc[kb_dnp_sub['STANDRADISED MAPPING TERM'] == term1, 'TERMS'])))
        for term2 in terms:
            name2 = "onto."+lowerplussmt(term1)
            with onto:
                NewClass = types.new_class(lowerplusterm(term2), (eval(name2),))
            entities = sorted(list(set(kb_dnp_sub.loc[kb_dnp_sub['TERMS'] == term2, 'ENTITY'])))
            for entity in entities:
                name3 = "onto."+lowerplusterm(term2)
                with onto:
                    NewClass = types.new_class(lowerplusentity(entity), (eval(name3),))

# create the is instance of property
# class is_instance_of(Property):
#     ontology = onto
#     domain = [continuant]
#     range = [continuant]
# code works, but property doesn't show up in object properties

# example given in documentation
# my_drug.has_for_ingredient.append(acetaminophen)

# alkaloid_group.is_instance_of.append(continuant)
# doesn't work

# onto.alkaloid_group.is_instance_of.append(onto.continuant)
# doesn't work

# onto.alkaloid_group.is_instance_of(onto.continuant)
# doesn't work

# print(onto.alkaloid_group.is_instance_of)


# tried copying ontology elements from documentation
# https://pythonhosted.org/Owlready/properties.html
# class Drug(Thing):
#     ontology = onto
#
# class Ingredient(Thing):
#     ontology = onto
#
# class has_for_ingredient(Property):
#     ontology = onto
#     domain = [Drug]
#     range = [Ingredient]
#
# my_drug = Drug("my_drug")
# doesn't work
#
# acetaminophen = Ingredient("acetaminophen")
#
# my_drug.has_for_ingredient.append(acetaminophen)
#
# print(my_drug.has_for_ingredient)

# from https://owlready2.readthedocs.io/en/latest/properties.html
# code works
with onto:
    class Drug(Thing):
        pass
    class Ingredient(Thing):
        pass
    class has_for_ingredient(ObjectProperty):
        domain = [Drug]
        range = [Ingredient]

with onto:
    class has_for_ingredient(Drug >> Ingredient):
        pass
my_drug = Drug("my_drug")

acetaminophen = Ingredient("acetaminophen")

my_drug.has_for_ingredient = [acetaminophen]

# =========

with onto:
    class is_instance_of(ObjectProperty):
        domain = [Thing]
        range = [Thing]

onto.continuant.is_instance_of = [Thing]

onto.chemical_compound.is_instance_of = [continuant]

# with onto:
#     class is_instance_of(onto.continuant >> onto.alkaloid_group):
#         pass

# need to reproduce onto.alkaloid_group.is_instance_of = [onto.continuant]
onto.alkaloid_group.is_instance_of = [onto.chemical_compound]

# eval("onto.alkaloid_group.is_instance_of") = [onto.continuant]
# SyntaxError: can't assign to function call

# "onto.alkaloid_group.is_instance_of" = [onto.continuant]
# SyntaxError: can't assign to literal

name = eval("onto.alkaloid_group.is_instance_of")
name = [onto.continuant]
# doesn't work


for group in groups:
    name = eval("onto."+group+".is_instance_of")
    name = [onto.continuant]
# doesn't work

onto.save(file = "kb_dnp_sub2.owl")
