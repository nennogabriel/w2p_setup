# -*- coding: utf-8 -*-
### Controler for mailmarketing app ###
# A pieace of Seal Works applications

from plugin_webtools.forms import ANTISPAMFORM

@auth.requires(lambda: auth.has_membership('app_admin'))
def _ah():
    response.view = 'default/_ah.html'
    tablename = request.args(0)
    if tablename: grid = SQLFORM.smartgrid(db[tablename])
    else: grid = UL(*[LI(A(t, _href=URL(args=t))) for t in db.tables if t.startswith('mailmarketing')])
    return dict(grid=grid)


def contact_form():
    form = ANTISPAMFORM(db.mailmarketing_contact)
    if request.post_vars: form.vars.update(request.post_vars)
    form.process()
    if form.accepted:
        message = T('Thank you for write to us. We will answer soon.')
        response.flash = message
        data = db.mailmarketing_contact._filter_fields(form.vars)
        db.mailmarketing_contact.insert(**data)
        html = response.render('plugin_mailmarketing/mail/contact.html', {'data': data})
        txt = response.render('plugin_mailmarketing/mail/contact.txt', {'data': data})
        mail.send(
            to=['sac@agenciadocidadao.com.br'],
            subject=T("[%s] contact from web", (request.env.http_host,)),
            reply_to="%(email)s" % form.vars,
            message=(txt, html)
        )
        return dict(message=message)
    elif form.errors:
        response.flash = T("Something is wrong. Please review the form.")
    return dict(form=form)


def newsletter_form():
    form = ANTISPAMFORM(db.mailmarketing_newsletter)
    if form.process().accepted:
        message = T('Tank you for subscribe. We will send you news soon!')
        response.flash = message
        data = db.mailmarketing_newsletter._filter_fields(form.vars)
        db.mailmarketing_newsletter.update_or_insert(**data)
        return dict(message = message)
    elif form.errors:
        response.flash = T("Something is wrong. Please review the form.")
    return dict(form=form)

