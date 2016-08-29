# -*- coding: utf-8 -*-

# from gluon import current

# T = current.T

class IS_EMPTY(object):

    def __init__(self, error_message="This field must be empty"):
        self.error_message = error_message

    def __call__(self, value):
      if value != "": return (value, self.error_message)
      return (value, None)

