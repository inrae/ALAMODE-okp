"""Functions to calculate parameter values.

This module contains the definition of the functions used to estimate the
value of the parameters used by the OKP lake model. These equations were
derived in Prats & Danis (2019).

The functions included in this module are:

    - estimate_par_a: estimate parameter A.
    - estimate_par_alpha: estimate parameter alpha.
    - estimate_par_b: estimate parameter B.
    - estimate_par_beta: estimate parameter beta.
    - estimate_par_c: estimate parameter C.
    - estimate_par_e: estimate parameter E.
    - estimate_parameters: estimate OKP parameter values.

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


from numpy import exp, log


def estimate_parameters(var_vals, par_cts):
    """Estimate the OKP parameter values.

    Args:
        var_vals: a dictionary indicating the value of the independent
            variables 'latitude' (degrees North), 'altitude' (m), 'zmax' (m),
            'surface' (m\\ :sup:`2`\\ ), 'volume' (m\\ :sup:`3`\\).
        par_cts: a dictionary indicating the value of the parameter constants
            'ALPHA1'-'ALPHA4', 'BETA1'-'BETA3', 'A1'-'A4', 'B1'-'B2',
            'C1'-'C2', 'D', 'E1'-'E3'.

    Returns:
        A dictionary of the OKP model parameter values according to Eq. (21,
        23-25, 27-28) in Prats & Danis (2019, p. 6-10).

    Example:
        .. code:: python

            var_vals = {'latitude': 44.233,
                        'altitude': 2232,
                        'surface': 528425,
                        'volume': 9775853,
                        'zmax': 51}
            par_cts = {'A1': 39.9, 'A2': -0.484, 'A3': -4.52E-3, 'A4': -0.167,
                       'ALPHA1': 0.52, 'ALPHA2': -3.0E-4, 'ALPHA3': 0.25,
                       'ALPHA4': -0.36,
                       'B1': 1.058, 'B2': -0.0010,
                       'BETA1': 1.0, 'BETA2': 0.13, 'BETA3': 0.95,
                       'C1': 1.12E-3, 'C2': -3.62E-6,
                       'D': 0.51,
                       'E1': 0.10, 'E2': 2.0, 'E3': -1.8}
            pars = estimate_parameters(var_vals=var_vals, par_cts=par_cts)
    """
    pars = {'A': estimate_par_a(var_vals, par_cts),
            'B': estimate_par_b(var_vals, par_cts),
            'C': estimate_par_c(var_vals, par_cts),
            'D': par_cts['D'],
            'E': estimate_par_e(var_vals, par_cts),
            'ALPHA': estimate_par_alpha(var_vals, par_cts)}
    pars.update({'BETA': estimate_par_beta(pars['E'], par_cts)})
    pars.update({'at_factor': 1.0, 'sw_factor': 1.0})
    return pars


def estimate_par_a(var_vals, par_cts):
    """Estimate the parameter A.

    Args:
        var_vals: a dictionary indicating the value of the independent
            variables 'latitude' (degrees North), 'altitude' (m) and 'surface'
            (m\\ :sup:`2`\\).
        par_cts: a dictionary indicating the value of the parameter constants
            'A1' to 'A4'.

    Returns:
        The estimated value of the parameter *A* according to Eq. (21) in Prats
        & Danis (2019, p.6).

    Example:
        .. code:: python

            var_vals = {'latitude': 44.233,
                        'altitude': 2232,
                        'surface': 528425}
            par_cts = {'A1': 39.9,
                       'A2': -0.484,
                       'A3': -4.52E-3,
                       'A4': -0.167}
            a = estimate_par_a(var_vals=var_vals, par_cts=par_cts)
    """

    a = par_cts['A1'] + \
        par_cts['A2']*var_vals['latitude'] + \
        par_cts['A3']*var_vals['altitude'] + \
        par_cts['A4']*log(var_vals['surface'])

    return a


def estimate_par_alpha(var_vals, par_cts):
    """Estimate the parameter alpha.

    Args:
        var_vals: a dictionary indicating the value of the independent
            variables 'altitude' (m), 'surface' (m\\ :sup:`2`\\), and 'volume'
            (m\\ :sup:`3`\\).
        par_cts: a dictionary indicating the value of the parameter constants
            'ALPHA1' to 'ALPHA4'.

    Returns:
        The estimated value of the parameter :math:`\\alpha` according to Eq.
        (23) in Prats & Danis (2019, p. 6).

    Example:
        .. code:: python

            var_vals = {'altitude': 2232,
                        'surface': 528425,
                        'volume': 9775853}
            par_cts = {'ALPHA1': 0.52,
                       'ALPHA2': -3.0E-4,
                       'ALPHA3': 0.25,
                       'ALPHA4': -0.36}
            alpha = estimate_par_alpha(var_vals=var_vals, par_cts=par_cts)
    """

    alpha = exp(par_cts['ALPHA1'] +
                par_cts['ALPHA2']*var_vals['altitude'] +
                par_cts['ALPHA3']*log(var_vals['surface']) +
                par_cts['ALPHA4']*log(var_vals['volume']))

    return alpha


def estimate_par_b(var_vals, par_cts):
    """Estimate the parameter B.

    Args:
        var_vals: a dictionary indicating the value of the independent variable
            'zmax' (m).
        par_cts: a dictionary indicating the value of the parameter constants
            'B1' to 'B2'.

    Returns:
        The estimated value of the parameter *B* according to Eq. (24) in Prats
        & Danis (2019, p.6).

    Example:
        .. code:: python

            var_vals = {'zmax': 51}
            par_cts = {'B1': 1.058,
                       'B2': -0.0010}
            b = estimate_par_b(var_vals=var_vals, par_cts=par_cts)
    """

    b = par_cts['B1'] + par_cts['B2']*var_vals['zmax']

    return b


def estimate_par_beta(par_e, par_cts):
    """Estimate the parameter beta.

    Args:
        par_e: value of the parameter E [0 - 1].
        par_cts: a dictionary indicating the value of the parameter constants
            'BETA1' to 'BETA3'.

    Returns:
        The estimated value of the parameter :math:`\\beta` according to Eq.
        (27) in Prats & Danis (2019, p. 9).

    Example:
        .. code :: python

            par_e = 0.24
            par_cts = {'BETA1': 1.0,
                       'BETA2': 0.13,
                       'BETA3': 0.95}
            beta = estimate_par_beta(par_e=par_e, par_cts=par_cts)
    """

    if par_e > par_cts['BETA3']:
        beta = par_cts['BETA1']
    else:
        beta = par_cts['BETA2']

    return beta


def estimate_par_c(var_vals, par_cts):
    """Estimate the parameter C.

    Args:
        var_vals: a dictionary indicating the value of the independent variable
            'altitude' (m).
        par_cts: a dictionary indicating the value of the parameter constants
            'C1' to 'C2'.

    Returns:
        The estimated value of the parameter *C* according to Eq. (25) in Prats
        & Danis (2019, p. 6).

    Example:
        .. code:: python

            var_vals = {'altitude': 2232}
            par_cts = {'C1': 1.12E-3,
                       'C2': -3.62E-6}
            c = estimate_par_c(var_vals=var_vals, par_cts=par_cts)
    """

    c = par_cts['C1'] + par_cts['C2']*var_vals['altitude']

    return c


def estimate_par_e(var_vals, par_cts):
    """Estimate the parameter E.

    Args:
        var_vals: a dictionary indicating the value of the independent
            variables 'surface' (m\\ :sup:`2`\\) and 'volume' (m\\ :sup:`3`\\).
        par_cts: a dictionary indicating the value of the parameter constants
            'E1' to 'E3'.

    Returns:
        The estimated value of the parameter *E* according to Eq. (28) in Prats
        & Danis (2019, p. 10).

    Example:
        .. code:: python

            var_vals = {'surface': 528425,
                        'volume': 9775853}
            par_cts = {'E1': 0.10,
                       'E2': 2.0,
                       'E3': -1.8}
            e = estimate_par_e(var_vals=var_vals, par_cts=par_cts)
    """

    var_vals['zmean'] = var_vals['volume']/var_vals['surface']

    e = par_cts['E1'] + \
        (1 - par_cts['E1'])/(1 + exp(par_cts['E3']*(par_cts['E2'] -
                             log(var_vals['zmean']))))

    return e
