"""Test run_okp

This script is used to test the function run_okp of the okplm package.

To use this script, first install the okplm following the instructions
included in the README.md file. Then, modify the variable
path_to_repertory_okplm to point to the directory where okplm has been
cloned. You can also modify the averaging period output data by modifying the
variable periodchoice. Then you will be able to run this script's commands
in the Python's console.
"""
import os.path

import okplm


# Choose the simulation periodicity
periodchoice = 'daily'  # 'daily' 'weekly' 'monthly'

# Define folders and file paths
path_to_repertory_okplm = '.'
folder = os.path.join(path_to_repertory_okplm, 'examples',
                      'synthetic_case_' + periodchoice)

output_file = os.path.join(folder, 'output.txt')
meteo_file = os.path.join(folder, 'meteo.txt')
par_file = os.path.join(folder, 'par.txt')
lake_file = os.path.join(folder, 'lake.txt')
validation_data_file = os.path.join(folder, 'obs.txt')
validation_res_file = os.path.join(folder, 'err_stats.txt')

# =============================================================================
# Test 1: input periodicity
# =============================================================================
okplm.run_okp(output_file, meteo_file, par_file, lake_file,
               periodicity=periodchoice)

# =============================================================================
# Test 2: input and output periodicity
# =============================================================================
okplm.run_okp(output_file, meteo_file, par_file, lake_file,
               periodicity=periodchoice,
               output_periodicity='weekly')

# =============================================================================
# Test 3: validation, input periodicity
# =============================================================================
okplm.run_okp(output_file, meteo_file, par_file, lake_file,
               periodicity=periodchoice,
               validation_data_file=validation_data_file,
               validation_res_file=validation_res_file)

# =============================================================================
# Test 4: validation, input and output periodicity
# =============================================================================
okplm.run_okp(output_file, meteo_file, par_file, lake_file,
               periodicity=periodchoice,
               validation_data_file=validation_data_file,
               validation_res_file=validation_res_file,
               output_periodicity='monthly')
