
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
	#How to store performance results?

# columns1 = ["Challenge Question", "Expected Answer", "Generated Answer", "Correct?"]

# data = []
# for i in list(range(len(jld["doc"]))):
# 	data += [list(range(len(columns1)))]

# performance_results = pd.DataFrame(data, columns = columns1)

# for i in range(len(jld["doc"])):
# 	cq = jld["doc"][i]
# 	cq_label = cq['label']
# 	performance_results.loc[performance_results.index[i], 'Challenge Question'] = cq_label
# 	performance = get_names(eval(cq["expression"]))
# 	generated_answer = set(performance.split())
# 	performance_results.loc[performance_results.index[i], 'Generated Answer'] = str(generated_answer)
# 	expected_answer = set(cq["true_answer"])
# 	performance_results.loc[performance_results.index[i], 'Expected Answer'] = str(expected_answer)
# 	if generated_answer == expected_answer:
# 		performance_results.loc[performance_results.index[i], 'Correct?'] = 1
# 	else:
# 		performance_results.loc[performance_results.index[i], 'Correct?'] = 0


# performance_results.to_csv('performance_results.csv')
