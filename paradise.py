#! /usr/bin/env python3

import spacy
from spacy import displacy
import requests, re
from pathlib import Path
from random import sample

def string_insert(source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]

def create_svg(sentence, filename):
    svg = displacy.render(sentence, style='dep', options=options)
    output_path = Path(filename)
    output_path.open('w', encoding='utf-8').write(svg)

def create_annotated_text(sentence, sentence_str):
    offset = 0
    for token in sentence:
        if token.pos_ == "NOUN":
            idx = token.idx - sentence.start_char
            note_idx = idx + len(token.text) + offset
            url = 'http://api.conceptnet.io/c/en/{}'.format(token.text.lower().strip('.,:;"-!?'))
            obj = requests.get(url).json()
            note = create_note(obj, token.text, token.idx)
            if note:
            	sentence_str = string_insert(sentence_str, note, note_idx)
            	offset += len(note)
    sentence_str = sentence_str.replace("\n", "\n\n")
    return sentence_str

def create_note(obj, word, idx):
    note = []
    note.append("*{}*:".format(word))
    if len(obj['edges']) > 0:
        # try:
        #     edges = sample(obj['edges'], 7)
        # except ValueError:
        edges = obj['edges']
        for e in edges:
            if e['surfaceText'] and "translation" not in e['surfaceText']:
                print(e['rel']['label'])
                note_sentence = re.sub(r"\[|\]|\*", "", e['surfaceText'])
                note_sentence = "{}.".format(note_sentence.capitalize())
                note.append(note_sentence)
        label = "{}-{}".format(word, idx)
        if len(note) > 1:
            note = "^[*\lineref{{{}}}*. {}]\linelabel{{{}}} ".format(label," ".join(note),label)
            print(note)
            return note

if __name__ == '__main__':

    nlp = spacy.load('en')

    with open('paradiselost.txt', 'r') as pl:
        text = pl.read()
    nlp.add_pipe(nlp.create_pipe('sentencizer'), before='parser')
    doc = nlp(text[:10000])
    sentence_spans = list(doc.sents)
    options= {'compact': True, 'collapse_punct': True }#, 'distance': 50 }
    #displacy.serve(sentence_spans, style='dep', options=options)
    full_md = ""
    for s_idx, sentence in enumerate(sentence_spans):

        filename = "img/sentence{}.png".format(s_idx)
        # create_svg(sentence, filename)
        sentence_str = sentence.text
        sentence_str = create_annotated_text(sentence, sentence_str)
        full_md += "{}\n\n![]({})\n\n".format(sentence_str, filename)

    with open('test.md', 'w') as newfile:
        newfile.write(full_md)
