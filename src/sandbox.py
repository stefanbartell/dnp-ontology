# we can already do a lot with just owlready2
# see these pages for documentation
# https://owlready2.readthedocs.io/en/latest/onto.html
# https://owlready2.readthedocs.io/en/latest/class.html

from owlready2 import *
import os

get_names = lambda ontoQuery: ' '.join(item.name for item in ontoQuery)

filename = "structural_derivatives_benzene.owl"
path = os.path.join('..','data','external')
onto = get_ontology(f'file://{os.path.join(path,filename)}').load()

print("Challenge Questions")
query  = onto.phenol.is_structural_derivative_of
print(f'\t1. What compound is phenol a direct structural derivative of? Ans:{get_names(query)}')

challenge_qs = [{
    @type: challenge-question
    @label: "What compuonds is phenol a direct...."
    @expression: "onto.phenol.is_structural_derivative_of"
    @true_answer: ["benzene"]
    @true_answer_type: "object" | "relation"
},
{}]

#JSON-LD format

for challenge_q in challenge_qs:
    performance = exec("get_names(challenge_q[@expression])")
    #["benzene","toluene"]
    challenge_q[@performance] = (performance == challenge_q[@true_answer]) if challenge[@true_answer_type]=="object" else (performance % challenge_q[@true_answer])

for num in load(data):
    num += 1 

for num in [1,2,3]:
    num += 1

query = 1
print query +=1

query = 2
print query +=1 



# print(list(onto.properties()))
# prints a list of properties in the ontology

query = onto.phenol.subclasses()
print(f'\t2. What phenols does the ontology specify? Ans:{get_names(query)}')

query = onto.phenol.is_a
print(list(onto.phenol.is_a))
print("This didn't print chemical_compound, because this is not asserted in the ontology.")
""" prints
    benzene, is_structural_derivative_of.some(benzene),
    has_part.min(1, hydroxyl_group)
    but doesn't print chemical_compound
"""

# print(list(onto.phenol.ancestors()))
# prints benzene, chemical_compound, owl.Thing, phenol, continuant

# print(onto.phenol.INDIRECT_is_structural_derivative_of)
# prints chemical_compound, benzene, which is what we want
# shows that there is inheritance of is_strucural_derivative_of
# I think this is what it captures in SparQL:
# phenol is_structural_derivative_of some ?x

query = onto.phenol.INDIRECT_has_structural_derivative
print(f'\t3. What compounds eventually have phenol as a structural derivative? Ans: {get_names(query)}')
print("Prints nothing because OWL search looks only for explicitly declared relationships. It performs no reasoning.")
"""
  prints nothing
    although has_structural_derivative is the inverse of
    is_structural_derivative_of, it is not declared explicitly
"""

query = onto.phenol.INDIRECT_is_structural_derivative_of
print(f'\t3.5. What compounds is phenol eventually a structural derivative of? Ans: {get_names(query)}')
print("Prints chemical_compound benzene. shows that there is inheritance of is_structural_derivative_of")
"""
  prints chemical_compound benzene
  shows that there is inheritance of is_structural_derivative_of
"""

# print(onto.phenol.get_properties())
# doesn't work
print("The query onto.phenol.get_properties() fails because the method assumes an Individual not a Class.")

# ====== Moving on to querying the ontology using sparql ======



sparql_query = list(default_world.sparql("""
SELECT (COUNT(?x) AS ?nb)
{ ?x a owl:Class . }
"""))[0][0]

print(f'\t4. How many classes are there? Owlready: {len(list(onto.classes()))}. SPARQL: {sparql_query}.')

query = default_world.sparql("""
    SELECT ?s
    { ?s ?v ?o .
      ?o rdfs:label 'phenol' .
      ?v rdfs:label 'is structural derivative of'}
    """) #Pay attention to single and double quotes
