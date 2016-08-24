# -*- coding: utf-8 -*-
from gluon import DIV, UL, LI, A

class MENU(DIV):
    tag = 'ul'

    def __init__(self, data, menu_name=None, **args):
        self.menu_name = menu_name
        self.data = data
        self.attributes = args
        self.components = []
        if '_class' not in self.attributes:
            self['_class'] = ''
        if 'ul_class' not in self.attributes:
            self['ul_class'] = 'dropdown-content'
        if 'li_class' not in self.attributes:
            self['li_class'] = ''
        if 'li_active' not in self.attributes:
            self['li_active'] = ''
        if 'mobile' not in self.attributes:
            self['mobile'] = False

    def serialize(self, data, level=0, menu_name=None):
        if level == 0:
            ul = UL(**self.attributes)
        elif level == 1 and menu_name :
            ul = UL(_class=self['ul_class'], _id=menu_name)
        else:
            return '' # Navbar works only for 1 level
        for n, item in enumerate(data):
            if isinstance(item, LI):
                ul.append(item)
            else:
                (name, active, link) = item[:3]
                if isinstance(link, DIV):
                    li = LI(link)
                elif 'no_link_url' in self.attributes and self['no_link_url'] == link:
                    li = LI(DIV(name))
                elif isinstance(link, dict):
                    li = LI(A(name, **link))
                elif link:
                    li = LI(A(name, _href=link))
                elif not link and isinstance(name, A):
                    li = LI(name)
                else:
                    li = LI(A(name, _href='#',
                              _onclick='javascript:void(0);return false;'))
                if len(item) > 3 and item[3]:
                    li['_class'] = self['li_class']
                    menu_id = "%s-%s" % (self.menu_name, n)
                    a = li.element('a')
                    a['_class'] = "dropdown-button"
                    a['_data-activates'] = menu_id
                    li.append(self.serialize(item[3], level + 1, menu_id))
                if active or ('active_url' in self.attributes and self['active_url'] == link):
                    if li['_class']:
                        li['_class'] = li['_class'] + ' ' + self['li_active']
                    else:
                        li['_class'] = self['li_active']
                if len(item) <= 4 or item[4] == True:
                    ul.append(li)
        return ul

    def xml(self):
        return self.serialize(self.data, 0).xml()
