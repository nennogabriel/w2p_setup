# -*- coding: utf-8 -*-
### this works on linux  or mac

from gluon.admin import apath
import re
import os
try:
    import fcntl
    import subprocess
    import signal
    import os
    import shutil
    from gluon.fileutils import read_file, write_file
except:
    session.flash = 'sorry, only on Unix systems'
    redirect(URL(request.application, 'default', 'index'))

GAE_APPCFG = os.path.abspath(os.path.join('/usr/local/bin/appcfg.py'))


from gluon.settings import settings
if not settings.is_source:
    session.flash = 'Requires running web2py from source'
    redirect(URL(request.application, 'default', 'index'))

forever = 10 ** 8


def kill():
    p = cache.ram('gae_upload', lambda: None, forever)
    if not p or p.poll() is not None:
        return 'oops'
    os.kill(p.pid, signal.SIGKILL)
    cache.ram('gae_upload', lambda: None, -1)


class EXISTS(object):
    def __init__(self, error_message='file not found'):
        self.error_message = error_message

    def __call__(self, value):
        if os.path.exists(value):
            return (value, None)
        return (value, self.error_message)

@auth.requires(lambda: auth.has_membership('app_admin'))
def index():
    yaml = apath('../app.yaml', r=request)
    if not os.path.exists(yaml):
        example = apath('../app.example.yaml', r=request)
        shutil.copyfile(example, yaml)
    gae_app_name = gae_app_version = '1'
    if not request.vars:
        data = read_file(yaml)
        comp = re.compile('application:(.*)')
        gae_app_name = re.findall(comp,data)[0].strip()
        comp = re.compile('version:(.*)')
        gae_app_version = re.findall(comp,data)[0].strip()

    form = SQLFORM.factory(
        Field('appcfg',
              default=GAE_APPCFG,
              label=T('Path to appcfg.py'),
              requires=EXISTS(error_message=T('file not found'))
              ),
        Field('google_application_id',
              default=gae_app_name,
              requires=IS_MATCH('[\w\-]+'),
              label=T('Google Application Id')
              ),
        Field('version',
              default=gae_app_version,
              requires=IS_NOT_EMPTY(),
              label=T('Version')
              ),
        Field('email',
              default=appconfig.get('google.admin', ''),
              requires=IS_EMAIL(),
              label=T('GAE Email')
              ),
        )
    cmd = output = errors = ""
    if form.accepts(request, session):
        try:
            kill()
        except:
            pass
        data = read_file(yaml)
        data = re.sub('application:.*', 'application: %s' % form.vars.google_application_id, data, 1)
        data = re.sub('version:.*', 'version: %s' % form.vars.version, data, 1)
        write_file(yaml, data)

        path = request.env.applications_parent
        cmd = '%s --email=%s update %s' % \
            (form.vars.appcfg, form.vars.email, path)
        p = cache.ram('gae_upload',
                      lambda s=subprocess, c=cmd: s.Popen(c, shell=True,
                                                          stdin=s.PIPE,
                                                          stdout=s.PIPE,
                                                          stderr=s.PIPE, close_fds=True), -1)
        fcntl.fcntl(p.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(p.stderr.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
    return dict(form=form, command=cmd)


def callback():
    p = cache.ram('gae_upload', lambda: None, forever)
    if not p or p.poll() is not None:
        return '<done/>'
    try:
        output = p.stdout.read()
    except:
        output = ''
    try:
        errors = p.stderr.read()
    except:
        errors = ''
    return (output + errors).replace('\n', '<br/>')
