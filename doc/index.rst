.. pyrk documentation master file, created by
   sphinx-quickstart on Mon Mar  2 16:38:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


PyRK
====

.. image:: images/logo.png
   :width: 25 %
   :alt: PyRK logo


**PyRK** is a python package for nuclear reactor kinetics. It uses a point
reactor kinetics model and provides an object oriented simulation environment
intended for transient simulations for reactors. It should perk you right up,
like a good cup of coffee.

**PyRK** welcomes your contributions. It already relies on many libraries in
the Scientific Python ecosystem including `numpy`_, `scipy`_, `pint`_, and
`matplotlib`_.

.. _numpy: http://numpy.org
.. _scipy: http://scipy.org
.. _pint: http://pint.readthedocs.org
.. _matplotlib: http://matplotlib.org


Documentation
-------------

.. toctree::
   :maxdepth: 1

   overview
   examples
   installing
   tutorial
   src/index

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _GitHub project site: https://github.com/pyrk

.. _github: https://github.com/pyrk/pyrk

Citation
--------

Up-to-date information about citing PyRK can be found within the `citation`_ 
file.

.. _citation: https://github.com/pyrk/pyrk/blob/master/CITATION.md

See also
--------

- Katy Huff's `SciPy2015 talk`_ introducing PyRK to an interdisciplinary audience.
- The associated `Scipy2015 slides`_
- The associated short `SciPy2015 paper`_ from the conference describing the software structure.
- Xin Wang's `ICAPP paper` using PyRK for PBFHR analysis.

.. _SciPy2015 talk: https://www.youtube.com/watch?v=2HToG61wMWI
.. _SciPy2015 slides: http://pyrk.github.io/scipy-2015
.. _SciPy2015 paper: http://conference.scipy.org/proceedings/scipy2015/kathryn_huff.html
.. _ICAPP paper: http://icapp.ans.org

Get in touch
------------

- Please report bugs, suggest feature ideas, and browse the source code `on GitHub`_.
- There, new contributors can also find `a guide to contributing`_.
- You can also contact Katy `on Twitter`_.

.. _on GitHub: http://github.com/pyrk/pyrk
.. _a guide to contributing: https://github.com/pyrk/pyrk/blob/master/CONTRIBUTING.md
.. _on Twitter: http://twitter.com/katyhuff

License
-------

PyRK is available under the open source `BSD 3-clause License`__.

__ https://raw.githubusercontent.com/pyrk/pyrk/master/licenses/LICENSE

History
-------

PyRK was originally developed for analysis of accident transients in the
Pebble-Bed, Fluoride-Salt-Cooled, High-Temperature Reactor (`PB-FHR`_) design. It was
originally written by Kathryn Huff who is supported by the Nuclear Science and
Security Consortium (`NSSC`_) as well as the `FHR Project`_ and the Berkeley
Institute for Data Science (`BIDS`_) at Berkeley.  Colleagues that contributed
feedback in this endeavor include Xin Wang, Per Peterson, Ehud Greenspan, and
Massimiliano Fratoni at the University of California Berkeley.

.. _PB-FHR: http://fhr.nuc.berkeley.edu/pb-fhr-technology/
.. _NSSC: http://nssc.berkeley.edu/
.. _FHR Project: http://fhr.nuc.berkeley.edu/
.. _BIDS: http://bids.berkeley.edu/

