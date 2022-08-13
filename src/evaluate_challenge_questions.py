import os, json 

from owlready2 import *
from pyld import jsonld

get_names = lambda ontoQuery: ' '.join(item.name for item in ontoQuery)

data = os.path.join('..','data')
filename = {"ontology":os.path.join(data,'external','ontologies',"structural_derivatives_benzene.owl"),
			"challenge_questions":os.path.join(data,"challenge-question.jsonld")}

onto = get_ontology(f'file://{filename["ontology"]}').load()

jld = json.load(open(filename['challenge_questions'],'r'))

cqs = jsonld.compact(jld["doc"],jld["context"])

for cq in jld["doc"]:
	performance = get_names(eval(cq["expression"]))
	print(f'Generated answer:{set(performance.split())}. Expected: {set(cq["true_answer"])}')
	print(set(cq["true_answer"]) == set(performance.split()))

	#How to handle expressions?
	#How to store performance results?
