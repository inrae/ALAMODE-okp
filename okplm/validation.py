"""Functions for the validation of simulation results.

This module contains only one function, used to validate simulation results:

- error_statistics: calculate error statistics.

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


import numpy as np


def error_statistics(t_sim, v_sim, t_obs, v_obs):
    """Calculate error statistics.

    Args:
        t_sim: time array of the simulated data.
        v_sim: array with simulated values.
        t_obs: time array of observed data.
        v_obs: observed values.

    Returns:
        A tuple of six performance indicators (n, sd, r, me, mae, rmse),
        corresponding to the number of measurements (n), the standard deviation
        (sd), the correlation coefficient (r), the mean error (me), the mean
        absolute error (mae), and the root mean square error (rmse).
    """
    # Make sure input data are arrays
    t_sim = np.array(t_sim)
    v_sim = np.array(v_sim)
    t_obs = np.array(t_obs)
    v_obs = np.array(v_obs)

    # Make sure input data is well ordered and without repetitions
    for c in ['_sim', '_obs']:
        if len(eval('t' + c)) != len(np.unique(eval('t' + c))):
            msg = 'Non unique time stamps in t' + c
            raise ValueError(msg)
        ind_ord = np.argsort(eval('t' + c))
        locals()['t' + c] = eval('t' + c)[ind_ord]
        locals()['v' + c] = eval('v' + c)[ind_ord]

    # Exclude observations out of the simulation period
    ind_in = np.in1d(t_obs, t_sim)
    t_obs = t_obs[ind_in]
    v_obs = v_obs[ind_in]

    # Select simulated values corresponding to observed values
    ind = np.in1d(t_sim, t_obs)
    t_sim = t_sim[ind]
    v_sim = v_sim[ind]

    # Calculate residuals
    res = v_sim - v_obs

    # Calculate error statistics
    n = len(t_sim)
    sd = np.std(res)
    r = np.corrcoef(v_sim, v_obs, rowvar=False)[0, 1]
    me = np.mean(res)
    mae = np.mean(np.abs(res))
    rmse = np.sqrt(np.mean(res**2))

    return n, sd, r, me, mae, rmse
