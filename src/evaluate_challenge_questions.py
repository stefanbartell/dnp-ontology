import os, json

import pandas as pd

from owlready2 import *

from pyld import jsonld

def percent_in_set(s1,s2):
	if len(s1) < len(s2):
		return percent_in_set(s2,s1)
	else:
		return round(len(s1&s2)/len(s1) * 100,2)

get_names = lambda ontoQuery: [item.name if type(item)==type(Thing) else str(item) for item in ontoQuery]

data = os.path.join('..','data')
filename = {"ontology":os.path.join(data,'external','ontologies',"structural_derivatives_benzene.owl"),
			"challenge_questions":os.path.join(data,"challenge-question.jsonld")}

onto = get_ontology(f'file://{filename["ontology"]}').load()

jld = json.load(open(filename['challenge_questions'],'r'))
cqs = jsonld.compact(jld["doc"],jld["context"])

evaluation = []

for cq in jld["doc"]:
	payload = {}

	performance = get_names(eval(cq["expression"]))

	payload["CQID"] = "stuff" #Implement this line
	payload["Expected Answer"] = set(performance)
	payload["Generated Answer"] = set(cq["true_answer"])
	payload["Correct?"] = int(set(cq["true_answer"]) == set(performance))

	lb = 0 #lower bound
	ub = max(len(payload["Generated Answer"]),len(payload["Expected Answer"])) #upper bound

	payload["Partially Correct?"] = int(lb<(len(payload["Expected Answer"]&payload["Generated Answer"]))<ub)
	payload["Percentage Correct"] = percent_in_set(payload["Expected Answer"],payload["Generated Answer"])

	evaluation += [payload]

results = pd.DataFrame(evaluation)
results.to_csv(os.path.join(data,'performance_results.csv'), index=False)
