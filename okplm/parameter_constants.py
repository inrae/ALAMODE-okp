"""OKP lake model constants.

This module defines the constants of the equations used to estimate the
parameter values of the model OKP as a function of water body characteristics.
The constants are defined in Prats & Danis (2019).

References:
    * Prats, J.; Danis, P.-A. (2019) An epilimnion and hypolimnion temperature
      model based on air temperature and lake characteristics. *Knowledge and
      Management of Aquatic Ecosystems*, 420, 8, doi: 10.1051/kmae/2019001.

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


# Epilimnion parameters
# ---------------------
# Parameter alpha
# alpha=exp(ALPHA1 + ALPHA2*altitude + ALPHA3*ln(surface) + ALPHA4*ln(volume))
ALPHA1 = 0.52
ALPHA2 = -3.0E-4
ALPHA3 = 0.25
ALPHA4 = -0.36

# Parameter A
# A = A1 + A2*latitude + A3*altitude + A4*ln(surface)
A1 = 39.9
A2 = -0.484
A3 = -4.52E-3
A4 = -0.167

# Parameter B
# B = B1 + B2*zmax
B1 = 1.058
B2 = -0.0010

# Parameter C
# C = C1 + C2*altitude
C1 = 1.12E-3
C2 = -3.62E-6

# Hypolimnion parameters
# ----------------------
# Parameter beta
# if E > BETA3: beta = BETA1
# if E <= BETA3: beta = BETA2
BETA1 = 1.0
BETA2 = 0.13
BETA3 = 0.95

# Parameter D
D = 0.51

# Parameter E
# E = E1 + (1 - E1)/{1 + exp[E3(E2 - ln(zmean))]}
# natural lakes
E1_LAKE = 0.10
E2_LAKE = 2.0
E3_LAKE = -1.8

# reservoirs
E1_RES = 0.49
E2_RES = 1.7
E3_RES = -2.0

# Dictionary with all parameter constants
par_cts = {'ALPHA1': ALPHA1, 'ALPHA2': ALPHA2,
           'ALPHA3': ALPHA3, 'ALPHA4': ALPHA4,
           'A1': A1, 'A2': A2, 'A3':A3, 'A4': A4,
           'B1': B1, 'B2': B2, 'C1': C1, 'C2': C2,
           'BETA1': BETA1, 'BETA2': BETA2, 'BETA3': BETA3,
           'D': D,
           'E1_LAKE': E1_LAKE, 'E2_LAKE': E2_LAKE,
           'E3_LAKE': E3_LAKE,
           'E1_RES': E1_RES, 'E2_RES': E2_RES, 'E3_RES': E3_RES}
