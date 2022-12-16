"""OKP lake model functions.

This module contains the functions used to calculate epilimnion and hypolimnion
temperature corresponding to the OKP model, described in Prats & Danis (2019).

The included functions are:

    - calc_epilimnion_temperature: calculate epilimnion temperature.
    - calc_hypolimnion_temperature: calculate hypolimnion temperature.
    - fit_sinusoidal: fit a sinusoidal function.
    - main: parse command line arguments and run the OKP model.
    - run_okp: run the OKP model.
    - water_density: calculate water density.

References:
    * Prats, J.; Danis, P.-A. (2019) An epilimnion and hypolimnion temperature
      model based on air temperature and lake characteristics. *Knowledge and
      Management of Aquatic Ecosystems*, 420, 8, doi: 10.1051/kmae/2019001.

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


import argparse
import os
from datetime import datetime

import numpy as np

import okplm


def calc_epilimnion_temperature(tair, sr, par_vals, periodicity='daily'):
    """Calculate epilimnion temperature.

    Args:
        tair: daily air temperature (ºC).
        sr: daily solar radiation (W/m\\ :sup:`2`\\ ).
        par_vals: a dictionary with values for the parameters ALPHA, A,
            B, C, at_factor and sw_factor.
        periodicity: periodicity of the input meteorological data and of the
            simulation; it can take the values 'daily', 'weekly', 'monthly'.

    Returns:
        The daily simulated epilimnion temperature in degrees C.
    """
    # Convert units of parameters ALPHA according to periodicity
    if periodicity == 'daily':
        nper_yr = 365.25  # days
    elif periodicity == 'weekly':
        nper_yr = 52  # weeks
    elif periodicity == 'monthly':
        nper_yr = 12  # months
    c = 365.25/nper_yr
    par_vals['ALPHA'] = par_vals['ALPHA']*c
    if par_vals['ALPHA'] > 1:
        par_vals['ALPHA'] = 1

    # Calculate ftair, the exponentially smoothed function of tair
    tair2 = tair*par_vals['at_factor'] - par_vals['mat']
    nmes = len(tair)
    ftair = np.zeros(nmes)
    ftair[0] = tair2[0]
    for i in np.arange(1, nmes):
        ftair[i] = par_vals['ALPHA']*tair2[i] + \
            (1 - par_vals['ALPHA'])*ftair[i - 1]

    # Calculate fsr, a sinusoidal function of solar radiation variability
    t = np.arange(nmes)
    m_sr, a_sr, ph_sr = fit_sinusoidal(t, sr*par_vals['sw_factor'],
                                       period=nper_yr)
    fsr = m_sr + a_sr*np.sin(2*np.pi*t/nper_yr + ph_sr)

    # Calculate epilimnion temperature tepi
    tepi = par_vals['A'] + par_vals['B']*ftair + par_vals['C']*fsr
    ind = np.less_equal(tepi, 0)
    tepi[ind] = 0

    return tepi


def calc_hypolimnion_temperature(tepi, par_vals, periodicity='daily'):
    """Calculate hypolimnion temperature.

    Args:
        tepi: daily epilimnion temperature (ºC).
        par_vals: a dictionary with values for the parameters BETA, A, D and E.
        periodicity: periodicity of the input epilimnion temperature data and
            of the simulation; it can take the values 'daily', 'weekly',
            'monthly'.

    Returns:
        The daily simulated hypolimnion temperature in ºC.
    """
    # Convert units of parameters BETA according to periodicity
    if periodicity == 'daily':
        nper_yr = 365.25  # days
    elif periodicity == 'weekly':
        nper_yr = 52  # weeks
    elif periodicity == 'monthly':
        nper_yr = 12  # months
    c = 365.25/nper_yr
    par_vals['BETA'] = par_vals['BETA']*c
    if par_vals['BETA'] > 1:
        par_vals['BETA'] = 1

    # Calculate hypolimnion temperature
    nmes = len(tepi)
    fet = np.zeros(nmes)
    thyp = np.zeros(nmes)
    thyp_prov = np.zeros(nmes)
    for i in range(nmes):
        if i == 0:
            fet[i] = tepi[i]
            thyp_prov[i] = par_vals['D']*par_vals['A'] + par_vals['E']*fet[i]
            thyp[i] = thyp_prov[i]
        else:
            fet[i] = par_vals['BETA']*(tepi[i]) + \
                (1 - par_vals['BETA'])*fet[i-1]
            thyp_prov[i] = par_vals['D']*par_vals['A'] + par_vals['E']*fet[i]
            dtemp = thyp_prov[i] - thyp_prov[i-1]
            thyp[i] = thyp[i-1] + dtemp

        # epilimnion density in [kg/m^3]
        dens_e = water_density(tepi[i])
        # hypolimnion density in [kg/m^3]
        dens_h = water_density(thyp[i])
        if dens_e >= dens_h:
            thyp[i] = tepi[i]
        if thyp[i] < 4:
            thyp[i] = 4

    return thyp


def fit_sinusoidal(x, y, period):
    """Fit a sinusoidal function to data.

    This function fits a sinusoidal function of the form:

        :math:`y = m + a\\sin(2\\pi x/period + ph)`

    Args:
        x: array of time data.
        y: array of response data.
        period: length of the period in time units.

    Returns:
        A tuple (m, a, ph) of the three coefficients of a sinusoidal function
        providing the mean value (m), the amplitude of the sinusoidal
        function (a), and the phase of the sinusoidal function (ph).
    """
    # Calculate Fourier coefficients for the main frequency
    a0 = np.mean(y)
    a1 = 2*np.mean(y*np.cos(2*np.pi*x/period))
    b1 = 2*np.mean(y*np.sin(2*np.pi*x/period))

    # Calculate coefficients of the sinusoidal function
    m = a0
    a = np.sqrt(a1**2 + b1**2)
    ph = np.arctan2(a1, b1)

    return m, a, ph


def run_okp(output_file, meteo_file, par_file, lake_file=None, start_date=None,
            end_date=None, periodicity='daily', output_periodicity=None,
            validation_data_file=None, validation_res_file=None):
    """Run the OKP model.

    Args:
        output_file: path of the output file.
        meteo_file: path of the meteorological data file.
        par_file: path of the parameter file.
        lake_file: path of the lake data file (optional, it is only necessary
            if par_file is not provided).
        start_date: date of start of the simulation in the format 'YYYY-mm-dd'.
        end date: date of end of the simulation in the format 'YYYY-mm-dd'.
        periodicity: periodicity of the input meteorological data and of the
            simulation; it can take the values 'daily', 'weekly', 'monthly'.
        output_periodicity: periodicity of the output data (only implemented
            for daily simulations); it can take the values 'daily', 'weekly',
            'monthly'. It is only used if the periodicity of the simulations is
            'daily'.
        validation_data_file: path of the file containing observational data to
            calculate error statistics. If validation_data_file is defined, you
            need to define also validation_res_file. If None, error statistics
            are not calculated. Validation is only implemented for 'daily'
            simulations.
        validation_res_file: path of the file where validation results will be
            written. It requires the definition of a valid
            validation_data_file.

    Returns:
        A text file named output_file is written. If the par_file does not
        exist, it is also created by this function. If validation data is
        provided, the file validation_res_file containing information on error
        statistics is created too.
    """
    # Allow tilde expansion
    output_file = os.path.expanduser(output_file)
    meteo_file = os.path.expanduser(meteo_file)
    par_file = os.path.expanduser(par_file)
    if lake_file is not None:
        lake_file = os.path.expanduser(lake_file)
    if validation_data_file is not None:
        validation_data_file = os.path.expanduser(validation_data_file)
    if validation_res_file is not None:
        validation_res_file = os.path.expanduser(validation_res_file)

    # Read meteorological data
    meteo = np.genfromtxt(meteo_file, names=True, encoding='utf-8', dtype=None)
    t = [datetime.strptime(i, '%Y-%m-%d') for i in meteo['date']]

    # Filter meteorological data according to date range
    if any([start_date is not None, end_date is not None]):
        if start_date is not None:
            t_start = datetime.strptime(start_date, '%Y-%m-%d')
            if t_start < np.min(t):
                t_start = np.min(t)
                print('Start date of simulations before start of ' +
                      'meteorological data. Using start date of ' +
                      'meteorological data instead.')
        else:
            t_start = np.min(t)
        if end_date is not None:
            t_end = datetime.strptime(end_date, '%Y-%m-%d')
            if t_end > np.max(t):
                t_end = np.max(t)
                print('End date of simulations after end of ' +
                      'meteorological data. Using end date of ' +
                      'meteorological data instead.')
        else:
            t_end = np.max(t)
        ind = okplm.select_daterange(t, t_start, t_end)
        meteo = meteo[ind]
        t = np.array(t)[ind]

    # If par_file is not provided, estimate parameter values
    if not os.path.exists(par_file):
        # Read lake data
        lake_data = okplm.read_dict(lake_file)

        # Create dictionary with all parameter constants
        par_cts = {'ALPHA1': okplm.ALPHA1, 'ALPHA2': okplm.ALPHA2,
                   'ALPHA3': okplm.ALPHA3, 'ALPHA4': okplm.ALPHA4,
                   'BETA1': okplm.BETA1, 'BETA2': okplm.BETA2,
                   'BETA3': okplm.BETA3,
                   'A1': okplm.A1, 'A2': okplm.A2, 'A3': okplm.A3,
                   'A4': okplm.A4,
                   'B1': okplm.B1, 'B2': okplm.B2,
                   'C1': okplm.C1, 'C2': okplm.C2,
                   'D': okplm.D}
        if lake_data['type'] == 'R':
            # Reservoirs (submerged outlet)
            par_cts.update({'E1': okplm.E1_RES, 'E2': okplm.E2_RES,
                            'E3': okplm.E3_RES})
        elif lake_data['type'] == 'L':
            # Lakes (surface outlet)
            par_cts.update({'E1': okplm.E1_LAKE, 'E2': okplm.E2_LAKE,
                            'E3': okplm.E3_LAKE})

        # Estimate parameter values
        pars = okplm.estimate_parameters(var_vals=lake_data, par_cts=par_cts)

        # Calculate mean air temperature (mat)
        pars['mat'] = np.mean(meteo['tair'])

        # Write parameter values to file
        okplm.write_dict(pars, par_file)
    else:
        # Read parameter values
        pars = okplm.read_dict(par_file)

    # Simulate epilimnion temperature
    tepi_sim = calc_epilimnion_temperature(tair=meteo['tair'],
                                           sr=meteo['sr'], par_vals=pars,
                                           periodicity=periodicity)

    # Simulate hypolimnion temperature
    thyp_sim = calc_hypolimnion_temperature(tepi=tepi_sim, par_vals=pars,
                                            periodicity=periodicity)

    # Write simulation results to file
    if periodicity != 'daily' and output_periodicity is not None:
        output_periodicity = None
        print('Variable output periodicity only implemented for daily ' +
              'simulations. Ignoring output_periodicity.')
    if output_periodicity is None:
        temp_sim = np.vstack([meteo['date'], tepi_sim, thyp_sim])
    elif output_periodicity == 'daily':
        temp_sim = np.vstack([meteo['date'], tepi_sim, thyp_sim])
    else:
        if output_periodicity == 'weekly':
            tepi_p = okplm.weekly_f(t, tepi_sim, np.mean, 'daily')
            thyp_p = okplm.weekly_f(t, thyp_sim, np.mean, 'daily')
        elif output_periodicity == 'monthly':
            tepi_p = okplm.monthly_f(t, tepi_sim, np.mean, 'daily')
            thyp_p = okplm.monthly_f(t, thyp_sim, np.mean, 'daily')
        t_vec = [d.strftime('%Y-%m-%d') for d in tepi_p[0]]
        temp_sim = np.vstack([t_vec, tepi_p[1], thyp_p[1]])
    np.savetxt(output_file, temp_sim.T, fmt='%s %s %s',
               header='date tepi thyp', comments='')

    # Validation
    if validation_data_file is not None:
        # check periodicity is daily
        if periodicity in ['weekly', 'monthly']:
            print('Validation implemented only for daily simulations. ' +
                  'Ignoring validation.')
        else:
            # read validation data
            v_data = np.genfromtxt(validation_data_file, names=True,
                                   encoding='utf-8', dtype=None)
            # epilimnion temperature validation
            if 'tepi' in v_data.dtype.names:
                tepi_validation = okplm.error_statistics(
                        meteo['date'], tepi_sim, v_data['date'],
                        v_data['tepi'])
            else:
                tepi_validation = tuple([0] + [np.nan]*5)
            if 'thyp' in v_data.dtype.names:
                thyp_validation = okplm.error_statistics(
                        meteo['date'], thyp_sim, v_data['date'],
                        v_data['thyp'])
            else:
                thyp_validation = tuple([0] + [np.nan]*5)
            with open(validation_res_file, 'wt') as f:
                f.write('n sd r me mae rmse' + os.linesep)
                f.write('%d %.3f %.3f %.3f %.3f %.3f' % tepi_validation +
                        os.linesep)
                f.write('%d %.3f %.3f %.3f %.3f %.3f' % thyp_validation +
                        os.linesep)
    return


def water_density(temp):
    """Calculate the water density as a function of temperature.

    Args:
        temp: water temperature (ºC).

    Returns:
        The water density (kg/m\\ :sup:`3`\\ ) calculated using the formula by
        Markofsky & Harleman (1971).

    References:
        * Markofsky, M. and Harleman, D. R. F. (1971) *A predictive model for
          thermal stratification and water quality in reservoirs.*
          Environmental Protection Agency.
    """
    # Assign coefficient values
    dens_0 = 1000  # kg/m**3
    t0 = 4  # ºC
    alpha = 6.63e-6  # C**-2

    # Calculate density
    dens = dens_0*(1 - alpha*(temp - t0)**2)

    return dens


def main():
    """Parse command line arguments and run the OKP model.

    To obtain help on this function type "run_okp -h" in the command line.
    """
    # parser
    parser = argparse.ArgumentParser(description='Run OKP model')

    # optional arguments
    parser.add_argument('-f', '--folder', help='path to the model data folder')
    parser.add_argument('-m', '--meteo', help='name of the meteorological ' +
                        'data file')
    parser.add_argument('-l', '--lake', help='name of the lake data file')
    parser.add_argument('-p', '--par', help='name of the okp model ' +
                        'parameter file')
    parser.add_argument('-o', '--output', help='name of the output data ' +
                        'file')
    parser.add_argument('-a', '--obs_data', help='name of the observation ' +
                        'data file')
    parser.add_argument('-b', '--val_results', help='name of the validation ' +
                        'results file')
    parser.add_argument('-v', '--verbose', help='show runtime messages',
                        action='store_true')
    parser.add_argument('-s', '--start', help='start date (YYYY-mm-dd)')
    parser.add_argument('-e', '--end', help='end date (YYYY-mm-dd)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--daily', action='store_true',
                       help='daily simulation (default)')
    group.add_argument('-w', '--weekly', action='store_true',
                       help='weekly simulation')
    group.add_argument('-n', '--monthly', action='store_true',
                       help='monthly simulation')
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('--daily_output', action='store_true',
                        help='daily output (default)')
    group2.add_argument('--weekly_output', action='store_true',
                        help='weekly output (weekly average)')
    group2.add_argument('--monthly_output', action='store_true',
                        help='monthly output (monthly average)')

    # parse arguments
    args = parser.parse_args()

    # path names
    if args.folder is None:
        folder = os.getcwd()
    else:
        folder = os.path.expanduser(args.folder)

    for k in ['meteo', 'lake', 'par', 'output']:
        if vars(args)[k] is None:
            globals()[k + '_file'] = os.path.join(folder, k + '.txt')
        else:
            globals()[k + '_file'] = os.path.join(folder, vars(args)[k])
    if args.obs_data:
        obs_data = os.path.join(folder, args.obs_data)
    else:
        obs_data = None
    if args.val_results:
        val_results = os.path.join(folder, args.val_results)
    else:
        val_results = None

    # check input files
    if not os.path.exists(meteo_file):
        err_msg = 'Could not find ' + meteo_file
        raise FileNotFoundError(err_msg)

    if os.path.exists(par_file):
        if args.verbose:
            if os.path.exists(par_file):
                print('Parameter file exists. ' +
                      'Using provided parameter values.')
            else:
                raise FileNotFoundError(
                        'One of lake_file of par_file is necessary')
    elif os.path.exists(lake_file):
        if args.verbose:
            print('Parameter file does not exist. ' +
                  'Estimating parameter values from lake characteristics.')
    else:
        raise FileNotFoundError('One of lake_file or pars_file is necessary')

    # periodicity of simulation
    periodicity = 'daily'
    if args.daily:
        pass
    elif args.weekly:
        periodicity = 'weekly'
    elif args.monthly:
        periodicity = 'monthly'

    # periodicity of output
    output_periodicity = None
    if args.daily_output:
        output_periodicity = 'daily'
    elif args.weekly_output:
        output_periodicity = 'weekly'
    elif args.monthly_output:
        output_periodicity = 'monthly'

    # run okp model
    run_okp(output_file=output_file, meteo_file=meteo_file, par_file=par_file,
            lake_file=lake_file, start_date=args.start, end_date=args.end,
            periodicity=periodicity, output_periodicity=output_periodicity,
            validation_data_file=obs_data, validation_res_file=val_results)
    print('Output written to ' + output_file)

    return


if __name__ == '__main__':
    main()
