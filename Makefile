practical-cosmology.pdf : practical-cosmology.tex chapters/*.tex *.bib
	pdflatex -interaction=nonstopmode -halt-on-error  $<
	makeindex $(shell basename $< .tex)
	bibtex $(shell basename $< .tex)
	pdflatex -interaction=nonstopmode -halt-on-error  $<
	pdflatex -interaction=nonstopmode -halt-on-error  $<
