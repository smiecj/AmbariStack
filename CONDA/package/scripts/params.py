# -*- coding: utf-8 -*-
from resource_management.libraries.script.script import Script
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
files_dir = os.path.join(os.path.dirname(script_dir), 'files')

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
repo_url = "http://repo_url"
miniconda_pkg_url = repo_url + "/jupyter/miniconda2.zip"
miniconda_install_path = config['configurations']['conda']['install_path']

conda_jupyter_env_name = "jupyter_env"