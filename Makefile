filename := test

pdf : $(filename).md
	pandoc -s -S $(filename).md -o $(filename).pdf --template booktemplate.latex -V documentclass=book -V linestretch=1 -V indent=true -V fontsize=16pt
	pdfnup $(filename).pdf --nup 2x1 --outfile $(filename)_2up.pdf