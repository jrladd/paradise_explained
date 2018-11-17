#! /usr/bin/env python3

import spacy
from spacy import displacy
import requests, re
from pathlib import Path
# from random import sample

def string_insert(source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]
    
nlp = spacy.load('en')

with open('paradiselost.txt', 'r') as pl:
    text = pl.read()
nlp.add_pipe(nlp.create_pipe('sentencizer'), before='parser')
doc = nlp(text[:10000])
sentence_spans = list(doc.sents)
options= {'compact': True, 'collapse_punct': True }#, 'distance': 50 }
#displacy.serve(sentence_spans, style='dep', options=options)
full_md = ""
for s_idx, s in enumerate(sentence_spans):
    # svg = displacy.render(s, style='dep', options=options)
    filename = "img/sentence{}.svg".format(s_idx)
    # output_path = Path(filename)
    # output_path.open('w', encoding='utf-8').write(svg)
    full_sentence = s.text
    offset = 0
    for token in s:
        if token.pos_ == "NOUN":#or token.pos_ == "PROPN":
            # print(token.text)
            idx = token.idx - s.start_char
            print(idx)
            note_idx = idx + len(token.text) + offset
            url = 'http://api.conceptnet.io/c/en/{}'.format(token.text.lower().strip('.,:;"-!?'))
            # print(url)
            obj = requests.get(url).json()
            note = []
            if len(obj['edges']) > 0:
                # edges = sample(obj['edges'], 2)
                for e in obj['edges']:
                    if e['surfaceText']:
                        sentence = re.sub(r"\[|\]|\*", "", e['surfaceText'])
                        sentence = "{}.".format(sentence.capitalize())
                        note.append(sentence)
            note = "^[{}]".format(" ".join(note))
            full_sentence = string_insert(full_sentence, note, note_idx)
            offset += len(note)
    full_sentence = full_sentence.replace("\n", "\n\n")
    full_md += "{}\n\n![]({})\n\n".format(full_sentence, filename)
    # print()
    #print(html)
# with open('dependency.html', 'w') as newfile:
#     newfile.write(html)
with open('test.md', 'w') as newfile:
    newfile.write(full_md)