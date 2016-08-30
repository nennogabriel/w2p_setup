# -*- coding: utf-8 -*-

from gluon import DIV

class MDI(DIV):
    tag = 'i'

    def _postprocessing(self):
        if '_class' in self.attributes:
            self.attributes['_class'] = 'material-icons ' + self.attributes['_class']
        else:
            self.attributes['_class'] = 'material-icons '

