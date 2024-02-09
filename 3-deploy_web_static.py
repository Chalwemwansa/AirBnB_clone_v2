#!/usr/bin/python3
""" the script that contains the necessary functions for deploying a
    website to a remote server
"""
from fabric.api import local, env, put, run, cd
from datetime import datetime
env.hosts = ['100.26.254.163', '100.24.72.49']


def do_pack():
    """ the function creates a tarball zip file (tgz) from the
        contents of the web_static directory
    """
    env.user = local('whoami', capture=True)
    zip_file_name = datetime.now().strftime("web_static_%Y%m%d%H%M%S")
    target_folder = 'versions'
    source_folder = 'web_static'

    #  ensure the target folder exists and create it if it does not
    local(f'if [ ! -d {target_folder} ]; then\
            mkdir {target_folder};\
            fi')
    #  make the archive file
    local(f'tar -czvf {target_folder}/{zip_file_name}.tgz {source_folder}')

    flag = local(f"if [ -f '{target_folder}/{zip_file_name}.tgz' ]; then\
                  echo 'True'; fi", capture=True)
    if flag:
        return f'{target_folder}/{zip_file_name}.tgz'
    else:
        return False


def do_deploy(archive_path):
    """ function deploys an archive in the versions directory to a server
    """
    archive_name = archive_path.split('/')[-1]
    archive_name_no_extension = archive_name.split('.')[0]
    link = '/data/web_static/current'

    dest_folder = f'/data/web_static/releases/{archive_name_no_extension}'
    flag = local(f"if [ -f {archive_path} ]; then\
                   echo 'True';\
                   fi", capture=True)
    if flag:
        put(archive_path, '/tmp/')
    else:
        return False
    flag = run(f"if [ ! -d {dest_folder} ]; then echo 'True'; fi")
    if flag:
        run(f'mkdir -p {dest_folder}')
    else:
        run(f'rm -rf {dest_folder}')
        run(f'mkdir -p {dest_folder}')
    run(f'tar -xzf /tmp/{archive_name} -C {dest_folder}')
    run(f'rm /tmp/{archive_name}')
    flag = run(f"if [ ! -f {link} ]; then echo 'True'; fi")
    if flag:
        pass
    else:
        run('rm -rf /data/web_static/current')
    run(f'mv {dest_folder}/web_static/* {dest_folder}')
    run(f'rm -rf {dest_folder}/web_static')
    run(f'ln -sf {dest_folder}/ {link}')
    return True


def deploy():
    """deploys a website onto a server, makes an archive and deploys it to
        a server
    """
    path_to_file = do_pack()
    if not path_to_file:
        return False
    val = do_deploy(path_to_file)
    return val
