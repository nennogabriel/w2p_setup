# -*- coding: utf-8 -*-
routers = dict(
    # base router
    BASE=dict(
        default_application='init',
        # domains = {},
    ),
)



routes_onerror = [
    # (r'*/*', '/init/plugin_error_handler'),
    (r'*/403', r'/init/static/403.html'),
    (r'*/404', r'/init/static/404.html'),
    (r'*/500', r'/init/static/500.html')
]


