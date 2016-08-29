# -*- coding: utf-8 -*-

from validators import IS_EMPTY
from gluon import Field, SQLFORM

def ANTISPAMFORM(table, fieldname='secure_captcha', **kwargs):
    fields = [field for field in table]
    widget = lambda f, v: SQLFORM.widgets.string.widget(f, v, _style='display:none')
    fields.insert(0, Field(fieldname, label='', requires=IS_EMPTY(), widget=widget))
    return SQLFORM.factory(*fields, **kwargs)
