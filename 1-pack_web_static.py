#!/usr/bin/python3
""""""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    if not os.path.exists("version"):
        local('mkdir versions')
    tm = datetime.now()
    f_tm = "%Y%m%d%H%M%S"
    path_archive = 'versions/web_static_{}.tgz'.format(tm.strftime(f_tm))
    local('tar -cvzf {} web_static'.format(path_archive))
    return path_archive
