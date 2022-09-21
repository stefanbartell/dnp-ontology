### Challenge Questions

A challenge question is a query to an ontology that yields a response whose content is already known. Challenge questions can function as consistency checks, positive controls, and negative controls. 

#### Role of Challenge Questions in Evaluating the Ontology 


#### Storage of Challenge Questions. 
This project uses `owlready`. In `owlready`, queries are represnted as strings or chains of Python functions. Our task is to create a database of challenge questions that also tracks when they are used and on what version of the software they were used. A secondary goal is to do this record-keeping as painlessly as possible. 

#### Starting Format


```json
	{"@context":"https://json-ld.org/contexts/person.jsonld",
	 "@type":"challenge-question",
	 "@id": "", //have to think about this one
	 "@name": "Name of challenge question",
	 "@code-type": "", //SPARQL query or OWL ready expression, does this need an @
	 "@code-location":{"@name":"","@value":""},
	 "performance":"" //Will be nested?
	 }
```