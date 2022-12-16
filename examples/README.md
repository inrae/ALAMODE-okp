# okplm examples
This folder contains data examples to test the execution of the OKP Lake Model.

## Data examples list
You can test the software using the example files provided. The module contains
four data examples in the folder `examples`. A Python script 
(`test_script.py`) using these data is available in the folder `tests`.

In all cases the lake data in the `lake.txt` file corresponds to the Lake Allos
(lake code = ALL04). The meteorological data (`meteo.txt`) is synthetic data
based on SAFRAN data. Air temperature has been created using a seasonal
component and an ARMA model, while solar radiation data corresponds to the
seasonal component only.

Three of the cases are used to exemplify the usage of `okplm` for three different
 periodicities:

* synthetic_case_daily : daily data
* synthetic_case_weekly: weekly data
* synthetic_case_monthly: monthly data

For these three case the input is meteorological data (`meteo.txt`) and lake
data (`lake.txt`). Thus, the model parameters are calculated from lake
characteristics given in `lake.txt`.

The remaining test case (synthetic_case_par_given) exemplifies the case when
the parameter file is given. The input is daily meteorological data
(`meteo.txt`) and parameter values (`par.txt`). The model uses the given
parameter values and the file `lake.txt` is not necessary.

## Test script
The test script `test_script.py` in the folder `tests` runs the OKP lake model
for synthetic_case_daily. To test the model, replace the value of
`path_to_repertory_okplm` by an appropriate value and run the script.
