# -*- coding: utf-8 -*-


def index():
    response.title += ': ' + response.subtitle
    return {}


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


def sitemap():
    if not request.extension == 'xml' : redirect(URL('sitemap.xml'))
    return {}


@auth.requires_login()
def setup():
    if not db.auth_group(role='app_admin'):
        auth.add_membership(auth.add_group('app_admin'))
    session.flash = "Setup done!"
    return redirect(URL('default', 'index'))


@auth.requires(lambda: auth.has_membership('app_admin'))
def _ah():
    tablename = request.args(0)
    if tablename: grid = SQLFORM.smartgrid(db[tablename])
    else: grid = UL(*[LI(A(t, _href=URL(args=t))) for t in db.tables])
    return dict(grid=grid)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


