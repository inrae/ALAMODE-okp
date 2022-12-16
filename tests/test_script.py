"""Script to test the package okplm.

To use this script, first install the okplm following the instructions
included in the README.md file. Then, modify the variable
path_to_repertory_okplm to point to the directory where okplm has been
cloned. You can also modify the averaging period output data by modifying the
variable periodchoice. Then you will be able to run this script's commands
in the Python's console.
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
import os.path

import okplm
from tests.plotly_functions import plotlyoutput
from tests.plotly_functions import plotlyoutputall

exec(open(os.path.join('okplm', 'plotly_functions.py')).read())

#==========================
# Test 1: Select periodicity
#==========================
periodchoice = 'daily'  # 'daily' 'weekly' 'monthly'

path_to_repertory_okplm = '.'
folder = os.path.join(path_to_repertory_okplm, 'examples',
                      'synthetic_case_' + periodchoice)
output_file = os.path.join(folder, 'output.txt')
meteo_file = os.path.join(folder, 'meteo.txt')
par_file = os.path.join(folder, 'par.txt')   # nonexistent and produced
lake_file = os.path.join(folder, 'lake.txt')
validation_data_file = os.path.join(folder, 'obs.txt')
validation_res_file = os.path.join(folder, 'err_stats.txt')

#==========================
# Test 1-1: Produce two files (par.txt and output.txt) using meteo_file and
# lake_file
#==========================
okplm.run_okp(output_file, meteo_file, par_file, lake_file,
              periodicity=periodchoice)
plotlyoutput(folder)

#==========================
# Test 1-2: Produce two files (par.txt and output.txt) using meteo_file and
# lake_file and use observations to compute validation file err_stats.txt
#==========================
okplm.run_okp(output_file, meteo_file, par_file, lake_file,
              periodicity=periodchoice,
              validation_data_file=validation_data_file,
              validation_res_file=validation_res_file)
plotlyoutput(folder)

#==========================
# Test 2 : Produce one file (output.txt) given a parameter file (par.txt)
#==========================
path_to_repertory_okplm = '.'
folder = os.path.join(path_to_repertory_okplm, 'examples',
                      'synthetic_case_par_given')
output_file = os.path.join(folder, 'output.txt')
meteo_file = os.path.join(folder, 'meteo.txt')
par_file = os.path.join(folder, 'par.txt')
lake_file = os.path.join(folder, 'lake.txt') # nonexistent and produced

# To produce two files : par.txt and output.txt using meteo_file, par_file,
okplm.run_okp(output_file, meteo_file, par_file, lake_file,
              periodicity='daily')
plotlyoutput(folder)


#==========================
# Plot the three tests results
#==========================
plotlyoutputall(folder='examples')