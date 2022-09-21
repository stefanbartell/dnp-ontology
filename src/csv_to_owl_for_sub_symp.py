import types, os
import pandas as pd
from owlready2 import *

# filename = "kb_dnp_sub_curated"
# filename = "kb_dnp_symp_curated"
filename = "kb_dnp_sub_symp_curated"

kb_dnp = pd.read_csv(os.path.join('..','data','external', filename+'.csv'))

# subsymp = ["substance", "symptom"]

groups = sorted(list(set(kb_dnp.loc[:,"GROUP"])))

groups_original = groups

substance_groups = []
symptom_groups = []
for group in groups:
    if "substance" in str(kb_dnp.loc[kb_dnp['GROUP'] == group, 'DOMAIN']):
        substance_groups += [group]
    if "symptom" in str(kb_dnp.loc[kb_dnp['GROUP'] == group, 'DOMAIN']):
        symptom_groups += [group]

substance_groups_original = sorted(list(set(substance_groups)))
symptom_groups_original = sorted(list(set(symptom_groups)))

# print(substance_groups)
# print(symptom_groups)

# print(len(substance_groups))
# print(len(symptom_groups))

def lowerplus(aStr):
    #Don't shadow reserved keywords (like str). It can have unintended consequences
    aStr = str(aStr)
    aStr = aStr.lower().replace(" ", "_").replace("-", "_")
    return aStr

def lowerplusgroup(aStr):
    #Don't shadow reserved keywords (like str). It can have unintended consequences
    aStr = str(aStr)
    aStr = aStr.lower().replace(" ", "_").replace("-", "_")
    aStr = f'{aStr}_group'
    return aStr

groups = sorted(list(map(lowerplusgroup, groups)))
substance_groups = sorted(list(map(lowerplusgroup, substance_groups)))
symptom_groups = sorted(list(map(lowerplusgroup, symptom_groups)))

onto = get_ontology("http://test.org/onto.owl")

# create the chemical substance class
class chemical_substance(Thing):
    namespace = onto

# # create the chemical substance label class
# class chemical_substance_label(Thing):
#     namespace = onto

# create the chemical substance class
class symptom(Thing):
    namespace = onto

# # create the chemical substance label class
# class symptom_label(Thing):
#     namespace = onto

# # create new group classes under chemical_substance class named after groups in csv file
# for group in groups:
#     with onto:
#         NewClass = types.new_class(group, (chemical_substance,))


# # create new subsymp classes under generically_dependent_continuant class
# for subsymp in ["chemical_substance", "symptom"]:
#     with onto:
#         NewClass = types.new_class(subsymp, (generically_dependent_continuant,))

# # create new group classes under substance or symptom class named after groups in csv file
# for group in groups:
#     if group in substance_groups:
#         with onto:
#             NewClass = types.new_class(group, (chemical_substance,))
#     if group in symptom_groups:
#         with onto:
#             NewClass = types.new_class(group, (symptom,))


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

# get the values of column 'STANDARDIZED MAPPING TERM' that align with GROUP Weightloss
# weightloss_standardized_mapping_term = list(set(kb_dnp.loc[kb_dnp['GROUP'] == 'Weightloss', 'STANDARDIZED MAPPING TERM']))

def lowerplussmt(astr):
    astr = astr.lower().replace(" ", "_").replace("-", "_")
    astr = astr+"_standardized_mapping_term"
    return astr

def lowerplusstl(astr):
    astr = astr.lower().replace(" ", "_").replace("-", "_")
    astr = astr+"_standardized_textual_label"
    return astr

def lowerplustm(astr):
    astr = astr.lower().replace(" ", "_").replace("-", "_")
    astr = astr+"_textual_mention"
    return astr

subsymp = ["chemical_substance", "symptom"]
headings = ["standardized_textual_label", "standardized_mapping_term", "group"]

for subsymp1 in subsymp:
    for heading in headings:
        NewClass = types.new_class(subsymp1+"_"+heading, (eval(subsymp1),))

# for subsymp1 in subsymp:
#     NewClass = types.new_class(subsymp1+"_"+"textual_mention", (eval("onto."+subsymp1+"_"+"standardized_textual_label"),))


for group in groups_original:
    if group in substance_groups_original:
        with onto:
            NewClass = types.new_class(lowerplusgroup(group), (eval("onto.chemical_substance_group"),))
    if group in symptom_groups_original:
        with onto:
            NewClass = types.new_class(lowerplusgroup(group), (eval("onto.symptom_group"),))

