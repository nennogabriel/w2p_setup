
from gluon import current

def create_default_config():
    import os
    from shutil import copyfile
    origem = os.path.join(current.request.folder, '00_local', 'appconfig.ini')
    destino = os.path.join(current.request.folder, 'private', 'appconfig.ini')
    copyfile(origem, destino)