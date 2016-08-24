# -*- coding: utf-8 -*-

from gluon.tools import Auth as GluonAuth
from gluon.tools import Mail as GluonMail
from gluon import DAL

class Auth(GluonAuth):

    def __init__(self, environment=None, db=None, **kwargs):
        if not db and environment and isinstance(environment, DAL):
            db = environment
        self.db = db
        if not hasattr(kwargs,'hmac_key'): kwargs['hmac_key'] = Auth.get_or_create_key()
        GluonAuth.__init__(self, db=self.db, **kwargs)


class Mail(GluonMail):
    def send_mailgun(self,**kwargs):
        pass
