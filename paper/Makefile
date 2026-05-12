LATEX_DIR := latex
MAIN      := esej_mba
PYTHON    ?= /Users/mmaciaszek/anaconda3/bin/python3

.PHONY: paper figures clean open

paper: figures
	cd $(LATEX_DIR) && xelatex -interaction=nonstopmode $(MAIN).tex && bibtex $(MAIN) && xelatex -interaction=nonstopmode $(MAIN).tex && xelatex -interaction=nonstopmode $(MAIN).tex

figures:
	$(PYTHON) analysis/figures_bdp_sweep.py
	$(PYTHON) analysis/figures_lambda_robustness.py

clean:
	rm -f $(LATEX_DIR)/*.aux $(LATEX_DIR)/*.bbl $(LATEX_DIR)/*.blg $(LATEX_DIR)/*.log $(LATEX_DIR)/*.out $(LATEX_DIR)/*.run.xml $(LATEX_DIR)/*.toc $(LATEX_DIR)/*.bcf $(LATEX_DIR)/*-blx.bib $(LATEX_DIR)/*.fdb_latexmk $(LATEX_DIR)/*.fls

open:
	open $(LATEX_DIR)/$(MAIN).pdf
