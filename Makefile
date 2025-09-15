practical-cosmology.pdf : practical-cosmology.tex chapters/*.tex
	pdflatex -interaction=nonstopmode -halt-on-error  $<
	pdflatex -interaction=nonstopmode -halt-on-error  $<
	pdflatex -interaction=nonstopmode -halt-on-error  $<
