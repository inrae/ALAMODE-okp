Usage
=====

Input data
----------

The model reads input and configuration data from three text files, one
obligatory (``meteo_file``) and two optional (``lake_file`` and ``par_file``).
Field data used for validation may also be read from a text file
(``validation_data_file``). Once you have created the input files, you can use
the ``okplm`` package as a command line application or a Python module.

File ``meteo_file``
^^^^^^^^^^^^^^^^^^^
Obligatory input file. It contains air temperature and solar radiation data.

The file is structured in three columns separated by white spaces:

* date: date in the format 'yyyy-mm-dd'.
* tair: mean daily air temperature (ºC).
* sr: mean daily solar radiation (W m\ :sup:`-2`\ ).

::

    date tair sr
    2015-01-01 -5.3 71.4
    2015-01-02 -4.6 71.5
    2015-01-03 -5.9 72.2
    2015-01-04 -8.5 69.4
    2015-01-05 -9.0 73.1
    ...

Meteorological data may be provided at three different frequencies: daily,
weekly and monthly.

File ``lake_file``
^^^^^^^^^^^^^^^^^^
Optional input file. It contains lake characteristics (depth, surface,
volume, altitude, latitude).

The file is structured in two columns, separated by blanks. The first column
contains the names of the variables and the second one contains their values.
The variable names are:

* name: lake name or code (optional, to identify the lake)
* zmax: lake depth (m)
* surface: lake surface area (m\ :sup:`2`\ )
* volume: lake volume (m\ :sup:`3`\ )
* altitude: altitude above sea level (m)
* latitude: latitude (º)
* type: lake type; it can be 'L' for lakes (surface outlet) or 'R' for
  reservoirs (submerged outlet)

The pairs of names-values may be specified in any order.

For example, for the Lake Allos (ALL04)::

    name ALL04
    altitude 2232
    latitude 44.233
    zmax 51
    surface 528424.501
    volume 9775853.276
    type L


Providing either ``lake_file`` or ``par_file`` is necessary. If the
``par_file`` is given, the program uses parameter values in ``par_file``.
Otherwise, the ``lake_file`` is required and the program calculates the model
parameters from the lake characteristics included in the ``lake_file``.

File ``par_file``
^^^^^^^^^^^^^^^^^
Optional input file. It contains the value of the model parameters.

The file is structured in two columns, separated by blanks. The first column
contains the names of the parameters and the second one contains their values.
The parameter names are:

* A: parameter *A*. It corresponds to the mean annual epilimnion temperature
  (ºC).
* B: parameter *B*. It modulates the effect of air temperature.
* C: parameter *C*. It modulates the effect of solar radiation.
* D: parameter *D*. A constant value of 0.51 by default.
* E: parameter *E*. It is related to the ratio between hypolimnion temperature
  and epilimnion temperature. It is equal to one when the water body is not
  stratified.
* ALPHA: parameter \ :math:`\alpha`\ , exponential smoothing factor of the air
  temperature.
* BETA: parameter \ :math:`\beta`\ , exponential smoothing factor of the
  epilimnion temperature.
* mat: mean annual air temperature (ºC).
* at_factor: multiplicative factor of air temperature.
* sw_factor: multiplicative factor of shortwave radiation.

For example, for the Lake Allos (ALL04)::

    A 6.20
    B 1.007
    C -0.0070
    D 0.51
    E 0.24
    ALPHA 0.07
    BETA 0.13
    mat -0.41
    at_factor 1.0
    sw_factor 1.0

For the definition of the parameters and further information see Prats & Danis
(2019).

If ``par_file`` is not given by the user, the model calculates the parameter
values as a function of the lake characteristics defined in ``lake_file``
according to the parameterisation by Prats & Danis (2019) for French freshwater
bodies. The values of the parameters thus estimated are written to
``par_file``.

The parameters ``at_factor`` and ``sw_factor`` are multiplicative factors of
input meteorological data, that can be useful for sensitivity analyses. By
default they take a value of 1.0.

File ``validation_data_file``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Optional observational data file used for the calculation of performance
indicators.

The file is structured in (at most) three columns separated by white spaces:

* date: date in the format 'yyyy-mm-dd'.
* tepi: epilimnion temperature (ºC) (optional).
* thyp: hypolimnion temperature (ºC) (optional).

::

    date tepi thyp
    2015-01-10 0.0 3.9
    2015-03-08 0.0 4.0
    2015-04-04 2.0 4.0
    2015-06-11 8.5 5.2
    2015-06-12 8.0 5.3
    2015-06-13 9.2 5.4
    2015-08-18 13.7 6.8
    2015-10-23 7.0 4.9
    2015-10-29 1.2 4.0
    2015-12-31 0.2 4.0

The file contains data for the dates for which measurements are available. You
may provide data for only one of tepi or thyp::

    date tepi
    2015-01-10 0.0
    2015-03-08 0.0
    2015-04-04 2.0
    2015-06-11 8.5
    2015-06-12 8.0
    2015-06-13 9.2
    2015-08-18 13.7
    2015-10-23 7.0
    2015-10-29 1.2
    2015-12-31 0.2


