"""Time series with Rangeslider

Functions to plot okplm simulation results based on
https://plot.ly/python/time-series/#time-series-with-rangeslider

There are two functions:
* plotlyoutput: plot results of one simulation
* plotlyoutputall: plot results of all simulations
"""
# Copyright 2019 Segula Technologies - Agence Française pour la Biodiversité.
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

import os

import plotly.graph_objects as go
import numpy as np


def plotlyoutput(folder):
    """Plot results of one simulation

    Args:
        folder: folder where the output data files are stored.

    Returns:
         An html figure. If observational data (obs.txt) or error statistics
         (err_stats.txt) are available, they are also shown in the figure.
    """

    foutput = os.path.join (folder, 'output.txt')
    fobs = os.path.join(folder, 'obs.txt')
    ferr = os.path.join(folder, 'err_stats.txt')

    #df = pd.read_csv(foutput, sep=' ')
    df = np.genfromtxt(foutput, names=True, dtype=('<M8[D]', float, float))
    # df[0:5]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['tepi'], name="Epilimnion",
                             line_color='deepskyblue', mode='lines'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['thyp'], name="Hypolimnion",
                             line_color='dimgray', mode='lines'))

    if os.path.isfile(fobs):
        dfobs = np.genfromtxt(fobs, names=True,
                              dtype=('<M8[D]', float, float))
        # dfobs[0:5]
        fig.add_trace(go.Scatter(x=dfobs['date'], y=dfobs['tepi'], name="Obs. Epilimnion",
                                 line_color='deepskyblue', mode = 'markers'))
        fig.add_trace(go.Scatter(x=dfobs['date'], y=dfobs['thyp'], name="Obs. Hypolimnion",
                                line_color='dimgray', mode = 'markers'))

    if os.path.isfile(ferr):
        dferr = np.genfromtxt(ferr, names=True)
        # dferr
        rmseE=str(round(dferr['rmse'][0], 1))
        rmseH=str(round(dferr['rmse'][1], 1))
        MyAnnot = [dict(xref='paper',
                        yref='paper',
                        x=0.5, y=1.05,
                        showarrow=False,
                        text ='rmse epilimnion = '+rmseE+'°C / rmse hypolimnion ='+rmseH+'°C')]
    else:
        MyAnnot = []

    fig.update_layout(title_text='Simulated epilimnion and hypolimnion temperatures with okplm package',
                      annotations=MyAnnot,
                      xaxis_rangeslider_visible=True,
                      yaxis={'title': 'Temperature [°C]'},
                      xaxis={'title': 'Time'})
    fig.show()


def plotlyoutputall(folder='examples'):
    """Plot results of several simulations

    Args:
        folder: folder containing the results of the three simulations
        `synthetic_case_daily`, `synthetic_case_weekly` and
        `synthetic_case_monthly`. The results of each simulation is in its
         own folder within "folder".

    Returns:
        An html figure comparing the different simulations. If observational
        data (obs.txt) is available it is also shown in the figure.
    """

    fod = os.path.join(folder, 'synthetic_case_daily','output.txt')
    fow = os.path.join(folder, 'synthetic_case_weekly','output.txt')
    fon = os.path.join(folder, 'synthetic_case_monthly','output.txt')
    fobs = os.path.join(folder, 'synthetic_case_daily', 'obs.txt')

    fig = go.Figure()

    ## Daily
    dfd = np.genfromtxt(fod, names=True,
                              dtype=('<M8[D]', float, float))
    fig.add_trace(go.Scatter(x=dfd['date'], y=dfd['tepi'], name="Daily Epi",
                             line_color='deepskyblue', mode='lines'))
    fig.add_trace(go.Scatter(x=dfd['date'], y=dfd['thyp'], name="Daily Hypo",
                             line_color='dimgray', mode='lines'))
    ## Weekly
    dfw = np.genfromtxt(fow, names=True,
                              dtype=('<M8[D]', float, float))
    fig.add_trace(go.Scatter(x=dfw['date'], y=dfw['tepi'], name="Weekly Epi",
                             line_color='cyan', mode='lines+markers', line_dash='dash')) ##'dash', 'dot', and 'dashdot'
    fig.add_trace(go.Scatter(x=dfw['date'], y=dfw['thyp'], name="Weekly Hypo",
                             line_color='gray', mode='lines+markers', line_dash='dash'))
    ## Monthly
    dfn = np.genfromtxt(fon, names=True,
                              dtype=('<M8[D]', float, float))
    fig.add_trace(go.Scatter(x=dfn['date'], y=dfn['tepi'], name="Monthly Epi",
                             line_color='skyblue', mode='lines+markers', line_dash='dot'))
    fig.add_trace(go.Scatter(x=dfn['date'], y=dfn['thyp'], name="Monthly Hypo",
                             line_color='dimgrey', mode='lines+markers', line_dash='dot'))
    ## Observation
    dfobs = np.genfromtxt(fobs, names=True,
                              dtype=('<M8[D]', float, float))
    fig.add_trace(go.Scatter(x=dfobs['date'], y=dfobs['tepi'], name="Obs. Epilimnion",
                             line_color='blue', mode='markers'))
    fig.add_trace(go.Scatter(x=dfobs['date'], y=dfobs['thyp'], name="Obs. Hypolimnion",
                             line_color='black', mode='markers'))

    fig.update_layout(title_text='Simulated epilimnion and hypolimnion temperatures with okplm package',
                      xaxis_rangeslider_visible=True)

    fig.show()
