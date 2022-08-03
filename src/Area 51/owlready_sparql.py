# we can already do a lot with just owlready2
# see these pages for documentation
# https://owlready2.readthedocs.io/en/latest/onto.html
# https://owlready2.readthedocs.io/en/latest/class.html

from owlready2 import *

# onto = get_ontology("http://www.semanticweb.org/stefan/ontologies/2022/6/untitled-ontology-9").load()
# doesn't work

onto = get_ontology("file:///Users/Stefan/Desktop/_Chary_lab_research/Protege/structural_derivatives_benzene_v3.owl").load()
# gets the ontology in the specified location and file

# print(onto.phenol.is_structural_derivative_of)
# prints benzene. Does not print the inherited chemical_compound,
# which is what we want

# print(list(onto.properties()))
# prints a list of properties in the ontology

# print(list(onto.phenol.subclasses()))
# prints subclasses of phenol, dinitrophenol and trinitrophenol

# print(list(onto.phenol.is_a))
# prints
# benzene, is_structural_derivative_of.some(benzene),
# has_part.min(1, hydroxyl_group)
# but doesn't print chemical_compound

# print(list(onto.phenol.ancestors()))
# prints benzene, chemical_compound, owl.Thing, phenol, continuant

# print(onto.phenol.INDIRECT_is_structural_derivative_of)
# prints chemical_compound, benzene, which is what we want
# shows that there is inheritance of is_strucural_derivative_of
# I think this is what it captures in SparQL:
# phenol is_structural_derivative_of some ?x

# print(onto.phenol.INDIRECT_has_structural_derivative)
# prints nothing
# although has_structural_derivative is the inverse of
# is_structural_derivative_of, it is not declared explicitly

# print(onto.phenol.get_properties())
# doesn't work


# ====== Moving on to querying the ontology using sparql ======

# About the variable names:
# I worked through these in reverse alphabetical order

# print(list(default_world.sparql("""
# SELECT (COUNT(?x) AS ?nb)
# { ?x a owl:Class . }
# """)))
# prints 19


# count_of_classes = list(default_world.sparql("""
#                SELECT (COUNT(DISTINCT ?x) AS ?nb)
#                { ?x a owl:Class.}
#         """))[0][0]

# print(count_of_classes)
# prints 19

# Syntactic features:
# 1. only the default_world.sparql function understands SPARQL strings. default_world
#  is a base class loaded with the command "from owlready2 import *".
# 2. triple quotes surround the SPARQL query. Triple quotes enclose multi-line strings.
# 3. curly braces surround the actual query.
# 4. the final (in this case only) line of the actual query is terminate by a period
# 5.  It's nested because the best practice for queries is to return a generators
#  rather than a list to minimize memory usage.


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

# s = list(default_world.sparql("""
#            SELECT ?x
#            {  phenol is_structural_derivative_of "some ?x". }
#     """))
#
# print(s)
# doesn't work
