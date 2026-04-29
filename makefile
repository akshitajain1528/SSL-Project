# Makefile for GameCraft CS108 SSL Project Report

MAIN     = report
LATEX    = pdflatex
LATEXOPT = -interaction=nonstopmode -halt-on-error
BUILDDIR = build

.PHONY: all clean distclean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex figures/start_screen.png figures/tictactoe.png \
             figures/league.png figures/statistics.png figures/leaderboard.png
	@mkdir -p $(BUILDDIR)
	$(LATEX) $(LATEXOPT) -output-directory=$(BUILDDIR) $(MAIN).tex
	$(LATEX) $(LATEXOPT) -output-directory=$(BUILDDIR) $(MAIN).tex
	@cp $(BUILDDIR)/$(MAIN).pdf .
	@echo "Build complete: $(MAIN).pdf"

clean:
	@rm -rf $(BUILDDIR)
	@echo "Cleaned build artifacts."

distclean: clean
	@rm -f $(MAIN).pdf
	@echo "Removed output PDF."
