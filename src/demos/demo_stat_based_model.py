import json, spacy, os, random, warnings
from spacy.training import Example, offsets_to_biluo_tags
from spacy.tokens import Doc
from spacy.vocab import Vocab

warnings.filterwarnings("error")

'''
 Annotated data created with Tecoholoic's NER-Annotator (https://tecoholic.github.io/ner-annotator/).

# 2. Tag the training-data using Techoholic's NER annotator (https://tecoholic.github.io/ner-annotator/)
    # Steps to tagging comments:
     # a. input txt file in annotator
     # b. create "Symptom" and "Substance" Tags 
     # c. tag comments with the tags created
     # d. export as JSON (Each entry contains "entity" and a list of "spans" with "start" and "end" annotations and "label" of annotated entities with respective tokenization)
        #Example Entry:
            # {"classes": ["SYMPTOM", "SUBSTANCE"],
                # "annotations": "DNP is great I felt hot and had diarrhea",
                    # {"entities": [0,3, "SUBSTANCE"],[20,23,"SYMPTOM"],[32,40,"SYMPTOM"]}
    
'''
training_data = json.load(open(os.path.join('..','data','annotated','annotations-fixeddoublequotes.json')))

#nlp = spacy.blank("en") #for blank
nlp = spacy.load('en_core_web_lg',disable=['ner'])
nlp.remove_pipe("ner")
ner = nlp.create_pipe("ner") 
nlp.add_pipe('ner', last=True)
ner = nlp.get_pipe('ner')

error_counter = 0
# Define blank english pipeline. Introduce annotations to program
for text,entity_dictionary in training_data["annotations"]:
    for entity in entity_dictionary["entities"]:
        try:
            start,stop,label = entity
        except UserWarning as warn:
            error_counter +=1
            #uncomment to print error
            print(spacy.training.offsets_to_biluo_tags(nlp.make_doc(text), [entity]))
        ner.add_label(label)

print(f'Of {len(training_data["annotations"])} docs, {error_counter} threw an error.')
#Of 342 docs, 115 threw an error.
print(len(training_data["annotations"]))
print('bort')
# Add custom entity tags to model
for label in training_data["classes"]:
    nlp.get_pipe("ner").add_label(label)

#optimizer = nlp.initialize() #can use only if start with spacy.blank()
optimizer = nlp.create_optimizer()

nreps = 10
for _ in range(nreps):
  text_annotations = training_data["annotations"]
  random.shuffle(text_annotations)
  for text, annotations in text_annotations:
    
    if len(text) > 0:

      example = Example.from_dict(nlp.make_doc(text), annotations)
      nlp.update([example])

# 8. Input remaining of data (Demo-data.txt) as text 
text = open(os.path.join('..','data','raw','Demo-data.txt')).read()
doc = nlp(text)

# 10. Print out the "entity" and corresponding "label"
for ent in doc.ents:
      print(ent.text, ent.label_)

outfile = os.path.join('..','data','output','demo-output-stat-with-en-based.txt')
with open(outfile, mode='wt', encoding='utf-8') as myfile:
    myfile.write("Name,Standardized Form,Classification\n")
    for ent in doc.ents:
        myfile.write(f'{ent.text},{ent.lemma_},{ent.label_}\n')

nlp.to_disk(os.path.join('..','models','stat_trained_on_bb_with_en_base'))

'''
Precision 99.51% and recall 64.72% [(Substances: 61.41%),(Symptoms: 68.03%)]
After NREPS 10 => 100, recall increased to 67.18% [(Substances: 56.68%),(Symptoms: 77.68%)]
'''