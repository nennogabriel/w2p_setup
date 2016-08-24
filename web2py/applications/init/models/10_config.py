# -*- coding: utf-8 -*-

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

from gluon.contrib.appconfig import AppConfig
appconfig = AppConfig(reload=True)

if request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb', lazy_tables=True)
    # ---------------------------------------------------------------------
    # store sessions and tickets in Memcache
    # ---------------------------------------------------------------------
    from gluon.contrib.gae_memcache import MemcacheClient
    from gluon.contrib.memdb import MEMDB
    cache.memcache = MemcacheClient(request)
    cache.ram = cache.disk = cache.memcache
    session.connect(request, response, db=MEMDB(cache.memcache.client))
else:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(appconfig.get('db.uri'),
             pool_size=appconfig.get('db.pool_site'),
             migrate_enabled=appconfig.get('db.migrate'),
             check_reserved=appconfig.get('db.migrate') and ['all'] or None,
             lazy_tables=True)

from extended.tools import Mail, Auth
from gluon.tools import Service, PluginManager

mail = Mail()
mail.settings.server = 'logging' if request.is_local else appconfig.get('smtp.server')
mail.settings.sender = appconfig.get('mailer.sender')
mail.settings.login = appconfig.get('mailer.login')
mail.settings.tls = appconfig.get('smtp.tls') or False
mail.settings.ssl = appconfig.get('smtp.ssl') or False

auth = Auth(db, host_names=appconfig.get('auth.host_names'))
auth.settings.mailer = mail
auth.define_tables(username=False, signature=False)
auth.settings.registration_requires_verification = not request.is_local
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = not request.is_local

if request.uri_language: T.force(request.uri_language)

# -------------------------------------------------------------------------
# Load Plugins
# -------------------------------------------------------------------------

from plugin_materialize import *
response.formstyle = formstyle_materialize
auth.settings.formstyle = formstyle_materialize