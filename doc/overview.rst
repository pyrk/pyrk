Overview
=========

Time-dependent fluctuations in neutron population, fluid flow, and heat transfer are
essential to understanding the performance and safety of a reactor. Such
*transients* include normal reactor startup and shutdown as well as abnormal scenarios
including Beyond Design Basis Events (BDBEs) such as Accident Transients
Without Scram (ATWS). However, no open source tool currently exists for
reactor transient analysis. To fill this gap, PyRK (Python for Reactor
Kinetics) was created. PyRK is the first open source tool capable of:

- time-dependent,
- lumped parameter thermal-hydraulics,
- coupled with neutron kinetics,
- in 0-dimensions,
- for nuclear reactor analysis,
- of any reactor design,
- in an object-oriented context.


The PRKE
---------

The point reactor kinetics equations are implemented.

Lumped Parameter TH
-------------------

TH is represented in 1-D

Material Library
------------------

A number of materials are represented. Additional materials are a key area
where user/developer contributions are desired.

Data Library
------------

Precursor and decay heat data from the ANS/ANSI standards and representative of
reactor neutronics for canonical reactors has been provided.

The Future
-----------

Our target audience is anyone interested in conducting analyses of nuclear
reactor safety. In the short term, we hope that users will add material
classes, contribute data, find bugs, contribute fixes, and share their ideas
for the future of PyRK.

In the long term, it is very likely that PyRK will one day be absorbed into or
will absorb the wonderful `PyNE` package.


.. PyNE:: http://pyne.github.io

.. warning::

    PyRK is a relatively new project and is still under heavy development.
    Although we will make a best effort to maintain compatibility with the
    current API, inevitably the API will change in future versions as PyRK
    matures.
