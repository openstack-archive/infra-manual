# -*- coding: utf-8 -*-
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import datetime

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'openstackdocstheme'
             ]

todo_include_todos = True

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'OpenDev Manual'
copyright = ('%d, OpenDev Contributors.' % datetime.date.today().year)

# openstackdocstheme options
repository_name = 'opendev/infra-manual'
bug_project = '721'
bug_tag = ''

# These docs are version independent, no need to set version and release.
version = ""
# The full version, including alpha/beta/rc tags.
release = ""

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['infra-manual.']

# -- Options for man page output ----------------------------------------------
man_pages = []

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'openstackdocs'

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = False


# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'Infra-manual.tex', u'Infra Manual',
   u'OpenDev Contributors', 'manual'),
]


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'Infra-manual', u'Infra Manual',
   u'OpenDev Contributors', 'infra-manual', 'OpenDev Manual.',
   'Miscellaneous'),
]


# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = u'OpenDev Manual'
epub_author = u'OpenDev Contributors'
epub_publisher = u'OpenDev Contributors'
epub_copyright = u'%s, OpenDev Contributors' % datetime.date.today().year