print(f'\t5. What substances are a structural derivative of phenol? Ans:{list(query)}')
print('\t\tThe list is empty because the ontology uses the SOME restriction.')
print('\t\tThe semantics of our query are more accurately expressed by:')
print('\t\tWhat substances CAN BE CONSIDERED a structural derivative of phenol?')

query = list(default_world.sparql("""
    SELECT ?s
    {
        ?s rdfs:subClassOf [owl:onProperty ?v; owl:someValuesFrom/rdfs:subClassOf* ?o]
        ?o rdfs:label 'phenol' .
        ?v rdfs:label 'is structural derivative of'
    }
    """))
print(f'\t\tTHIS WORKS to print what is a structural derivative of phenol: {[item[0].name for item in query]}')


print('How to print what phenol is a structural derivative of?')

print('Selecting ?o instead of ?s')
query = list(default_world.sparql("""
    SELECT ?o
    {
        ?s rdfs:subClassOf [owl:onProperty ?v; owl:someValuesFrom/rdfs:subClassOf* ?o]
        ?o rdfs:label 'phenol' .
        ?v rdfs:label 'is structural derivative of'
    }
    """))
print(f'\t\tThis just prints phenol four times: {[item[0].name for item in query]}')


print('Switching s and o and selecting ?o instead of ?s')
query = list(default_world.sparql("""
    SELECT ?o
    {
        ?s rdfs:label 'phenol'
        ?o rdfs:subClassOf [owl:onProperty ?v; owl:someValuesFrom/rdfs:subClassOf* ?o]  .
        ?v rdfs:label 'is structural derivative of'
    }
    """))
print(f'\t\tThis does not work: Prints most of the classes in the ontology. {[item[0].name for item in query]}')


print('Switching s and o and selecting ?o instead of ?s and replacing ?o in 2nd line with ?s')
query = list(default_world.sparql("""
    SELECT ?o
    {
        ?s rdfs:label 'phenol'
        ?o rdfs:subClassOf [owl:onProperty ?v; owl:someValuesFrom/rdfs:subClassOf* ?s]  .
        ?v rdfs:label 'is structural derivative of'
    }
    """))
print(f'\t\tThis does not work: Prints structural derivatives of phenol again {[item[0].name for item in query]}')


print('Selecting v instead of s')
query = list(default_world.sparql("""
    SELECT ?v
    {
        ?s rdfs:subClassOf [owl:onProperty ?v; owl:someValuesFrom/rdfs:subClassOf* ?o]
        ?o rdfs:label 'phenol' .
        ?v rdfs:label 'is structural derivative of'
    }
    """))
print(f'\t\tTHIS does not work. just prints is_structural_derivative_of 4 times: {[item[0].name for item in query]}')


print('Switching the order of ?o and ?v syntax in ?s')
query = list(default_world.sparql("""
    SELECT ?s
    {
        ?s rdfs:subClassOf [owl:someValuesFrom/rdfs:subClassOf* ?o; owl:onProperty ?v]
        ?o rdfs:label 'phenol' .
        ?v rdfs:label 'is structural derivative of'
    }
    """))
print(f'\t\tThis does not work: Prints structural derivatives of phenol again {[item[0].name for item in query]}')


print('Switching ?o and ?v in the ?s line')
query = list(default_world.sparql("""
    SELECT ?s
    {
        ?s rdfs:subClassOf [owl:onProperty ?o; owl:someValuesFrom/rdfs:subClassOf* ?v]
        ?o rdfs:label 'phenol' .
        ?v rdfs:label 'is structural derivative of'
    }
    """))
print(f'\t\tTHIS does not work. Prints the empty list: {[item[0].name for item in query]}')


print('Switching "is structural derivative of" to "has structural derivative"')
query = list(default_world.sparql("""
    SELECT ?s
    {
        ?s rdfs:subClassOf [owl:onProperty ?v; owl:someValuesFrom/rdfs:subClassOf* ?o]
        ?o rdfs:label 'phenol' .
        ?v rdfs:label 'has structural derivative'
    }
    """))
