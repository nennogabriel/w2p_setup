# -*- coding: utf-8 -*-

# from plugin_image_storage import optimize_and_cache

from plugin_image_storage import Thumbnail, optimize_and_cache

def thumb():
    return optimize_and_cache(db, cache_model=cache.ram)


@auth.requires(lambda: auth.has_membership('app_admin'))
def _ah():
    response.view = 'generic.html'
    grid = SQLFORM.smartgrid(db.image_storage)
    return dict(grid=grid)


def ckeditor():
    rows = db(db.image_storage.id > 0).select()
    return locals()