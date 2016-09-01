# -*- coding: utf-8 -*-

def STATIC(*args, **kwargs):
    kwargs['language'] = "en"
    return URL('static', *args, **kwargs)