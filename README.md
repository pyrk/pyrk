# PyRK

Welcome to PyRK. This is a solver tool for coupled neutronic and thermal
hydraulic reactor transient analysis in 0-D. It is in active development.
Please correspond directly with the author for suggestions about use,
additional documentation, etc.

## Installation

Detailed instructions will be present in the upcoming user's guide. However,
for now, install this as you would any other pure python module

    python setup.py install

If you use --prefix, be sure to add the path to your PYTHONPATH environment
variable.

## Documentation

The documentation for pyrk can be found at 
[pyrk.github.io](pyrk.github.io). Additionally, the entire contents of that 
website can be built from the doc directory in the source code using the 
following steps

#. `pip install sphinx` 
#. `pip install sphinx_rtd_theme`.
#. `sphinx-apidoc --separate --force --output-dir=src/ ../pyrk`
#. `make clean`
#. `make html`

After these steps, the website will be found in `pyrk/doc/_build/html`.

## License

The license for this work can be found
[here](https://github.com/katyhuff/pyrk/blob/master/licenses/LICENSE). Please
be respectful of my intellectual work by communicating with me about its use,
understanding its limitations, and citing me where appropriate. I would be
thrilled to work with you on improving it.


## Contribution

This repository is a work in progress. I would love it if you wanted to
contribute to this code here in this repository. [Here is some information about
how to do that.](https://github.com/katyhuff/pyrk/blob/master/CONTRIBUTING.md).

## Other

- You will find the current state of the test suite on our [Travis continuous
integration servers](https://travis-ci.org/katyhuff/pyrk).

