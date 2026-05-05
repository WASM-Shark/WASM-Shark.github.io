# Configuration file for the Sphinx documentation builder.
# WASMShark — WebAssembly Malware Analyzer

import os
import sys

# -- Project information
project   = 'WASMShark'
copyright = '2025, WASMShark'
author    = 'WASMShark'
release   = '1.0'
version   = '1.0'

# -- General configuration 
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
]

templates_path   = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix    = '.rst'
master_doc       = 'index'
language         = 'en'

# -- Options for HTML output 
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'logo_only':              False,
    'display_version':        True,
    'prev_next_buttons_location': 'both',
    'style_external_links':   True,
    'collapse_navigation':    False,
    'sticky_navigation':      True,
    'navigation_depth':       4,
    'includehidden':          True,
    'titles_only':            False,
    'style_nav_header_background': '#1a1a2e',
}

html_static_path = ['_static']
html_css_files   = ['custom.css']

html_title      = 'WASMShark — WebAssembly Malware Analyzer'
html_short_title = 'WASMShark'

html_context = {
    'display_github': False,
}

# Sidebar
html_sidebars = {
    '**': [
        'globaltoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html',
    ]
}

# -- Todo extension 
todo_include_todos = True

# -- Napoleon settings 
napoleon_google_docstring = True
napoleon_numpy_docstring  = True
napoleon_include_init_with_doc = False

# -- Autodoc settings
autodoc_member_order = 'bysource'
autoclass_content    = 'both'
