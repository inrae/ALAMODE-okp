# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import os
import sys

from okplm import __version__

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
sys.path.insert(0, os.path.abspath('../../../../okplm'))

# -- Project information -----------------------------------------------------

project = 'okplm_fr'
copyright = '2019, Segula Technologies - Agence Française pour la Biodiversité'
author = 'Jordi Prats-Rodríguez, Pierre-Alain Danis'

# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The master toctree document
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']


# -- Options for LaTex output ------------------------------------------------

# Grouping the document tree into LaTex files. List of tuples
# (source start file, target name, title,
# author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, project + '.tex', 'okplm : Guide d\'Utilisation et Développement',
     'J. PRATS-RODRÍGUEZ \\and P.-A. DANIS', 'manual', True)]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = '../../logos/combined_logo.jpg'

# -- Internationalisation options --------------------------------------------
# Directories in which to search for additional message catalogs, relative to
# the source directory. The directories on this path are searched by the
# standard gettext module.
locale_dirs = ['locale/']

# If true, a document's text domain is a top-level project file and its very
# base directory otherwise.
gettext_compact = False
