extensions = [
    "myst_parser",
    "sphinx.ext.autodoc"
]

myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'dollarmath'
]
myst_heading_anchors = 2

project = 'pytecord'
html_logo = "l.png"
html_favicon = 'favicon.ico'
html_theme = 'furo'

html_theme_options = {
    "source_repository": "https://github.com/pixeldeee/pytecord",
    "source_branch": "master",
    "source_directory": "docs/source",
    "repository_branch": "master"
}

html_static_path = ["_static"]
templates_path = ["_templates"]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
