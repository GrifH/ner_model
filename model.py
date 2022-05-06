from __future__ import unicode_literals, print_function

import random
from pathlib import Path
import spacy
from tqdm import tqdm
from spacy.training.example import Example
import pickle

from annotations import training
from annotations import testing

abstracts = training

model = 'en_ner_bionlp13cg_m'
output_dir=Path("output/")
n_iter=100

#load the model

if model is not None:
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('en')
    print("Created blank 'en' model")

if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe('ner', last=True)
else:
    ner = nlp.get_pipe('ner')

for _, annotations in abstracts:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])
example = []
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
print(other_pipes)
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(abstracts)
        losses = {}
        for text, annotations in tqdm(abstracts):
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update(
                [example],
                drop=0.5,
                sgd=optimizer,
                losses=losses)
        print(losses)
if output_dir is not None:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)
pickle.dump(nlp, open( "education nlp.pkl", "wb" ))

for temp in testing:
    print(temp[0])
    print("-----")
    print(temp[1])
    print("-----")

    doc=nlp(temp[0])
    for ent in doc.ents:
        print(ent.label_+ '  ------>   ' + ent.text)
    print()
    print("-----")
    print()
