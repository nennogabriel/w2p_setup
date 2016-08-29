# -*- coding: utf-8 -*-

# SEO Site map page colector
db.define_table(
    'sitemap',
    Field('loc', 'string', requires=IS_NOT_EMPTY()),
    Field('lastmod', 'datetime', ),
    Field('changefreq', 'string', default='none',
          requires=IS_IN_SET(('none', 'always', 'hourly', 'daily', 'weekly', 'monthly', 'anual', 'never'))),
    Field('priority', 'string', default='0.5',
          requires=IS_IN_SET(('none', '0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'))),
    Field('translated', 'boolean', default=True),
    Field('active', 'boolean', default=True),
)

if 'addtositemap' in request.vars:
    if request.extension == 'html' and not request.ajax:
        if not (request.controller.startswith('plugin_') or request.function.startswith('_')):
            loc = ','.join(('c:%s' % request.controller, 'f:%s' % request.function))
            if request.args: loc +=',args:%s' % '/'.join(request.args)
            if request.function == 'user': db.sitemap.priority.default = '0.1'
            db.sitemap.update_or_insert(loc=loc)

