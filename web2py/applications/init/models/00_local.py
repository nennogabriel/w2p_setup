# -*- coding: utf-8 -*-

## do not deploy this file and any other 00_local folder or file

if not request.env.web2py_runtime_gae:
    from gluon.custom_import import track_changes
    track_changes(True)

response.livereload = XML("<script src=\"http://127.0.0.1:35729/livereload.js?snipver=1\"></script>")