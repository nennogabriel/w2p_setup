# -*- coding: utf-8 -*-

db.define_table(
    'store_product',
    Field('name', 'string', requires=IS_NOT_EMPTY()),
    Field('slug', 'string', requires=IS_SLUG()),
    Field('description', ''),
    Field('avaliable', 'boolean'),
    Field('thumbs', 'list: integer')
)
