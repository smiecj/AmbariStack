# -*- coding: utf-8 -*-
from resource_management.libraries.script.script import Script
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
files_dir = os.path.join(os.path.dirname(script_dir), 'files')

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
repo_url = "http://repo_url"

node_rpm_url = repo_url + "/jupyter/node_setup_16.x"
node_modules_path = config['configurations']['npm_nodejs']['node_modules_path']
pre_install_node_modules = config['configurations']['npm_nodejs']['pre_install_node_modules'].replace(" ", "").split("\n")