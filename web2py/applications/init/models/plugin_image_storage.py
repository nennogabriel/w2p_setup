# -*- coding: utf-8 -*-

from plugin_image_storage import RESIZE, THUMB

db.define_table(
    'image_storage',
    Field('alt'),
    Field('slug', requires=[IS_SLUG(), IS_NOT_IN_DB(db,'image_storage.slug')]),
    Field('url', 'upload', requires=RESIZE('2800x1600')),
    Field('transparency', 'boolean'),
    Field('tags', 'list:string')
)


