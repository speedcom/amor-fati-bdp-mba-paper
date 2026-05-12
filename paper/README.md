# MBA Paper LaTeX Draft

This folder follows the structure used by the local `paper-*` projects:

```text
paper/
├── Makefile
├── README.md
├── analysis/
│   └── figures_bdp_sweep.py
└── latex/
    ├── data/
    ├── esej_mba.tex
    ├── figures/
    ├── references.bib
    ├── sections/
    └── tables/
```

Build from `paper/`:

```sh
make paper
```

This first regenerates the BDP sweep figures from `../mc/` and then uses `xelatex + bibtex`, matching the existing `paper-*` projects and avoiding the local broken `biber` binary.

If needed, override the Python interpreter:

```sh
make paper PYTHON=/path/to/python-with-matplotlib
```

The PDF is written to `latex/esej_mba.pdf`.

The current project checklist is tracked in `../paper-project-plan.md`. The LaTeX files in this directory are the source of the current PDF draft.
