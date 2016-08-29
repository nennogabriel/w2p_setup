# -*- coding: utf-8 -*-

from gluon import current, HTTP
try:
    from PIL import Image
except:
    import Image


def optimize_and_cache(db, cache_model=current.cache.disk):
    if not current.request.args: raise HTTP(403)
    if not '.' in current.request.args(-1): raise HTTP(404)
    args = current.request.args(-1).split('.')
    geometry = args[1] if len(args) > 2 else ""
    # options = args[2] if len(args) > 3 else ""

    @current.cache.action(time_expire=60*60*24*7, cache_model=cache_model, quick='')
    def gen_cache_thumb():
        import datetime
        row = db.image_storage(slug=args[0])
        now = datetime.datetime.now()
        created_on = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        expires_on = now + datetime.timedelta(days=7)
        if len(geometry.split('x')) == 2:
            img = Thumbnail(row.url, geometry=geometry, db=db, **current.request.vars).fit_to_size()
        else:
            img = Thumbnail(row.url, geometry=geometry, db=db, **current.request.vars).fit_to_max()
        if not current.request.env.web2py_runtime_gae:
            if args[-1].lower() == 'png':
                img = img.convert('P', dither=0, palette=0, colors=256)
                img.save(current.response.body, args[-1].upper(), optimize=True, bits=8)
            else:
                img.save(current.response.body, args[-1].upper(), optimize=True, quality=78)
            return created_on, expires_on, current.response.body
        else:
            current.response.body = img
            return created_on, expires_on, current.response.body

    created_on, expired_on, img = gen_cache_thumb()

    if created_on == current.request.env.http_if_modified_since: current.response.status = 304

    current.response.headers['Content-Type']="image/" + args[-1].lower()
    current.response.headers['Last-Modified'] = created_on
    current.response.headers['Expires'] = expired_on
    current.response.headers['Pragma'] = current.request.env.http_pragma
    current.response.headers['Cache-Control'] = current.request.env.http_pragma

    # img.save(current.response.body, args[-1].upper())
    current.response.body = img
    if current.request.env.web2py_runtime_gae:
        return current.response.body
    else:
        return current.response.body.getvalue()


