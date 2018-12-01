#! /usr/bin/env python3

import spacy
from spacy import displacy
import requests, re
from pathlib import Path
from random import sample

def string_insert(source_str, insert_str, pos):
    """
    Insert a new string into a specific position in the original string.
    Used for adding markdown notes to the poems.
    """
    return source_str[:pos]+insert_str+source_str[pos:]

def tokenize_books(text):
    """
    Given the full Paradise Lost text, tokenize by book using a simple regex.
    """
    booksplit = r"^Book.*"
    books = re.split(booksplit, text, flags=re.MULTILINE)
    books = books[1:]
    return books

def create_svg(sentence, filename):
    """
    Create an SVG of spacy's dependency parse diagram and write it to file.
    """
    svg = displacy.render(sentence, style='dep', options=options)
    full_filename = "{}.svg".format(filename)
    output_path = Path(full_filename)
    output_path.open('w', encoding='utf-8').write(svg)

def create_annotated_text(sentence, sentence_str):
    """
    Given a sentence of Paradise Lost, create a full set of annotations for that
    sentence and output the resulting string with markdown footnotes.
    """
    offset = 0 #Keep track of token offset to place notes accurately
    dependency = []
    for token in sentence:
        dependency.append(token.dep_)
        if token.pos_ == "NOUN":
            idx = token.idx - sentence.start_char #Token's position from start of sentence
            note_idx = idx + len(token.text) + offset #Where the note should go, with care toward the length of the previous note

            #Make API call to ConceptNet for note contents
            url = 'http://api.conceptnet.io/c/en/{}'.format(token.text.lower().strip('.,:;"-!?'))
            obj = requests.get(url).json()
            note = create_note(obj, token.text, token.idx) #Try to create a note
            if note:
            	sentence_str = string_insert(sentence_str, note, note_idx) #If a note exists, insert it into the sentence.
            	offset += len(note) #Increase offset
    sentence_str = create_dependency_note(sentence, sentence_str, dependency) #Add dependency note after first word
    sentence_str = sentence_str.replace("\n", "\n\n") #Add additional linebreaks for markdown parsing
    return sentence_str

def create_note(obj, word, idx):
    """
    Given the result of a ConceptNet request, a token, and its index, produce a note to be attached to that word.
    """
    note = []
    note.append("*{}*:".format(word)) #The first part of the note should be the markdown italicized word itself.
    if len(obj['edges']) > 0: #If the ConceptNet result has any word relationships.
        edges = obj['edges']
        for e in edges:
            # In each relationship, pull out the text on which that relationship is based (always a complete sentence).
            if e['surfaceText'] and "translation" not in e['surfaceText']: #Don't include the translation relationship sentences.
                print(e['rel']['label'])
                # Clean up the text and reformat it as a normal sentence.
                note_sentence = re.sub(r"\[|\]|\*", "", e['surfaceText'])
                note_sentence = "{}.".format(note_sentence.capitalize())
                note.append(note_sentence)
        label = "{}-{}".format(word, idx) #Create line label for latex
        if len(note) > 1: #Don't include empty notes
            note = "^[*\lineref{{{}}}*. {}]\linelabel{{{}}} ".format(label," ".join(note),label) #Create full markdown text of the note, with latex linerefs
            print(note)
            return note

def create_dependency_note(sentence, sentence_str, dependency):
    """
    Given a sentence and a list of dependency parse tokens, return a string
    that includes a footnote of the dependency parse after the first token in
    the sentence.
    """
    dependency = "*Sentence Parse: {}*".format("--".join(dependency)) #Turn list of dependency labels into a string.
    label = "{}-{}".format(sentence[0].idx, sentence[0].idx) #Create the line label for latex
    dep_note = "^[*\lineref{{{}}}*. {}]\linelabel{{{}}} ".format(label,dependency,label) #Assemble the full markdown note, with latex linerefs
    first_idx = sentence[0].idx - sentence.start_char #Get position of the first token in the sentence
    first_position = first_idx + len(sentence[0].text) #Find the end of that token, where the note will go
    sentence_str = string_insert(sentence_str,dep_note,first_position) #Insert note into sentence string
    return sentence_str

if __name__ == '__main__':

    nlp = spacy.load('en') # Load spacy language model

    # Read full text of Paradise Lost
    with open('paradiselost.txt', 'r') as pl:
        text = pl.read()

    # Use punctuation-based sentence tokenizer instead of default dependency-based tokenizer
    nlp.add_pipe(nlp.create_pipe('sentencizer'), before='parser')
    books = tokenize_books(text)

    # Run spacy on Book 1
    doc = nlp(books[0])

    # Get all sentences as a list
    sentence_spans = list(doc.sents)

    # Options and testing for dependency parse trees
    #options= {'compact': True, 'collapse_punct': True }#, 'distance': 50 }
    #displacy.serve(sentence_spans, style='dep', options=options)


    full_md = ""
    for s_idx, sentence in enumerate(sentence_spans):

        # This is where I'd create the SVG image, but I decided to not go in that direction.
        #filename = "img/sentence{}".format(s_idx)
#       create_svg(sentence, filename)

        # Get plaintext of each sentence
        sentence_str = sentence.text

        # Annotate each sentence and return strings
        sentence_str = create_annotated_text(sentence, sentence_str)

        #full_md += "![]({}.png)\n\n{}\n\n\\newpage\n\n".format(filename, sentence_str) #What the full sentence string would look like if I used the SVG image.

        #Add every sentence to full markdown string
        full_md += "Sentence {}: {}\n\n\\newpage\n\n".format(s_idx+1, sentence_str)

    # Write markdown file for conversion to PDF
    with open('book1.md', 'w') as newfile:
        newfile.write(full_md)
