import sphinx_bootstrap_theme

extensions = []
html_logo = "l.png"
html_favicon = 'favicon.ico'
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': 'white',
    # Toc options
    'navigation_depth': -1,
}