for subsymp1 in subsymp:
    standardized_mapping_terms = sorted(list(set(kb_dnp.loc[kb_dnp['DOMAIN'] == subsymp1, 'STANDARDIZED MAPPING TERM'])))
    for term1 in standardized_mapping_terms:
        with onto:
            NewClass = types.new_class(lowerplussmt(term1), (eval("onto."+subsymp1+"_standardized_mapping_term"),))
    standardized_textual_labels = sorted(list(set(kb_dnp.loc[kb_dnp['DOMAIN'] == subsymp1, 'STANDARDIZED TEXTUAL LABEL'])))
    for label in standardized_textual_labels:
        with onto:
            NewClass = types.new_class(lowerplusstl(label), (eval("onto."+subsymp1+"_standardized_textual_label"),))
            # NewClass = types.new_class(lowerplustm(label), (eval("onto."+lowerplusstl(label)),))
            textual_mentions = sorted(list(set(kb_dnp.loc[kb_dnp['STANDARDIZED TEXTUAL LABEL'] == label, 'TEXTUAL MENTION'])))
            for mention in textual_mentions:
                with onto:
                    NewClass = types.new_class(lowerplustm(mention), (eval("onto."+lowerplusstl(label)),))


# create the is instance of property
# class is_instance_of(Property):
#     ontology = onto
#     domain = [generically_dependent_continuant]
#     range = [generically_dependent_continuant]
# code works, but property doesn't show up in object properties

# example given in documentation
# my_drug.has_for_ingredient.append(acetaminophen)

# alkaloid_group.is_instance_of.append(generically_dependent_continuant)
# doesn't work

# onto.alkaloid_group.is_instance_of.append(onto.generically_dependent_continuant)
# doesn't work

# onto.alkaloid_group.is_instance_of(onto.generically_dependent_continuant)
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
# with onto:
#     class Drug(Thing):
#         pass
#     class Ingredient(Thing):
#         pass
#     class has_for_ingredient(ObjectProperty):
#         domain = [Drug]
#         range = [Ingredient]
#
# with onto:
#     class has_for_ingredient(Drug >> Ingredient):
#         pass
# my_drug = Drug("my_drug")
#
# acetaminophen = Ingredient("acetaminophen")
#
# my_drug.has_for_ingredient = [acetaminophen]

# =========

with onto:
    class is_instance_of(ObjectProperty):
        domain = [Thing]
        range = [Thing]

# with onto:
#     class is_label_for_chemical_substance(ObjectProperty):
#         domain = [chemical_substance_label]
#         range = [chemical_substance]
#
# with onto:
#     class is_label_for_symptom(ObjectProperty):
#         domain = [symptom_label]
#         range = [symptom]

# onto.generically_dependent_continuant.is_instance_of = [Thing]

onto.chemical_substance.is_instance_of = [Thing]

# onto.chemical_substance_label.is_instance_of = [Thing]

onto.symptom.is_instance_of = [Thing]

# onto.symptom_label.is_instance_of = [Thing]

# with onto:
#     class is_instance_of(onto.generically_dependent_continuant >> onto.alkaloid_group):
#         pass

# need to reproduce onto.alkaloid_group.is_instance_of = [onto.chemical_substance]
# onto.alkaloid_group.is_instance_of = [onto.chemical_substance]

# exec("onto.alkaloid_group.is_instance_of = [onto.chemical_substance]")
# works

# eval("onto.alkaloid_group.is_instance_of") = [onto.chemical_substance]
# SyntaxError: can't assign to function call

# [onto.chemical_substance] = eval("onto.alkaloid_group.is_instance_of")
# TypeError: cannot unpack non-iterable property object

# "onto.alkaloid_group.is_instance_of" = [onto.chemical_substance]
# SyntaxError: can't assign to literal

# [onto.chemical_substance] = "onto.alkaloid_group.is_instance_of"
# ValueError: too many values to unpack (expected 1)

# name = eval("onto.alkaloid_group.is_instance_of")
# name = [onto.chemical_substance]
# code runs but doesn't work

# name = eval("onto.alkaloid_group.is_instance_of")
# [onto.chemical_substance] = name
# TypeError: cannot unpack non-iterable property object

# name = eval("onto.alkaloid_group.is_instance_of")
# name = [chemical_substance]
# code runs but doesn't work

# name = eval("onto.alkaloid_group.is_instance_of")
# [chemical_substance] = name
# TypeError: cannot unpack non-iterable property object

# for group in substance_groups:
#     exec("onto."+group+".is_instance_of = [onto.chemical_substance]")
#
# for group in symptom_groups:
#     exec("onto."+group+".is_instance_of = [onto.symptom]")

# for group in groups:
#     name = eval("onto."+group+".is_instance_of")
#     name = [onto.chemical_substance]
# code runs but doesn't work

