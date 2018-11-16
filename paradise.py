#! /usr/bin/env python3

import spacy
from spacy import displacy
import requests
from random import sample

nlp = spacy.load('en')
#text = u"""In ancient Rome, some neighbors live in three adjacent houses. In the center is the house of Senex, who lives there with wife Domina, son Hero, and several slaves, including head slave Hysterium and the musical's main character Pseudolus. A slave belonging to Hero, Pseudolus wishes to buy, win, or steal his freedom. One of the neighboring houses is owned by Marcus Lycus, who is a buyer and seller of beautiful women; the other belongs to the ancient Erronius, who is abroad searching for his long-lost children (stolen in infancy by pirates). One day, Senex and Domina go on a trip and leave Pseudolus in charge of Hero. Hero confides in Pseudolus that he is in love with the lovely Philia, one of the courtesans in the House of Lycus (albeit still a virgin)."""

with open('paradiselost.txt', 'r') as pl:
    text = pl.read()
nlp.add_pipe(nlp.create_pipe('sentencizer'), before='parser')
doc = nlp(text[:10000])
sentence_spans = list(doc.sents)
options= {'compact': True, 'collapse_punct': True }#, 'distance': 50 }
#displacy.serve(sentence_spans, style='dep', options=options)
for s in sentence_spans:
    #html = displacy.render(s, style='dep', options=options)
    print(s)
    for token in s:
        if token.pos_ == "NOUN":#or token.pos_ == "PROPN":
            print(token.text)
            url = 'http://api.conceptnet.io/c/en/{}'.format(token.text.lower().strip('.,:;"-!?'))
            print(url)
            obj = requests.get(url).json()
            if len(obj['edges']) > 2:
                edges = sample(obj['edges'], 2)
                for e in edges:
                    print(e['surfaceText'])
    print()
    #print(html)
# with open('dependency.html', 'w') as newfile:
#     newfile.write(html)
