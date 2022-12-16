"""Functions for time-related operations.

This module contains functions for time operations (e.g., time averaging or
selection of date ranges).

The included functions are:

    - daily_f: apply function on daily periods.
    - monthly_f: apply function on monthly periods.
    - select_daterange: return indices between two dates.
    - weekly_f: apply function on weekly periods.

"""
# Copyright 2016-2018 Irstea - Agence Française pour la Biodiversité.
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


from datetime import datetime

import numpy as np


def daily_f(t, x, funcname):
    """Apply a function using subdaily values as args to obtain daily values.

    Args:
        t: datetime sequence at subdaily frequency. Missing timestamps are not
            allowed.
        x: data sequence, the same length of t.
        funcname: the function to be used (sum, numpy.mean, etc.).

    Returns:
        A tuple of two sequences/arrays (t_day, y_day). The sequence t_day is a
        datetime sequence at daily frequency. The sequence y_day is the output
        data sequence, result of applying funcname to the x values for each
        day. If the input data for a given day is less than 90% of the
        measurements for a day, a nan value is returned.
    """
    # Arrange data by days
    nmes = len(t)
    x_day = dict()
    for i in range(nmes):
        t_day = t[i].strftime('%Y/%m/%d')
        if t_day in x_day:
            x_day[t_day].append(x[i])
        else:
            x_day[t_day] = [x[i]]

    # Make the calculations
    t_day = []
    y_day = []
    dt = (t[1] - t[0]).total_seconds()  # measurement interval
    nmesday = 86400//dt
    for d in x_day:
        t_day.append(datetime.strptime(d, '%Y/%m/%d'))
        if len(x_day[d]) < nmesday*0.90:
            y_day.append(np.nan)
        else:
            ind = np.logical_not(np.isnan(x_day[d]))
            y_day.append(funcname(np.array(x_day[d])[ind]))

    # Sort the data
    sorting_index = np.argsort(t_day)
    t_day = np.array(t_day)[sorting_index]
    y_day = np.array(y_day)[sorting_index]

    return t_day, y_day


def monthly_f(t, x, funcname, input_type):
    """Apply a function using daily/subdaily values to obtain monthly values.

    Args:
        t: datetime sequence at daily or subdaily frequency. There should not
            be missing timestamps.
        x: data sequence, the same length of t.
        funcname: the function to be used (sum, numpy.mean, etc.).
        input_type: type of input data, "daily" or "subdaily".

    Returns:
        A tuple of two sequences/arrays (t_mon, y_mon). The sequence t_mon
        is a datetime sequence at monthly frequency. The date indicates the
        beginning of each month. The sequence y_mon is the output data
        sequence, result of applying funcname to the x values for each month.
        If data there are at least 3 days with missing data in a month, a nan
        value is returned.
    """
    from calendar import monthrange

    # Convert subdaily data to daily data if necessary
    if input_type == 'subdaily':
        t_day, x_day = daily_f(t, x, funcname)
    else:
        t_day, x_day = np.array(t), np.array(x)

    # Arrange the data by month
    ndays = len(t_day)
    x_mon = dict()
    for i in range(ndays):
        t_mon = t_day[i].strftime('%m/%Y')
        if t_mon in x_mon:
            x_mon[t_mon].append(x_day[i])
        else:
            x_mon[t_mon] = [x_day[i]]

    # Make the calculations
    t_mon = []
    y_mon = []
    for d in x_mon:
        t_mon.append(datetime.strptime(d, '%m/%Y'))
        month, year = d.split('/')
        month = int(month)
        year = int(year)
        ndaysmon = monthrange(year, month)[1]
        if sum(np.isnan(x_mon[d])) >= 3:
            # Not enough days of data available
            y_mon.append(np.nan)
        else:
            ind = np.logical_not(np.isnan(x_mon[d]))
            y_mon.append(funcname(np.array(x_mon[d])[ind]))

    # Sort the data
    sorting_index = np.argsort(t_mon)
    t_mon = np.array(t_mon)[sorting_index]
    y_mon = np.array(y_mon)[sorting_index]

    return t_mon, y_mon


def select_daterange(t, t_start, t_end):
    """Return indices of dates comprised between two dates.

    Args:
        t: list or array of dates in datetime format.
        t_start: initial date in datetime format.
        t_end: last date in datetime format.

    Returns:
        An array of indices of dates in t comprised between t_start and t_end
        (or equal).
    """
    t = np.array(t)
    ind1 = np.less_equal(t_start, t)
    ind2 = np.less_equal(t, t_end)
    ind = ind1*ind2

    return ind


def weekly_f(t, x, funcname, input_type):
    """Apply a function using daily/subdaily values to obtain weekly values.

    Args:
        t: datetime sequence at daily/subdaily frequency. There should not be
            missing timestamps.
        x: data sequence, the same length of t.
        funcname: the function to be used (sum, numpy.mean, etc.).
        input_type: type of input data, "daily" or "subdaily".

    Returns:
        A tuple of two sequences/arrays (t_week, y_week). The sequence t_week
        is a datetime sequence at weekly frequency. The date indicates the
        beginning of each week. The sequence y_week is the output data
        sequence, result of applying funcname to the x values for each week.
        If data is not available for all days for a given week, a nan value is
        returned.
    """
    # Convert subdaily data to daily data if necessary
    if input_type == 'subdaily':
        t_day, x_day = daily_f(t, x, funcname)
    else:
        t_day, x_day = np.array(t), np.array(x)

    # Arrange the data by weeks
    ndays = len(t_day)  # number of days in the period
    x_week = dict()
    t_week = 1
    for i in range(ndays):
        if i % 7 == 0:
            x_week[t_week] = [x_day[i]]
        elif i % 7 < 6:
            x_week[t_week].append(x_day[i])
        else:
            x_week[t_week].append(x_day[i])
            t_week += 1
    ind_week_start = np.mod(range(ndays), 7) == 0
    t_week = t_day[ind_week_start]

    # Make the calculations
    y_week = []
    for w in x_week:
        if len(x_week[w]) == 7:
            y_week.append(funcname(x_week[w]))
        else:
            y_week.append(funcname(np.nan))
    y_week = np.array(y_week)

    # Sort the data
    sorting_index = np.argsort(t_week)
    t_week = np.array(t_week)[sorting_index]
    y_week = np.array(y_week)[sorting_index]

    return t_week, y_week