# # create object property relations
# for group in groups_original:
#     standardized_mapping_terms = sorted(list(set(kb_dnp.loc[kb_dnp['GROUP'] == group, 'STANDARDIZED MAPPING TERM'])))
#     for term1 in standardized_mapping_terms:
#         name1 = "onto."+lowerplusgroup(group)
#         term11 = "onto."+lowerplussmt(term1)
#         exec(term11 + ".is_instance_of = [" + name1 + "]")
#         standardized_textual_labels = sorted(list(set(kb_dnp.loc[kb_dnp['STANDARDIZED MAPPING TERM'] == term1, 'STANDARDIZED TEXTUAL LABEL'])))
#         for label in standardized_textual_labels:
#             name2 = "onto."+lowerplussmt(term1)
#             label2 = "onto."+lowerplusstl(label)
#             # exec(label2 + ".is_label_for_chemical_substance = [" + name2 + "]")
#             # commented out to avoid making standardized textual label a subclass of standardized mapping term
#             if group in substance_groups_original:
#                 exec(label2 + ".is_instance_of = [" + "onto.chemical_substance_label" + "]")
#             if group in symptom_groups_original:
#                 exec(label2 + ".is_instance_of = [" + "onto.symptom_label" + "]")
#             textual_mentions = sorted(list(set(kb_dnp.loc[kb_dnp['STANDARDIZED TEXTUAL LABEL'] == label, 'TEXTUAL MENTION'])))
#             for textual_mention in textual_mentions:
#                 name3 = "onto."+lowerplusstl(label)
#                 textual_mention2 = "onto."+lowerplustm(textual_mention)
#                 # exec(textual_mention2 + ".is_label_for_chemical_substance = [" + name2 + "]")
#                 # commented out to avoid making textual mention a subclass of standardized mapping term
#                 if group in substance_groups_original:
#                     exec(textual_mention2 + ".is_instance_of = [" + "onto.chemical_substance_label" + "]")
#                 if group in symptom_groups_original:
#                     exec(textual_mention2 + ".is_instance_of = [" + "onto.symptom_label" + "]")
#


# print(list(onto.classes()))

# === moving onto adding definitions to the ontology ===

# def unsuffix(astr):
#     astr = astr.replace('_group', '').replace('_standardized_mapping_term', '')
#     astr = astr.replace('_standardized_textual_label', '').replace('_textual_mention', '')
#     astr = astr.replace('_label', '')
#     return(astr)
#
# def unprefix(astr):
#     astr = astr.replace('onto.','')
#     return(astr)
#
# import requests as rq
# from bs4 import BeautifulSoup
# # for clss in list(onto.classes())[2:3]:
# # chemical substance
# # for clss in list(onto.classes())[3:4]:
# # alkaloid
# # for clss in list(onto.classes())[0:10]:
# for clss in list(onto.classes()):
#     # print(clss)
#     term = unprefix(unsuffix(str(clss)))
#
#     term2 = term.split('_')
#     # print(term2)
#     term3 = ''
#     for word in term2[0:1]:
#         term3 += word.capitalize()
#     for word in term2[1:]:
#         term3 += '_'+word.lower()
#
#     print(term3)
#     # term = unprefix(unsuffix(str(clss))).capitalize()
#     # print(term)
#     # label = term.replace('_', ' ').capitalize()
#     # print(label)
#     # url = "https://en.wiktionary.org/wiki/"+term
#     url = "https://en.wikipedia.org/wiki/"+term3
#
#     # html = open(url).read()
#     # soup = BeautifulSoup(html)
#
#     req = rq.get(url)
#     # print(req.text)
#     soup = BeautifulSoup(req.content, 'html.parser')
#
#     # modified code from https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
#
#     [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
#     visible_text = soup.getText()
#     # print(visible_text)
#
#     definition = visible_text.split("Jump to navigation\nJump to search\n")[1].split('\n\nContents\n')[0]
#     definition = definition.replace('\n\n', '\n').replace('\n', '. ').replace('..', '.').replace('. .', '.')
#     # definition = visible_text.split(".hatnote+link+.hatnote{margin-top:-0.5em}")[1]
#     if "Wikipedia does not have an article with this exact name." in definition:
#         print("Page not found.")
#     else:
#         print(definition)
#         clss.comment = "Wikipedia.org: "+definition
#
# # for clss in list(onto.classes())[3:4]:
# # alkaloid
# for clss in list(onto.classes())[0:10]:
# # for clss in list(onto.classes()):
#     # print(clss)
#     term = unprefix(unsuffix(str(clss))).replace('_', '-')
#     # print(term)
#     label = term.replace('-', ' ').capitalize()
#     print(label)
#     url = "https://www.dictionary.com/browse/"+term
#     req = rq.get(url)
#     # print(req.text)
#     soup = BeautifulSoup(req.content, 'html.parser')
#     html = str(soup)
#     # print(html)
#     # print(soup.prettify())
#     if label+" definition, " in html:
#         print("Definition found.")
#         definition = html.split('<meta content="'+label+" definition, ")[1].split('. See more."')[0]
#         print(definition)
#         clss.comment = "Dictionary.com: "+definition
#     if "No results found for" in html:
#         print("Definition not found.")

onto.save(file = filename+".owl")
