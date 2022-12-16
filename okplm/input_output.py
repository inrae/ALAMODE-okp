"""Functions to read and write data.

The functions in this module are used to read the configuration and input data
files of the OKP lake model, as well as for writing the results to a text file.

This module contains the following functions:

    * read_dict: read lake or parameter file to dictionary.
    * write_dict: write dictionary to file.

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


def read_dict(path):
    """Read lake or parameter file to dictionary.

    Args:
        path: path of text file. The file should be structured in two columns
            separated by a space; the first column contains key names and the
            second column contains their values.

    Returns:
        A Python dictionary created from the key-value pairs in the text file.
    """
    # Read file
    with open(path, 'rt') as f:
        file_content = f.readlines()

    # Construct output dictionary
    output = dict()
    for l in file_content:
        k, v = l.split()
        try:
            # Convert from string to float whenever possible
            v = float(v)
        except ValueError:
            pass
        output.update({k: v})

    return output


def write_dict(x_dict, path):
    """Write dictionary to file.

    Args:
        x_dict: a Python dictionary.
        path: path of the text file to write the data.

    Returns:
        A file located at "path" where the dictionary data is written.
    """
    with open(path, 'wt') as f:
        for k, v in x_dict.items():
            f.write(k + ' ' + str(v) + '\n')
    return