Start and end of simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
When calling the function ``run_okp()``, you can specify the dates of start
and end of the simulation by using the arguments ``start_date`` and
``end_date`` (or ``-s`` and ``-e`` in the command line). The format of the
dates is 'yyyy-mm-dd'.

If no start and end date are defined, the length of the simulation is
determined by the length of the ``meteo_file``.

Command line application
------------------------

To run ``okplm`` in the command line, change to the directory containing the
input files and make:

.. code:: shell

    run_okp

Alternatively, you can indicate the input data folder. E.g.:

.. code:: shell

    run_okp -f C:/users/yourself/data/lake_data

Please note that the software understands the tilde '~' expansion, so that you
may use instead:

.. code:: shell

    run_okp -f ~/data/lake_data

By default, the model looks for the files named ``meteo.txt`` (meteorological
data), ``lake.txt`` (lake data) and ``par.txt`` (values of the model parameters).
You can specify other names using the optional arguments ``-m``, ``-l`` and ``-p``,
respectively. E.g.,

.. code:: shell

    run_okp -m meteorology.txt

Similarly, the results are written by default to ``output.txt``, but you can use
define another name using ``-o``.

You can limit the length of the simulation by specifying the start and end
dates:

.. code:: shell

    run_okp -s 2014-01-01 -e 2015-12-31

To tell the model the frequency of the input meteorological data and of the
simulation you may use ``-d`` (daily), ``-w`` (weekly) or ``-n`` (monthly). E.g.

.. code:: shell

    run_okp -w

By default the program assumes the input data is provided at a daily time step.

For daily simulations, the output can be given at daily, weekly of monthly
frequencies with the arguments ``--daily_output``, ``--weekly_output`` and 
``--monthly_output``.

It is also possible to obtain error statistics of the daily simulations by
providing an observation data file (e.g., ``obs.txt``) and the name of the
validation results file (e.g., ``err_stats.txt``):

.. code:: shell

    run_okp -a obs.txt -b err_stats.txt

If these file names are not provided, validation statistics are not calculated.

For obtaining help on the usage of the application, write:

.. code:: shell

    run_okp -h


Python module
-------------

To use ``okplm`` as a Python module you can simply import it and use the
functions within::

    import okplm

To run the model, first define the names of the different input and output
files. For example::

    import os.path
    
    folder = path_to_data_repertory
    output_file = os.path.join(folder, 'output.txt')
    meteo_file = os.path.join(folder, 'meteo.txt')
    par_file = os.path.join(folder, 'par.txt')
    lake_file = os.path.join(folder, 'lake.txt')

Remember you may use the tilde '~' expansion.

Then, type::

    okplm.run_okp(output_file=output_file, meteo_file=meteo_file,
                   par_file=par_file, lake_file=lake_file)

You may also define a start, an end date and a periodicity for the simulations::

    okplm.run_okp(output_file=output_file, meteo_file=meteo_file,
                   par_file=par_file, lake_file=lake_file, start_date='2014-01-01',
                   end_date='2015-12-31', periodicity='weekly')

The output of daily simulations can be given at ``daily``, ``weekly`` or ``monthly`` 
frequency using the argument ``output_periodicity``.

If you provide a file containing observational data (``validation_data_file``)
and a file name where to write the validation results (``validation_res_file``),
error statistics are calculated and written to the specified file.

Other useful functions are ``okplm.read_dict()`` and ``okplm.write_dict()``,
which can be used to read and write the lake data and parameter files.

You can include the previous commands in a Python script (see the example
script ``test_script.py``). To run a python script from the command line, type:

.. code:: shell

    python path_to_script

Output data
-----------

The OKP model produces three types of output data:

* water temperature simulations, saved to the file ``output_file``.
* estimated parameter values (if not provided by the user), saved to the file
  ``par_file`` described above.
* indicators of simulation performance (if validation data is provided), saved
  to the file ``validation_res_file``.

File ``output_file``
^^^^^^^^^^^^^^^^^^^^
Main output file. It contains the simulated epilimnion and hypolimnion
temperature at the requested output periodicity.

The file is structured in three columns separated by white spaces:

* date: date in the format 'yyyy-mm-dd'.
* tepi: epilimnion temperature (ºC).
* thyp: hypolimnion temperature (ºC).

::

    date tepi thyp
    2015-01-01 0.7736048264277242 4.0
    2015-01-02 0.8253707698690544 4.001647106544848
    2015-01-03 0.780854030568508 4.001663640357946
    2015-01-04 0.5561293109277756 4.0
    2015-01-05 0.31121842955433243 4.0
    2015-01-06 0.06755075725464099 4.0
    2015-01-07 0.0 4.0
    2015-01-08 0.0 4.0
    2015-01-09 0.0 4.0
    ...

File ``validation_res_file``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Optional output file. It contains performance statistics of the simulation,
calculated if ``validation_data_file`` and ``validation_res_file`` are defined.

The file is structured in six columns separated by white spaces:

* n: number of measurements.
* sd: standard deviation.
* r: correlation coefficient.
* me: mean error.
* mae: mean absolute error.
* rmse: root mean square error.

The first line of results corresponds to the epilimnion, and the second line of
results corresponds to the hypolimnion.

::

    n sd r me mae rmse
    10 2.285 0.871 -0.025 1.555 2.286
    10 0.596 0.757 -0.018 0.452 0.597

