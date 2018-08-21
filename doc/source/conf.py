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
project = u'OpenStack Project Infrastructure Manual'
copyright = ('%d, OpenStack Contributors.' % datetime.date.today().year)

# openstackdocstheme options
repository_name = 'openstack-infra/infra-manual'
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

# To use the API Reference sidebar dropdown menu,
# uncomment the html_theme_options parameter.  The theme
# variable, sidebar_dropdown, should be set to `api_ref`.
# Otherwise, the list of links for the User and Ops docs
# appear in the sidebar dropdown menu.
html_theme_options = {
    "display_badge": False
}

# Must set this variable to include year, month, day, hours, and minutes.
html_last_updated_fmt = '%Y-%m-%d %H:%M'

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = False


# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'Infra-manual.tex', u'Infra Manual',
   u'OpenStack Contributors', 'manual'),
]


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'Infra-manual', u'Infra Manual',
   u'OpenStack Contributors', 'infra-manual', 'OpenStack Project Infrastructure Manual.',
   'Miscellaneous'),
]


# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = u'OpenStack Project Infrastructure Manual'
epub_author = u'OpenStack Contributors'
epub_publisher = u'OpenStack Contributors'
epub_copyright = u'%s, OpenStack Contributors' % datetime.date.today().year
