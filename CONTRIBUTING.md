### Thanks for Your Help!

Contributing is so kind of you. In pyrk, all contributions, bug reports, bug
fixes, documentation improvements, enhancements and ideas are welcome.

The [GitHub "issues" tab](https://github.com/pyrk/pyrk/issues)
contains some issues labeled "first PR". Those are open issues that would be a
good quick way to get started. Browse them to see if you want to get started on
one.

#### Bug Reports

  - Please include a short but detailed, self-contained Python snippet or
    explanation for reproducing the problem.

  - Explain what the expected behavior was, and what you saw instead.

##### Instructions for setting up a development environment

The pyrk project aims to to be compatible between Python 2.7 and 3.x, so it
is important to test in both platforms before submitting a pull request.
Anaconda is the recommended distribution to use to work on pyrk; we will
assume that if you want to use another distribution or your own set up,
you can translate the instructions.

You can download Anaconda at https://www.continuum.io/Downloads for the full
install. You can also download a mini Anaconda install for a bare-bones
install -- this is good for a build server or if you don't have much space.
The mini Anaconda installs are available at https://conda.io/miniconda.html.

Once your Anaconda package is installed and available, create a Python 2.7
and 3.6 environment in Anaconda --

 - conda create -q -n pyrk-27-test-environment python=2.7 scipy numpy matplotlib nose pytables
 - conda create -q -n pyrk-36-test-environment python=3.6 scipy numpy matplotlib nose pytables

Each of these commands will take a bit of time -- give it a few minutes
to download and install the packages and their dependences. Once complete,
switch to each and install additional packages needed to run and test.

Activate the 2.7 environment and install nose and pint

 - source activate pyrk-27-test-environment
 - pip install nose pint

Activate the 3.6 environment and install nose and pint

 - source activate pyrk-27-test-environment
 - pip install nose pint

##### Run the tests

Tests are automatically detected and run with nose. To run them, use
the nosetests script that was made available when nose was installed
and add the pyrk code into the PYTHONPATH variable so that the tests
can find the implementation code.

Start in the root directory where you have cloned the pyrk repository
and run for Python 2.7 --

 - source active pyrk-27-test-environment
 - cd pyrk
 - PYTHONPATH=$PWD nosetests

And then for Python 3.6 --

 - source activate pyrk-36-test-environment
 - cd pyrk
 - PYTHONPATH=$PWD nosetests

##### Pull Requests

  - **Make sure the test suite passes** on your computer. To do so, run `nosetests` in the tests directory.
  - Please reference relevant Github issues in your commit message using `GH1234`
    or `#1234`.
  - Changes should be PEP8 compatible [PEP8](http://www.python.org/dev/peps/pep-0008/).
  - Keep style fixes to a separate commit to make your PR more readable.
  - Docstrings ideally follow the [sphinx autodoc](https://pythonhosted.org/an_example_pypi_project/sphinx.html#function-definitions)
  - Write tests.
  - When writing tests, please make sure they are in a `test` directory.
  - When you start working on a PR, start by creating a new branch pointing at the latest
    commit on github master.
  - Please avoid rebasing if possible. Nothing wrong with rebase... it is just confusing for @katyhuff .
  - The pyrk copyright policy is detailed in the pyrk [LICENSE](https://github.com/pyrk/pyrk/blob/master/LICENSE).

#### More developer docs

* We are working on it.


#### Meta
Note, this contributing file was adapted from the one at the
[pandas](https://github.com/pydata/pandas) repo. Thanks pandas!
