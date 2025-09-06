# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
#%%
import os
import sys
sys.path.insert(0,os.path.abspath('../../aurelia/aurelia'))
sys.path.insert(0,os.path.abspath('../../aurelia'))

#%%
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'aurelia'
copyright = '2025, MengXing Na, Matteo Michiardi'
author = 'MengXing Na, Matteo Michiardi'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosectionlabel',
]




# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = "Aurelia — MengXing Na"
html_short_title = "Aurelia"

# Add meta tags for SEO
html_context = {
    "description": "Aurelia — Python library for ARPES simulations and machine-learning analysis, developed by MengXing Na and Matteo Michiardi",
    "keywords": "MengXing Na, Aurelia, ARPES, simulation, machine-learning",
}
# Ensure search index works
html_search_language = "en"
html_theme_options = {
	'collapse_navigation':True,
    'logo_only':True
}

html_logo = 'images/aurelia_logo.png'