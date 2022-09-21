#!/usr/bin/env python
# coding: utf-8

import json, spacy, os

from spacy.language import Language

patterns = json.load(open(os.path.join('..','data','patterns.json')))
nlp = spacy.load("en_core_web_sm", disable=['ner'])

## One approach to extending pipline
# @Language.component("further_label_substances")
# def further_label_substances(doc):
#     return doc

ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(patterns)
#nlp.add_pipe('further_label_substances',after='entity_ruler')

# 4. Add patterns as Labels of "Symptoms" and "Substances" and corresponding pattern:
    # can use 'LEMMA' or 'LOWER' in pattern
        # LEMMA: (wikipedia) is the canonical form, dictionary form, or citation form of a set of words (headword)
            # e.g.: [be] mapping to [is, was or 's]
        # LOWER:  (SpaCy) is a token whose lowercase form matches “text”
            #  e.g.: [hello] mapping to [“Hello” or “HELLO”]

text = open(os.path.join('..','data','raw','comments_after_fixing_double_quotes.txt')).read()
doc = nlp(text)

outfile = os.path.join('..','data','output','complete-output-rule-based.txt')
with open(outfile, mode='wt', encoding='utf-8') as myfile:
    myfile.write("Name,Standardized Form,Classification\n")
    for ent in doc.ents:
        myfile.write(f'{ent.text},{ent.lemma_},{ent.label_}\n')

nlp.to_disk(os.path.join('..','models','rule-based'))


# Our unit tests show that it achieves desired performances precision 100% and recall 78.47% [(Substances: 66.57%),(Symptoms: 90.36%)]
# On change of pattern at input in point [4], we extended the algorithm by changing "LEMMA" to "LOWER", after which increased recall to 86.91% [(Substances: 90.82%),(Symptoms: 82.99%)]