class Thumbnail():
    def __init__(self, image_file, geometry=None, db=None, **options):
        if isinstance(image_file, str):
            if current.request.env.web2py_runtime_gae:
                from google.appengine.api import images
                row = db(db.image_storage.url == image_file).select().first()
                image_file = row.url_blob
                self.img = images.Image(image_file)
                self.img.size = [self.img.width, self.img.height]
            else:
                import os
                image_file = os.path.join(current.request.folder, 'uploads/', image_file)
                self.img = Image.open(image_file)
        else:
            self.img = Image.open(image_file)
        self.reductor = Image.ANTIALIAS if self.img.format != 'PNG' else Image.BICUBIC
        width = height = None
        if isinstance(geometry, str):
            if 'x' in geometry:
                w, h = geometry.split('x')
                width = 0 if not w else int(w)
                height = 0 if not h else int(h)
                options['geometry_sting'] = geometry
            else:
                width = height = int(geometry) if geometry else 0
        elif isinstance(geometry, int):
            width = height = geometry
        elif isinstance(geometry, tuple) or isinstance(geometry, list):
            width, height = geometry[:2]
        if not 'geometry_string' in options:
            s = 'x' if width < 1 else '%sx' % width
            s += '' if height < 1 else str(height)
            options['geometry_string'] = s
        self.vars = {
            'width'         : width,
            'height'        : height,
            'crop'          : None,
            'error_message' : 'image file'
        }
        self.vars.update(options)

    def ratio(self):
        return self.img.size[0] / self.img.size[1]

    def fit_to_width(self, width=0, antialias=True):
        if width <= 0 or width > self.img.size[0]: return self.img
        height = width * self.img.size[1] / self.img.size[0]
        if current.request.env.web2py_runtime_gae:
            self.img.resize(width, height, True)
            self.img = self.img.execute_transforms()
            self.img.size = [self.img.width, self.img.height]
        else:
            self.img.thumbnail((width, height), self.reductor)
        return self.img

    def fit_to_height(self, height=0, antialias=True):
        if height <= 0 or height > self.img.size[1]:return self.img
        width = height * self.img.size[0] / self.img.size[1]
        if current.request.env.web2py_runtime_gae:
            self.img.resize(width, height, True)
            self.img = self.img.execute_transforms()
        else:
            self.img.thumbnail((width, height), self.reductor)
        return self.img

    def fit_to_min(self, **kwargs):
        if not self.vars['width']: return self.fit_to_height(self.vars['height'])
        if not self.vars['height']: return self.fit_to_width(self.vars['width'])
        vw = self.img.size[0] / float(self.vars['width'])
        vh = self.img.size[1] / float(self.vars['height'])
        if vw > vh:
            self.fit_to_width(self.vars['width'], **kwargs)
        else:
            self.fit_to_height(self.vars['height'], **kwargs)
        return self.img

    def fit_to_max(self, **kwargs):
        if not self.vars['width']: return self.fit_to_height(self.vars['height'])
        if not self.vars['height']: return self.fit_to_width(self.vars['width'])
        vw = self.img.size[0] / float(self.vars['width'])
        vh = self.img.size[1] / float(self.vars['height'])
        if vw < vh:
            self.fit_to_width(self.vars['width'], **kwargs)
        else:
            self.fit_to_height(self.vars['height'], **kwargs)
        return self.img

    def fit_to_size(self, **kwargs):
        if not self.vars['width']: return self.fit_to_height(self.vars['height'], **kwargs)
        if not self.vars['height']: return self.fit_to_width(self.vars['width'], **kwargs)
        vw = self.img.size[0] / float(self.vars['width'])
        vh = self.img.size[1] / float(self.vars['height'])
        if vw < vh:
            self.fit_to_width(self.vars['width'], antialias=False)
        else:
            self.fit_to_height(self.vars['height'], antialias=False)

        factor = 1
        while self.img.size[0] / factor > 2 * self.vars['width'] and \
              self.img.size[1] * 2 / factor > 2 * self.vars['height']:
            factor *= 2
        if factor > 1:
            width = self.img.size[0] / factor
            height = self.img.size[1] / factor
            if current.request.env.web2py_runtime_gae:
                self.img.resize(width, height, True)
                self.img = self.img.execute_transforms()
                self.img.size = [self.img.width, self.img.height]
            else:
                self.img.thumbnail((width, height), self.reductor)

        #calculate the cropping box and get the cropped part
        x1 = y1 = 0
        x2, y2 = self.img.size
        wRatio = 1.0 * x2 / self.vars['width']
        hRatio = 1.0 * y2 / self.vars['height']
        if hRatio > wRatio:
            y1 = int(y2 / 2 - self.vars['height'] * wRatio / 2)
            y2 = int(y2 / 2 + self.vars['height'] * wRatio / 2)
        else:
            x1 = int(x2 / 2 - self.vars['width'] * hRatio / 2)
            x2 = int(x2 / 2 + self.vars['width'] * hRatio / 2)
        self.img = self.img.crop((x1, y1, x2, y2))
        if current.request.env.web2py_runtime_gae:
            self.img = self.img.execute_transforms()
            self.img.size = [self.img.width, self.img.height]
        else:
            self.img.thumbnail((self.vars['width'], self.vars['height']), self.reductor)
        return self.img


# Validator user in models
# db.image_storage.self.img.requires = RESIZE('x1600')
class RESIZE(object):
    def __init__(self, geometry="x800", **options):
        if not geometry: geometry = ''
        self.vars = {
            'geometry': geometry,

        }
        self.vars.update(options)

    def __call__(self, value):
        if isinstance(value, str) and len(value) == 0:
            return (value, None)
        import cStringIO
        file = Thumbnail(value.file, **self.vars).fit_to_min()
        s = cStringIO.StringIO()
        file.save(s, file.format, optmize=True, quality=90)
        s.seek(0)
        value.file = s
        return (value, None)


from gluon import DIV, URL, DAL

class THUMB(DIV):
    tag = 'img'
    def _postprocessing(self):
        db = img = self.components[0]
        if isinstance(db, DAL):
            img = self.components[1]
            slug = img.split('.')[0]
            row = db.image_storage(slug=slug)
            if not row:
                self.tag = 'span'
                self.components = [img]
                return
            elif row.alt:
                self.attributes['_alt'] = row.alt
        if '//' in img[:10]: self.attributes['_data-src'] = img
        else: self.attributes['_data-src'] = URL('plugin_image_storage', 'thumb', args=img)
        if self.attributes.get('lazy', True):
            self.attributes['_src'] = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEAAAAALAAAAAABAAEAAAI="
        else:
            self.attributes['_src'], self.attributes['_data-src'] = self.attributes['_data-src'], None

        self.components = []
