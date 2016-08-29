# -*- coding: utf-8 -*-

db.define_table(
    'mailmarketing_contact',
    Field('name', 'string', requires=IS_NOT_EMPTY()),
    Field('email', 'string', requires=IS_EMAIL()),
    Field('body', 'text', requires=IS_NOT_EMPTY(), label=T('Message')),
    auth.signature
)

db.define_table(
    'mailmarketing_newsletter',
    Field('name', 'string'),
    Field('email', 'string', requires=IS_EMAIL())
)
