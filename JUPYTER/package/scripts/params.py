# -*- coding: utf-8 -*-
from resource_management import *
from resource_management.libraries.script.script import Script
import os, socket

script_dir = os.path.dirname(os.path.realpath(__file__))
files_dir = os.path.join(os.path.dirname(script_dir), 'files')

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()
stack_name = default("/hostLevelParams/stack_name", None)
stack_version_buildnum = default("/commandParams/version", None)
repo_url = "http://repo_url"
miniconda_pkg_url = repo_url + "/jupyter/miniconda2.zip"
miniconda_install_path = "/home/modules/miniconda2"
if config['configurations']['conda']:
    miniconda_install_path = config['configurations']['conda']['install_path']

conda_jupyter_env_name = "jupyter_env"
python3_ver = "3.8"

ip = config['configurations']['jupyter-hub-server']['bind_ip']
port = config['configurations']['jupyter-hub-server']['bind_port']
authenticator = config['configurations']['jupyter-hub-server']['authenticator']

jupyterhub_inner_port = 8002

jupyterhub_pid_name = "jupyterhub.pid"
jupyter_install_path = "/home/modules/jupyterhub"
jupyterhub_conf_path = jupyter_install_path
jupyterhub_pid_path = jupyter_install_path + "/pid"
jupyterhub_conf_name = "jupyterhub_config.py"

configurable_http_proxy_name = "configurable-http-proxy"

juputerhub_share_folder = config['configurations']['jupyterhub_config.py']['share_code_folder']
allowed_login_users = config['configurations']['jupyterhub_config.py']['allowed_login_users']
dummy_password = config['configurations']['jupyterhub_config.py']['dummy_password']

allowed_users = ''
if "" != allowed_login_users:
    allowed_users = "{'" + {"','".join(allowed_login_users.split(','))} + "'}"

jupyterhub_conf_content = config['configurations']['jupyterhub_config.py']['content']

authenticator = config['configurations']['jupyterhub_config.py']['authenticator']

ldap_server = config['configurations']['jupyterhub_config.py']['ldap_server']
ldap_port = config['configurations']['jupyterhub_config.py']['ldap_port']

ldap_bind_user_dn = config['configurations']['jupyterhub_config.py']['ldap_bind_user_dn']
ldap_user_search_base = config['configurations']['jupyterhub_config.py']['ldap_user_search_base']
ldap_lookup_search_filter = config['configurations']['jupyterhub_config.py']['ldap_lookup_search_filter']
ldap_lookup_attribute = config['configurations']['jupyterhub_config.py']['ldap_lookup_attribute']

ldap_user_attribute = config['configurations']['jupyterhub_config.py']['ldap_user_attribute']
ldap_bind_dn_template = config['configurations']['jupyterhub_config.py']['ldap_bind_dn_template']
ldap_lookup_user = config['configurations']['jupyterhub_config.py']['ldap_lookup_user']
ldap_loopup_password = config['configurations']['jupyterhub_config.py']['ldap_loopup_password']

oauth_tenant_id = config['configurations']['jupyterhub_config.py']['oauth_tenant_id']
oauth_server_address = config['configurations']['jupyterhub_config.py']['oauth_server_address']
oauth_client_id = config['configurations']['jupyterhub_config.py']['oauth_client_id']
oauth_client_secret = config['configurations']['jupyterhub_config.py']['oauth_client_secret']

ssl_key_folder = config['configurations']['jupyterhub_config.py']['ssl_key_folder']
ssl_pem_folder = config['configurations']['jupyterhub_config.py']['ssl_pem_folder']

jupyterhub_spawner_timeout = config['configurations']['jupyterhub_config.py']['jupyterhub_spawner_timeout']

jupyter_user_name = "jupyter"
jupyter_group_name = "jupyter"
jupyter_pwd = "jupyter!qwer"