# -*- coding: utf-8 -*-
from gluon import DIV, SPAN, INPUT, I

def formstyle_materialize(form, fields, *args, **kwargs):
    """ divs only """
    if not getattr(form, 'tag', None) == 'form': return DIV(form, fields, *args, **kwargs)
    form['_class'] = form['_class'] or 'col'
    form['_class'] = ' '.join(set(['col', 's12'] + form['_class'].split(' ')))
    table = DIV(_class="row")
    for id, label, controls, help in fields:
        _input_field = DIV(_class="input-field col s12")
        if help:
            _input_field.add_class('tooltipped')
            _input_field['_data-tooltip'] = help
        if getattr(controls, 'tag', None) == 'textarea':
            controls['_class'] += ' materialize-textarea'
        if controls['_type'] == 'file':
            _input_field['_class'] = 'file-field col s12 input-field'
            _input_field.append(
                    DIV(
                        SPAN(label[0]),
                        controls,
                        _class='btn'))
            _input_field.append( DIV(
                    INPUT(
                        _class='file-path  validate',
                        _readonly = '',
                        _type='text'),
                    _class='file-path-wrapper'))
            table.append(_input_field)
            continue
        if controls['_type'] == 'submit':
            controls.tag = 'button'
            controls.components.append(I('send', _class=('material-icons right')))
            controls.components.append(controls['_value'])
            del controls['_value']
            controls['_name'] = 'action'
            controls.add_class('btn right')
        _input_field.append(controls)
        _input_field.append(label)
        table.append(_input_field)
    return table

