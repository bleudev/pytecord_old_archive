extensions = ["myst_parser"]

myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'dollarmath'
]
myst_heading_anchors = 2

project = 'disspy'
html_logo = "l.png"
html_favicon = 'favicon.ico'
html_theme = 'furo'

html_theme_options = {
    "source_repository": "https://github.com/pixeldeee/disspy",
    "source_branch": "main",
    "source_directory": "docs/",
    "repository_branch": "master"
}

html_static_path = ["_static"]
templates_path = ["_templates"]
