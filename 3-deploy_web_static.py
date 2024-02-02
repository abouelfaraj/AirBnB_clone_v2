#!/usr/bin/python3
"""Module distributes an archive to server web-01 and web-02"""

from datetime import datetime
from fabric.api import *
import shlex
import os


env.hosts = ['34.207.155.207', '18.206.208.206']


def do_pack():
    """Creates archive tgz"""
    try:
        date = datetime.now().strftime("")
        if isdir("versions") is False:
            local("mkdir versions")
        filename = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except:
        return None


def do_deploy(archive_path):
    """Fabric script that distributes an archive to server web-01 and web-02"""
    if not os.path.exists(archive_path):
        return False
    try:
        name = archive_path.split("/")[-1]
        name_inex = name.split(".")[0]
        path = "/data/web_static/releases/"
        
        put(archive_path, "/tmp/")
        run("mkdir -p {}{}/".format(path, name_inex))
        run("tar -xzf /tmp/{} -C {}{}/".format(name, path, name_inex))
        run("rm /tmp/{}".format(name))
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, name_inex))
        run("rm -rf {}{}/web_static".format(path, name_inex))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(path, name_inex))
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to the web"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
