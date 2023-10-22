# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'FOOBARPROJECT'
copyright = '2023, FOOBARAUTHOR'
author = 'FOOBARAUTHOR'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
#exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
templates_path = ['_templates']

# -- Options for HTML output

import sphinx_rtd_theme

html_theme = "sphinx_rtd_theme"
#html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
]
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

#os.system("Rscript -e \"install.packages('irace', repos='https://cloud.r-project.org')\"")


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_build_dir = '$READTHEDOCS_OUTPUT/html/'
autodoc_mock_imports = ["antlr4-python3-runtime", "click", 
                        "cloudpickle", "ConfigSpace", 
                        "dask", "dask-jobqueue", 
                        "dill", "distributed", 
                        "emcee", "exceptiongroup", 
                        "fsspec", "grpcio", 
                        "grpcio-tools", "importlib-metadata", 
                        "iniconfig", "irace", 
                        "Jinja2", "joblib", 
                        "locket", "MarkupSafe", 
                        "more-itertools", "msgpack", 
                        "multipledispatch", "networkx", 
                        "numpy", "packaging", 
                        "pandas", "partd", 
                        "Pebble", "pluggy", 
                        "protobuf", "psutil", 
                        "pynisher", "pyparsing", 
                        "pyperplan", "pyrfr", 
                        "pytamer", "pytest", 
                        "PyYAML", "regex", 
                        "rpy2", "scikit-learn", 
                        "scipy", "smac", 
                        "sortedcontainers", "swig", 
                        "tarski", "tblib", 
                        "threadpoolctl", "tomli", 
                        "toolz", "tornado", 
                        "typing-extensions", "unified-planning", 
                        "up-aries", "up-enhsp", "up-fast-downward", 
                        "up-fmap", "up-lpg", "up-pyperplan", "up-symk", 
                        "up-tamer", "urllib3", "wget", 
                        "wheel", "zict", "zipp"]
#autoapi_dirs = ['up_ac_files/AC_interface']