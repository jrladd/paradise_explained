# Paradise Explained, Meaning Lost

## *A Nonsensically Annotated Edition of Milton's Epic*

Annotated editions of complex poetic works often try to decode the poem for the reader. But what if the annotations only caused more confusion?

Beginning with Milton's syntactical complexity as a first premise, this project builds an edition of *Paradise Lost* split up according to the poem's dazzlingly complicated sentences. The first footnote for each sentence uses spaCy's [dependency parsing](https://spacy.io/usage/linguistic-features#section-dependency-parse) to create a string of dependency tags that describe the sentence without explaining it.

Description without explanation is the theme of all the following notes, which identify terms in *Paradise Lost* and attempt to explain those terms using sentences from [ConceptNet](http://conceptnet.io/).

What results is an edition of the poem that in appearance mimics the [thorough scholarly edition](https://books.google.com/books?id=q1cSBAAAQBAJ&source=gbs_similarbooks) published by Longman and edited by Alistair Fowler. But where that edition provides background and explanation, this edition suggests explanatory annotation while only further occluding and complicating the poem.

As a sample here (and to save my computer from memory issues), I've only processed Book 1, but the resulting text is well over 90,000 words.

## How to Run

Simply running the `paradise.py` script will generate a markdown file for Book 1. Then use the command `make pdf` to convert the markdown into a readable PDF. I've customized a LaTeX template to make the book appear as close to the Longman *Paradise Lost* as possible.

This project requires [spaCy](https://spacy.io/) (for natural language processing), as well as [LaTeX](https://www.latex-project.org/) and [pandoc](https://pandoc.org/) (for generating the PDF). It also makes use of the [ConceptNet API](https://github.com/commonsense/conceptnet5/wiki/API).

I original intended to use spaCy's [dependency parse visualizations](https://spacy.io/usage/visualizers#section-dep) instead of footnotes for the dependency parsing portion. The idea was to display the massive entangled diagram as another attempt to explain the poem that ends in incoherence. Unfortunately the diagrams wound up *so* massive that they were both nearly unreadable and difficult to process at scale. I left the code commented-out in the script so that you can see how I would have done it.

## Credits

I was inspired by a variety of projects from both the recent and the distant past. The sometimes nonsensical annotations that the mysterious "E.K." provided for Spenser's *The Shepheardes Calendar* were a starting point for my thinking about annotation in general. The great Allison Parrish's [2014 NaNoGenMo project, *I Waded In Clear Water*](https://github.com/aparrish/nanogenmo2014), was a huge inspiration for her ConceptNet/WordNet footnote approach (but I intentionally did not look at her code when working on my scripts). Finally Dan Shore's recent book [*Cyberformalism*](https://jhupbooks.press.jhu.edu/content/cyberformalism) got me thinking about the importance of Milton's sentence structure and led to my interest in using dependency parsing in this project.

A final thanks to Steve Pentecost for letting me bend his ear about the project and lending help with the LaTeX templates. [His own NaNoGenMo project](https://github.com/spenteco/nanogenmo2018) is worth a look.
