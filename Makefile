practical-cosmology.pdf : practical-cosmology.tex chapters/*.tex
	pdflatex $< -halt-on-error
	pdflatex $< -halt-on-error
	pdflatex $< -halt-on-error
