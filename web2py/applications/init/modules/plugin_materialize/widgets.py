# -*- coding: utf-8 -*-

from gluon.sqlhtml import OptionsWidget, add_class, FormWidget
from gluon import DIV, P, SPAN, INPUT, LABEL

class CheckWidget(OptionsWidget):

    @classmethod
    def widget(cls, field, value, **attributes):
        """
        Simple and best way to do radio boxes and/or checkboxes
        """
        if isinstance(value, (list, tuple)):
            value = str(value[0])
        else:
            value = str(value)

        attr = cls._attributes(field, {}, **attributes)
        attr['_class'] = add_class(attr.get('_class'), 'radio-widget')
        # attr['_class'] = 'row'

        requires = field.requires
        if not isinstance(requires, (list, tuple)):
            requires = [requires]
        if requires:
            if hasattr(requires[0], 'options'):
                options = requires[0].options()
            else:
                raise SyntaxError('widget cannot determine options of %s' % field)
            _type = 'checkbox' if getattr(requires[0], 'multiple') else 'radio'

        options = [(k, v) for k, v in options if str(v)]
        opts = []
        cols = attributes.get('cols', 1)
        totals = len(options)
        mods = totals % cols
        rows = totals / cols
        if mods:
            rows += 1

        parent, child, inner = DIV, DIV, P

        for r_index in range(rows):
            tds = []
            for k, v in options[r_index * cols:(r_index + 1) * cols]:
                checked = {'_checked': 'checked'} if k == value else {}
                tds.append(inner(INPUT(_type = _type,
                                         _id = '%s%s' % (field.name, k),
                                         _name = field.name,
                                         requires = attr.get('requires', None),
                                         hideerror = True, _value = k,
                                         value = value,
                                         **checked),
                                   LABEL(v, _for='%s%s' % (field.name, k)),
                                   _class="col s12 m%s" % (12 / cols)
                                 ))
            opts.append(child(tds, _class='row'))

        if opts:
            opts[-1][0][0]['hideerror'] = False
        if len(opts) == 1:
            opts[0].attributes.update(attr)
            return opts[0]
        return parent(*opts, **attr)

class SwitchWidget(FormWidget):

    @classmethod
    def widget(cls, field, value, **attributes):
        """
        Turn me on. lol! (or off)
        """
        _id = str(field).replace('.', '_')
        attributes['_type'] = 'checkbox'
        return DIV(
            P(
                LABEL(
                    'Off',
                    INPUT(
                        _id = _id,
                        _name = field.name,
                        requires = field.requires,
                        value = value,
                        **attributes
                    ),
                    SPAN(_class='lever'),
                    'On',
                    _for = _id,
                ),
                _style='padding:20px'
            ), _class='switch')


