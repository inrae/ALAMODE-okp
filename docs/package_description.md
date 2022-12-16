# okplm: Ottosson-Kettle-Prats Lake Model

**Description:** Package containing the implementation of the OKP model (Prats & Danis, 2019).

**Language:** Python 3.

##	Functions
*	`okp_model.py`
    - *calc_epilimnion_temperature*: calculate epilimnion temperature from air temperature and solar radiation.
    - *calc_hypolimnion_temperature*: calculate hypolimnion temperature from epilimnion temperature.
    - *fit_sinusoidal*: fit a sinusoidal function.
    - *run_okp*: run the model.
    - *water_density*: calculate water density.
    - *main*: implement command line functionality.
*	`parameter_functions.py`
    -	*estimate_parameters*: calculate the value of all the model parameters.
    - *estimate_par_alpha*: calculate the value of the parameter $`\alpha`$ of the model as a function of altitude, surface area and volume.
    - *estimate_par_a*: calculate the value of the parameter *A* of the model as a function of latitude, altitude and surface area.
    - *estimate_par_b*: calculate the value of the parameter *B* of the model as a function of maximum depth.
    - *estimate_par_beta*: calculate the value of the parameter $`\beta`$ of the model as a function of the parameter *E*.
    - *estimate_par_c*: calculate the value of the parameter *C* of the model as a function of altitude.
    - *estimate_par_e*: calculate the value of the parameter *E* of the model as a function of surface area and volume.
*	`input_output.py`
    - *read_dict*: read a text file and create a dictionary (used to read `lake.txt` and `par.txt`).
    - *write_dict*: write a dictionary to a text file (used to write `par.txt`).

## Constants
*	`parameter_constants.py`
    - ALPHA1 = 0.5
    -	ALPHA2 = -3.0E-4
    -	ALPHA3 = 0.25
    -	ALPHA4 = -0.36
    - A1 = 39.9
    -	A2 = -0.484
    -	A3 = -4.52E-3
    -	A4 = -0.167
    - B1 = 1.058
    -	B2 = -0.0010
    -	BETA1 = 1
    -	BETA2 = 0.13
    -	BETA3 = 0.95
    -	C1 = 1.12E-3
    -	C2 = -3.62E-6
    -	D = 0.51
    -	E1_LAKE = 0.10
    -	E2_LAKE = 2.0
    -	E3_LAKE = -1.8
    -	E1_RES = 0.49
    -	E2_RES = 1.7
    -	E3_RES = -2.0

##	Input
*	`lake.txt`
    - **name**: lake name
    -	**latitude**: latitude [°N]
    -	**altitude**: altitude [m.a.s.l.]
    -	**zmax**: maximum depth [m]
    -	**surface**: surface area [m<sup>2</sup>]
    -	**volume**: volume [m<sup>3</sup>]
    -	**type**: water body type; it can be "L" (lake, surface outlet) or "R" (reservoir, submerged outlet)
*	`meteo.txt`
    - **date**: date in the format "YYYY-mm-dd"
    - **tair**: air temperature [°C]
    - **sr**: solar radiation [W m<sup>-2</sup>]
*	`par.txt` (optional)
    -	**ALPHA**
    -	**A**
    -	**B**
    -	**C**
    -	**BETA**
    -	**D**
    -	**E**

## Simulation options
*	Daily
*	Weekly
*	Monthly

Meteorological data has to be given with the correct periodicity.

## Output
* `output.txt`
    - date: date in the format "YYYY-mm-dd"
    -	tepi: epilimnion temperature [°C]
    -	thyp: hypolimnion temperature [°C]

## References
* Prats, J.; Danis, P.-A. (2019) An epilimnion and hypolimnion temperature model
based on air temperature and lake characteristics. *Knowledge and Management of Aquatic
Ecosystems*, 420, 8, doi: [10.1051/kmae/2019001](https://doi.org/10.1051/kmae/2019001).

