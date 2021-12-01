#!/usr/bin/python
# -*- coding: utf-8 -*-
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import format
from resource_management.core.resources.system import Execute

class CondaBase(Script):
    def install_conda(self, env):
        import params
        env.set_params(params)
        self._install_conda(params)

    def _install_conda(self, params):
        import os
        conda_url_split_arr = params.miniconda_pkg_url.split("/")
        conda_pkg_name = conda_url_split_arr[len(conda_url_split_arr)-1]
        conda_pkg_full_path = format("{tmp_dir}/{conda_pkg_name}")

        conda_install_path_split_arr = params.miniconda_install_path.split("/")
        conda_install_parent_path = "/".join(conda_install_path_split_arr[0:len(conda_install_path_split_arr)-1])

        ## Download moniconda and install it
        Execute(format("cd {tmp_dir} && rm -f {conda_pkg_name} && wget {miniconda_pkg_url}"))
        if not os.path.isdir(format("{miniconda_install_path}")):
            Execute(format("rm -rf {miniconda_install_path}"))
            Execute(format("cd {conda_install_parent_path} && mv {tmp_dir}/{conda_pkg_name} . && unzip {conda_pkg_name}"))
            Execute(format("cd {conda_install_parent_path} && rm -f {conda_pkg_name}"))
            ## remove old conda environment
            Execute("sudo sed -i 's/.*conda.*//g' /etc/profile")
            Execute("sudo sed -i 's/.*CONDA.*//g' /etc/profile")
            ## put new profile in the end
            ### olea: use tee to append content
            Execute(format("echo 'export CONDA_HOME={miniconda_install_path}' | sudo tee -a /etc/profile"))
            Execute(format("echo 'export PATH=$PATH:$CONDA_HOME/bin' | sudo tee -a /etc/profile"))
            ### olea: conda must install in /home/modules , need to replace python file prefix old install path to new install path
            old_install_path = "/usr/local/miniconda2"
            replace_old_install_path = old_install_path.replace("/", "\/")
            replace_miniconda_install_path = params.miniconda_install_path.replace("/", "\/")
            Execute(format("find {miniconda_install_path} -name '*' | xargs grep '{old_install_path}'") + " | grep -v 'Binary' | awk -F':{1,}' '{print $1}' | xargs -I {}" + format(" sudo sed -i 's/{replace_old_install_path}/{replace_miniconda_install_path}/g' ") + "{}")

        Execute("source /etc/profile && conda update conda")
        Execute("source /etc/profile && conda config --set auto_activate_base false")
        Execute("source /etc/profile && conda init || true")
        Execute("source /etc/profile && conda clean -y --all || true")
