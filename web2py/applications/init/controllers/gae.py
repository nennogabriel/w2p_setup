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
    regex = re.compile('^\w+$')
    apps = sorted(
        file for file in os.listdir(apath(r=request)) if regex.match(file))
    form = SQLFORM.factory(
        Field('appcfg',
              default=GAE_APPCFG,
              label=T('Path to appcfg.py'),
              requires=EXISTS(error_message=T('file not found'))
              ),
        Field('google_application_id',

              requires=IS_MATCH('[\w\-]+'),
              label=T('Google Application Id')
              ),
        Field('applications', 'list:string',
              requires=IS_IN_SET(apps, multiple=True),
              label=T('web2py apps to deploy')),
        Field('email', requires=IS_EMAIL(), label=T('GAE Email')),
        )
    cmd = output = errors = ""
    if form.accepts(request, session):
        try:
            kill()
        except:
            pass
        ignore_apps = [item for item in apps
                       if not item in form.vars.applications]
        regex = re.compile('\(applications/\(.*')

        yaml = apath('../app.yaml', r=request)
        if not os.path.exists(yaml):
            example = apath('../app.example.yaml', r=request)
            shutil.copyfile(example, yaml)

        data = read_file(yaml)
        data = re.sub('application:.*', 'application: %s' %
                      form.vars.google_application_id, data)
        data = regex.sub(
            '(applications/(%s)/.*)|' % '|'.join(ignore_apps), data)
        write_file(yaml, data)

        path = request.env.applications_parent
        cmd = '%s --email=%s update %s' % \
            (form.vars.appcfg, form.vars.email, path)
        p = cache.ram('gae_upload',
                      lambda s=subprocess, c=cmd: s.Popen(c, shell=True,
                                                          stdin=s.PIPE,
                                                          stdout=s.PIPE,
                                                          stderr=s.PIPE, close_fds=True), -1)
        # p.stdin.write(form.vars.password + '\n')
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
