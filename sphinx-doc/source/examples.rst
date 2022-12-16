Examples of usage of the package ``okplm``
==========================================

You can test the application with examples provided.
The package contains four data examples in the folder
``examples``. An associated Python script (``test_script.py``)
and a module based on the ``plotly`` package (``plotly_fonctions.py``)
to plot results are available in the folder ``tests``.

The data
--------

In all cases the lake data in the ``lake.txt`` file corresponds to the Lake Allos
(lake code = ALL04). The meteorological data (``meteo.txt``) is synthetic data
based on meteorological data. Air temperature has been created using a seasonal
component and an ARMA model, while solar radiation data corresponds to the
seasonal component only.

Three of the cases are used to exemplify the usage of ``okplm`` for three different
periodicities. The necessary data for these tests can be found in the folders:

* synthetic_case_daily : daily data
* synthetic_case_weekly: weekly data
* synthetic_case_monthly: monthly data

The simulations
---------------

For these three case the input is meteorological data (``meteo.txt``) and lake
data (``lake.txt``). Thus, the model parameters are calculated from lake
characteristics given in ``lake.txt`` with the following command:

.. code:: python

    okplm.run_okp(output_file, meteo_file, par_file, lake_file,
                  periodicity=periodchoice)


In the case of the simulation with daily data, the script
``test_script.py`` gives example of validation of the model results
with an observation data file ``obs.txt``.

.. code:: python

    okplm.run_okp(output_file, meteo_file, par_file, lake_file,
                  periodicity=periodchoice,
                  validation_data_file=validation_data_file,
                  validation_res_file=validation_res_file)

The remaining test case (synthetic_case_par_given) exemplifies the case when
the parameter file is given. The data are in the folder:

* examples/synthetic_case_given : daily data

The model uses the given parameter values (``par.txt``)
and the daily meteorological data (``meteo.txt``). The file
``lake.txt`` is not necessary.

Plotting of results
-------------------

You can plot the simulation results with the function ``plotlyoutput()``
in the module ``tests/plotly_functions.py``, in addition to validation
criteria (n, sd, r, me, mae et rmse) and observations, if they are available,
with the instruction :

.. code:: python

    plotlyoutput(folder)

The results are then presented as an html file such as:

.. image:: ../../images/plotlyoutput.png
    :alt: Example of figure created by the function ``plotlyoutput()``

