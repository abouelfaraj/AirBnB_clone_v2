#!/usr/bin/python3
"""Module distributes an archive to server web-01 and web-02"""

from datetime import datetime
from fabric.api import *
from os.path import exists, isdir


env.hosts = ['34.207.155.207', '18.206.208.206']


def do_pack():
    """Creates archive tgz"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("sudo mkdir versions")
        filename = "versions/web_static_{}.tgz".format(date)
        local("sudo tar -cvzf {} web_static".format(filename))
        return filename
    except:
        return None


def do_deploy(archive_path):
    """Fabric script that distributes an archive to server web-01 and web-02"""
    if exists(archive_path) is False:
        return False
    try:
        name = archive_path.split("/")[-1]
        name_i = name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}{}/".format(path, name_i))
        run("sudo tar -xzf /tmp/{} -C {}{}/".format(name, path, name_i))
        run("sudo rm /tmp/{}".format(name))
        run("sudo mv {0}{1}/web_static/* {0}{1}/".format(path, name_i))
        run("sudo rm -rf {}{}/web_static".format(path, name_i))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}{}/ /data/web_static/current".format(path, name_i))
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to the web"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
