PyRK Tutorial
=============

Creating an Input File
------------------

To create an input file, the user can use a default example as a good starting
template. Each simulation object requires several parameters to run:

- A timer for each simulation must be created. The user can define a start/end
times as well as a time-step value. The timer is its own module with more
details present in its file.

- Thermal components of the reactor can be created and linked together through
convection, conduction, etc. The thermal hydraulics model is its own module
with more details present in its file(s).

- The isotopes within the fuel, as well as the energy spectrum of the reactor
should be specified. Precursor and decay groups, as well as ficticious neutron
groups (if multi-point kinetics is used) should also be specified.

- External reactivity insertions and feedback coefficients can also be included
if feedback and reactivity insertions are modeled. External reactivity
insertions are modeled in their own module, with more details in its file.

Running an Input
-----------------

A simulation can be run by using the command below. The infile is the path
to the input file, and plotdir is the path to the output folder location.


.. code-block:: bash

   python /path/to/pyrk/driver.py --infile=input --plotdir=output 


In the example above, path/to/pyrk is, of course, the path to the pyrk 
directory, containing driver.py.

Reading Output
---------------

After the simulation is complete, multiple output files are created within
the specified output folder (the default name is "images" in the main PyRK
directory).

These output files include:

- Temperature plots for each modeled thermal component
- Average power plots (normalized to initial power)
- Reactivity plots
- Zetas plots (precursor concentrations)

PyRK also provides an h5 database file containing solutions for each timestep.
