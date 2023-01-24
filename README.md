# okplm: Ottosson-Kettle-Prats Lake Model
Copyright 2019 Segula Technologies - Office Français de la Biodiversité.

<p align="center">
<img title="banner ALAMODE" src="images/ALAMOD_withlogos.png">
</p>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7564750.svg)](https://doi.org/10.5281/zenodo.7564750)

## Content

1. [What is the okplm package?](#purpose)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Dependencies](#dependencies)
5. [Usage](#Usage)
6. [Examples for okp](#Examples)
7. [References](#references)

<a name="purpose"></a>

## What is the okplm package ?

`okplm` is a package ALAMODE software in python 3 used to simulate the epilimnion and
hypolimnion temperature of freshwater bodies using the OKP model (Prats &
Danis, 2019).

The OKP model simulates water temperature at the daily frequence using air
temperature and solar radiation as forcing data. The model is the result of the
evolution of the models presented by Ottosson & Abrahamsson (1998) and Kettle
*et al.* (2004).

Water temperatures can be calculated using the default parameters for French
water bodies, parameterized as a function of lake characteristics (latitude,
altitude, maximum depth, surface area, volume) by Prats & Danis (2019). 

Otherwise, parameter values defined by the user may be used. Parameter values
for other geographical settings may be found in the works by Ottosson &
Abrahamsson (1998) (Swedish lakes) and Kettle *et al.* (2004) (epilimnion
temperatures for southwest Greenland lakes).

__Authors__ :

* Jordi Prats-Rodríguez (jprats@segula.es)
* Pierre-Alain Danis (pierre-alain.danis@ofb.gouv.fr)

<a name="requirements"></a>

## Requirements

You need Python 3.5 or later to run the `okplm` package. You can have
multiple Python versions (2.x and 3.x) installed on the same system
without problems.


<a name="installation"></a>

## Installation
### Cloning the repository
First you have to clone the `okplm` package with git:
```git
git clone https://gitlab.irstea.fr/alamode/okplm
```
This command creates the okplm repertory.


### Installing `okplm`
Using septuptools:
```bash
cd pathtorepertoryokplm
python setup.py install
```
Using pip :
```bash
cd pathtorepertoryokplm
pip install -U .
```


<a name="dependencies"></a>

## Dependencies

The application `okplm` depends on the following Python packages:

* numpy


<a name="Usage"></a>

## Usage

The model reads input and configuration data from three text files, one
obligatory and two optional:

* meteo_file: it contains air temperature and solar radiation data
* lake_file (optional): it contains lake characteristics (depth, surface,
volume, altitude, latitude). It is ignored if par_file is given.
* par_file (optional): it contains the value of the model parameters. If not
given by the user, the model creates the file calculating the value of the
parameters as a function of the lake characteristics defined in the lake_file
according to the parameterization by Prats & Danis (2019) for French freshwater
bodies.

If no start and end date are defined, the lenght of the simulation is
determined by the length of the meteo_file. In addition, meteorological data
may be provided at three different frequencies: daily, weekly and monthly.

Providing either lake_file or par_file is necessary. If the par_file is given,
the program uses the provided parameter values. Otherwise, the lake_file is
required and the program calculates the model parameters from the lake
characteristics included in the lake_file. See the extensive documentation for
further details on the formatting of input files.

Once you have created the input files, you can use the `okplm` package as a
command line application or a Python module.


### Command line application
To run `okplm` in the command line, change to the directory containing the
input files and make:

```bash
run_okp
```

Alternatively, you can indicate the input data folder. E.g.,

```bash
run_okp -f C:/users/yourself/data/lake_data
```

Please note that the software understands the tilde '~' expansion, so that you
may use instead:
```bash
run_okp -f ~/data/lake_data
```

By default, the model looks for the files named `meteo.txt` (meteorological
data), `lake.txt` (lake data) and `par.txt` (values of the model parameters).
You can specify other names using the optional arguments `-m`, `-l` and `-p`,
respectively. E.g.,
```bash
run_okp -m meteorology.txt
```

Similarly, the results are written by default to `output.txt`, but you can use
define another name using `-o`.

You can limit the length of the simulation by specifying the start and end
dates:
```bash
run_okp -s 2014-01-01 -e 2015-12-31
```

To tell the model the frequency of the input meteorological data and of the 
simulation you may use `-d` (daily), `-w` (weekly) or `-n` (monthly). E.g.
```bash
run_okp -w
```
By default the program assumes the input data is provided at a daily time step.

For daily simulations, the output can be given at daily, weekly of monthly
frequencies with the arguments `--daily_output`, `--weekly_output` and 
`--monthly_output`.

It is also possible to obtain error statistics of the daily simulations by
providing an observation data file (e.g., `obs.txt`) and the name of the
validation results file (e.g., `err_stats.txt`):
```bash
run_okp -a obs.txt -b err_stats.txt
```
If these file names are not provided, validation statistics are not calculated.

For obtaining help on the usage of the application, write:
```bash
run_okp -h
```


### Python module
To use `okplm` as a Python module you can simply import it and use the
functions within:

```python
import okplm
```

To run the model, first define the names of the different input and output
files. For example:
```python
import os.path
folder = path_to_data_repertory
output_file = os.path.join(folder, 'output.txt')
meteo_file = os.path.join(folder, 'meteo.txt')
par_file = os.path.join(folder, 'par.txt')
lake_file = os.path.join(folder, 'lake.txt')
```
Remember you may use the tilde '~' expansion.

Then, type:

```python
okplm.run_okp(output_file=output_file, meteo_file=meteo_file,
               par_file=par_file, lake_file=lake_file)
```

You may also define a start, an end date and a periodicity for the simulations:
```python
okplm.run_okp(output_file=output_file, meteo_file=meteo_file,
               par_file=par_file, lake_file=lake_file, start_date='2014-01-01',
               end_date='2015-12-31', periodicity='weekly')
```
The output of daily simulations can be given at `daily`, `weekly` or `monthly` 
frequency using the argument `output_periodicity`.

If you provide a file containing observational data (`validation_data_file`)
and a file name where to write the validation results (`validation_res_file`),
error statistics are calculated and written to the specified file.

Other useful functions are `okplm.read_dict()` and `okplm.write_dict()`,
which can be used to read and write the lake data and parameter files.

You can include the previous commands in a Python script (see the example
script `test_script.py`). To run a python script from the command line, type:

```bash
python path_to_script
```


<a name="Examples"></a>

## Examples for okplm

You can test the software using the example files provided. The module contains
four data examples in the folder `examples` and an example Python script
(`test_script.py`).

In all cases the lake data in the `lake.txt` file corresponds to the Lake Allos
(lake code = ALL04). The meteorological data (`meteo.txt`) is synthetic data
based on SAFRAN data. Air temperature has been created using a seasonal
component and an ARMA model, while solar radiation data corresponds to the
seasonal component only.

Three of the cases are used to exemplify the usage of `okplm` for three
different periodicities:

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

<a name="references"></a>

## References
* Kettle, H.; Thompson, R.; Anderson, N. J.; Livingstone, D. M. (2004)
Empirical modeling of summer lake surface temperatures in southwest Greenland.
*Limnology and Oceanography*, 49 (1), 271-282,
doi: [10.4319/lo.2004.49.1.0271](https://doi.org/10.4319/lo.2004.49.1.0271).
* Ottosson, F.; Abrahamsson, O. (1998) Presentation and analysis of a model
simulating epilimnetic and hypolimnetic temperatures in lakes. *Ecological
Modelling*, 110, 233-253, doi:
[10.1016/S0304-3800(98)00067-2](https://doi.org/10.1016/S0304-3800(98)00067-2).
* Prats, J.; Danis, P.-A. (2019) An epilimnion and hypolimnion temperature
model based on air temperature and lake characteristics. *Knowledge and
Management of Aquatic Ecosystems*, 420, 8, doi:
[10.1051/kmae/2019001](https://doi.org/10.1051/kmae/2019001).
