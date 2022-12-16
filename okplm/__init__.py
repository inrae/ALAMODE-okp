"""okplm: Python package to simulate epilimnion and hypolimnion temperatures.

`okplm` is a package in Python 3 used to simulate the epilimnion and
hypolimnion temperature of freshwater bodies using the OKP lake model (Prats &
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

# References
* Kettle, H.; Thompson, R.; Anderson, N. J.; Livingstone, D. (2004) Empirical
modeling of summer lake surface temperatures in southwest Greenland. *Limnology
and Oceanography*, 49(1), 271-282, doi:
[10.4319/lo.2004.49.1.0271](https://doi.org/10.4319/lo.2004.49.1.0271).
* Ottosson, F.; Abrahamsson, O. (1998) Presentation and analysis of a model
simulating epilimnetic and hypolimnetic temperatures in lakes. *Ecological
Modelling*, 110(3), 233-253, doi:
[10.1016/S0304-3800(98)00067-2](https://doi.org/10.1016/S0304-3800(98)00067-2)
* Prats, J.; Danis, P.-A. (2019) An epilimnion and hypolimnion temperature
model based on air temperature and lake characteristics. *Knowledge and
Management of Aquatic Ecosystems*, 420, 8, doi:
[10.1051/kmae/2019001](https://doi.org/10.1051/kmae/2019001).

"""
# Copyright 2019 Segula Technologies - Agence Française pour la Biodiversité.
# Copyright 2020-2022 Segula Technologies - Office Français de la Biodiversité.
#
# This file is part of the Python package "okplm".
#
# The package "okplm" is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The package "okplm" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with "okplm".  If not, see <https://www.gnu.org/licenses/>.


from .parameter_constants import *
from .parameter_functions import estimate_parameters
from .input_output import read_dict, write_dict
from .time_functions import *
from .validation import error_statistics
from .okp_model import run_okp
from ._version import __version__