print(f'\t\tDoes not work. prints the empty list: {[item[0].name for item in query]}')


print('Switching o and v')
query = list(default_world.sparql("""
    SELECT ?s
    {
        ?s rdfs:subClassOf [owl:onProperty ?v; owl:someValuesFrom/rdfs:subClassOf* ?o]
        ?o rdfs:label 'is structural derivative of'  .
        ?v rdfs:label 'phenol'
    }
    """))
print(f'\t\tTHIS does not work. Prints the empty list. {[item[0].name for item in query]}')


# About the variable names:
# I worked through these in reverse alphabetical order

# c = list(default_world.sparql("""
# SELECT ?s WHERE { is_structural_derivative_of ?v "phenol" }"""))
# print(c)
# doesn't work

# d = list(default_world.sparql("""
# SELECT ?s WHERE { ?s is_structural_derivative_of "phenol" }"""))
# print(d)
# doesn't work

# e = list(default_world.sparql("""
# SELECT ?s WHERE { ?s ?v "phenol" }"""))
# print(e)
# prints [[structural_derivatives_benzene_v3.phenol]]

# f = list(default_world.sparql("""
# SELECT ?v WHERE { ?s ?v ?o }"""))
# print(f)
 #prints a list of numbers and [rdf-schema. ...]

# g = list(default_world.sparql("""
# SELECT ?y
# { ?x rdfs:label "phenol" .
# ?y subClassOf:is_structural_derivative_of* ?x }
# """))
# print(g)
# trying to obtain the structural derivatives of phenol
# doesn't work

# h = list(default_world.sparql("""
# SELECT ?y
# { ?x rdfs:label "phenol" .
# ?y rdfs:is_structural_derivative_of* ?x }
# """))
# print(h)
# trying to obtain the structural derivatives of phenol
# doesn't work


# i = list(default_world.sparql("""
# SELECT ?y
# { ?x rdfs:label "phenol" .
# ?y rdfs:subClassOf* ?x }
# """))
# print(i)
# prints subclasses of phenol as expected


# j = list(default_world.sparql("""
# SELECT ?x
# { ?x rdfs:label "chemical compound" . }
# """))
# print(j)
# prints chemical compound

# k = list(default_world.sparql("""
# SELECT ?x
# { ?x a owl:Class . }
# """))
# print(k)
# prints all classes in the ontology but not object properties


# l = list(default_world.sparql("""
# SELECT (?x AS ?nb)
# { ?x a continuant . }
# """))
#
# print(l)
# doesn't work

# m = list(default_world.sparql("""
# SELECT (?x AS ?nb)
# { ?x a owl:Thing . }
# """))
#
# print(m)
# prints empty list

# n = list(default_world.sparql("""
# SELECT (?x AS ?nb)
# { ?x a owl:topObjectProperty . }
# """))
#
# print(n)
# doesn't work


# o = list(default_world.sparql("""
# SELECT (?x AS ?nb)
# { ?x a owl:Class . }
# """))
#
# print(o)
# prints all the classes in the ontology but not object properties

# p = onto.query(
# """ ?v
#     WHERE {
#       ?s ?v ?o .)
#    }""")
#
# print(p)
# doesn't work


# q = list(default_world.sparql("""
#            {  ?s ?v ?o .  }
#     """))
#
# print(q)
# doesn't work


# r = list(default_world.sparql("""
#            SELECT ?x
#            {  ?x is_structural_derivative_of "some phenol". }
#     """))
#
# print(r)
# doesn't work
## YOU MISUNDERSTAND HOW TO USE THE PROPERTY RESTRICTION SOME IN SPARQL. SEE MY WORKING EXAMPLE

# s = list(default_world.sparql("""
#            SELECT ?x
#            {  phenol is_structural_derivative_of "some ?x". }
#     """))
#
# print(s)
# doesn't work
