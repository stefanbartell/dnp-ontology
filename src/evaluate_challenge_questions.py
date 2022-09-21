
import os, json
import pandas as pd
from owlready2 import *
from pyld import jsonld

get_names = lambda ontoQuery: [item.name if type(item)==type(Thing) else str(item) for item in ontoQuery]

data = os.path.join('..','data')
filename = {"ontology":os.path.join(data,'external','ontologies',"structural_derivatives_benzene.owl"),
			"challenge_questions":os.path.join(data,"challenge-question.jsonld")}

onto = get_ontology(f'file://{filename["ontology"]}').load()

class aThing(Thing):
	pass

jld = json.load(open(filename['challenge_questions'],'r'))

cqs = jsonld.compact(jld["doc"],jld["context"])

for cq in jld["doc"]:
	performance = get_names(eval(cq["expression"]))
	print(f'Generated answer: {set(performance)}. Expected: {set(cq["true_answer"])}')
	print(set(cq["true_answer"]) == set(performance))

	# if cq["@type"] != "chemical_substance":
	# 	# performance = get_names(eval(cq["expression"])) # issues
	# 	performance = get_names(eval(cq["expression"])) # issues
	# else:
	# 	performance = "N/A"
	# print(f'Generated answer: {set(performance.split())}. Expected: {set(cq["true_answer"])}')
	# print(set(cq["true_answer"]) == set(performance.split()))


	#How to handle expressions?
	# taken care of

	#How to store performance results?
	# see below

columns1 = ["Challenge Question", "Expected Answer", "Generated Answer",
			"Correct?", "Partially Correct?", "Percentage Correct"]

data = []
for i in list(range(len(jld["doc"]))):
	data += [list(range(len(columns1)))]

performance_results = pd.DataFrame(data, columns = columns1)

def percent_in_set(set1, set2):
	set1len = len(set1)
	set2len = len(set2)
	counter = 0
	if set1len <= set2len:
		for element in set1:
			if element in set2:
				counter += 1
		return counter/set2len*100
	else:
		for element in set2:
			if element in set1:
				counter += 1
		return counter/set1len*100

for i in range(len(jld["doc"])):
	cq = jld["doc"][i]
	# cq_label = cq['label']
	cq_label = i+1
	performance_results.loc[performance_results.index[i], 'Challenge Question'] = cq_label
	performance = get_names(eval(cq["expression"]))
	generated_answer = set(performance)
	performance_results.loc[performance_results.index[i], 'Generated Answer'] = str(generated_answer)
	expected_answer = set(cq["true_answer"])
	performance_results.loc[performance_results.index[i], 'Expected Answer'] = str(expected_answer)
	if generated_answer == expected_answer:
		performance_results.loc[performance_results.index[i], 'Correct?'] = 1
	else:
		performance_results.loc[performance_results.index[i], 'Correct?'] = 0
	if len(generated_answer.intersection(expected_answer)) > 0 or len(expected_answer.intersection(generated_answer)) > 0:
		performance_results.loc[performance_results.index[i], 'Partially Correct?'] = 1
	else:
		performance_results.loc[performance_results.index[i], 'Partially Correct?'] = 0
	performance_results.loc[performance_results.index[i], 'Percentage Correct'] = percent_in_set(generated_answer, expected_answer)

performance_results.to_csv('performance_results.csv', index=False)
