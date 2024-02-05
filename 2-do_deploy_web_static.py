#!/usr/bin/python3
""" the script that contains the necessary functions for deploying a
    website to a remote server
"""
from fabric.api import env, put, run
from os.path import exists
env.hosts = ['100.26.254.163', '100.24.72.49']


def do_deploy(archive_path):
    """ function deploys an archive in the versions directory to a server
    """
    if exists(archive_path) is False:
        return False
    try:
        archive_name = archive_path.split('/')[-1]
        archive_name_no_extension = archive_name.split('.')[0]
        link = '/data/web_static/current'
        dest_folder = f'/data/web_static/releases/{archive_name_no_extension}'

        put(archive_path, '/tmp/')
        run(f'mkdir -p {dest_folder}/')
        run(f'tar -xzf /tmp/{archive_name} -C {dest_folder}')
        run(f'rm /tmp/{archive_name}')
        run(f'mv {dest_folder}/web_static/* {dest_folder}')
        run(f'rm -rf {dest_folder}/web_static/')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {dest_folder}/ {link}')
        return True
    except Exception:
        return False
