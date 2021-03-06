import os
import yaml
from fabric.api import *

LOCAL_ROOT = os.path.dirname(os.path.abspath(__file__))
#
#
#---------------------- CONFIG --------------------------
stream = open('%s/fabfile.yaml' % LOCAL_ROOT, 'r')
configfile = yaml.load(stream)
stream.close()
for key, value in configfile.items():
    setattr(env, key, value)
#
#
# ------------------- PRODUCTION  ------------------------
def deploy(commit_msg=None):
    """performs the deploy tasks"""
    if commit_msg is not None:
        commit_and_push(commit_msg)
    push_media()
    maintenance()
    update_src()
    # TODO: rsync media
    gunicorn_restart()
    maintenance_end()

@with_settings(warn_only=True)
def commit_and_push(commit_msg):
    local('git add -A')
    local('git commit -a -m "%s"' % commit_msg)
    local('git push origin master')

def maintenance():
    """puts the 503 file to enter production into upgrade mode"""
    put('%(local_templates)s/503.html' % env, '%(remote_media)s' % env)

def update_src():
    """updates source code on production"""
    with cd(env.remote_src):
        run('git pull origin master')

def gunicorn_restart():
    """restarts the guicorn process"""
    run('supervisorctl restart %(supervisorctl_name)s' % env)

@with_settings(warn_only=True)
def maintenance_end():
    """removes the 503 file to exit production from upgrade mode"""
    run('rm %(remote_media)s/503.html' % env)

def nginx_restart():
    """restarts nginx"""
    run('nginx -s reload')

def pip(app):
    """installs a pip app into the virtualenv"""
    with prefix('workon %(remote_virtualenv)s' % env):
        run('pip install -U %s' % app)
        
def mem():
    """returns the memory usage of the account"""
    run('ps -u %(user)s -o pid,rss,command' % env)

def push_media():
    local("rsync -avz %(local_media)s/ -e ssh %(ssh_string)s:%(remote_media)s/" 
            % env)

#
#
# ------------------- DEVLOPMENT--------------------------

def test(apps=""):
    """Clears the screen and runs the tests om the test project"""
    local('clear')
    local('%s/manage.py test %s --setting=jamiecurle.settings.test'\
                 % ( env.local_src, apps))

#
#
# -------------------- OMBLOG
@with_settings(warn_only=True)
def install_production_omblog():
    """installs cccheckout using the version in the requirements file"""
    req = local('cat requirements.txt | grep obscuremetaphor-blog',
                capture=True)
    remove_omblog()
    local('pip install %s' % req)


@with_settings(warn_only=True)
def remove_omblog():
    """removees cccheckout completly"""
    #with hide('stderr', 'warnings', 'stdout'):
    local('pip uninstall obscuremetaphor-blog')
    local('rm -rf %(site_packages)s/omblog' % env)

def edit_dev_omblog():
    """opens cccheckout in TextMate"""
    local('mate %(omblog_project)s' % env)


@with_settings(warn_only=True)
def install_dev_omblog():
    """Installs the development copy of cccheckout"""
    remove_omblog()
    local('ln -s %(omblog_src)s %(site_packages)s/omblog' % env )


