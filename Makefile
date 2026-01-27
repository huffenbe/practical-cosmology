all : practical-cosmology.pdf #Huffenberger-measuring_distance.pdf

practical-cosmology.pdf : practical-cosmology.tex chapters/*.tex *.bib figs/*/*.pdf
	lualatex -interaction=nonstopmode -halt-on-error  $<
	makeindex $(shell basename $< .tex)
	bibtex $(shell basename $< .tex)
	lualatex -interaction=nonstopmode -halt-on-error  $<
	lualatex -interaction=nonstopmode -halt-on-error  $<


Huffenberger-measuring_distance.pdf : practical-cosmology.pdf
	qpdf --empty --pages $< 52-56 -- $@
