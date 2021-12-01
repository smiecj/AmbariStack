#!/usr/bin/python
# -*- coding: utf-8 -*-
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import format
from resource_management.core.resources.system import Execute

class NodejsBase(Script):
    def install_node(self, env):
        import params
        env.set_params(params)
        self._install_npm(params)

    def install_packages(self):
        import params
        for component in params.pre_install_node_modules:
            Execute("npm install -g {}".format(component))

    def _install_npm(self, params):
        node_rpm_split_arr = params.node_rpm_url.split("/")   
        node_rpm_name = node_rpm_split_arr[len(node_rpm_split_arr)-1]
        node_rpm_path = format("{tmp_dir}/{node_rpm_name}")

        Execute(format("wget -O {node_rpm_path} {node_rpm_url}"))
        Execute(format("bash - {node_rpm_path} || true"))
        Execute("sudo yum clean all && sudo yum makecache && sudo yum -y remove nodejs && sudo yum -y install nodejs")

        ## set system env
        Execute(format("npm config set prefix '{node_modules_path}/node_global_modules'"))
        Execute(format("npm config set cache '{node_modules_path}/node_cache'"))
        Execute("sudo sed -i 's/.*NODE_REPO.*//g' /etc/profile")
        Execute(format("echo 'export NODE_REPO={node_modules_path}/node_global_modules' | sudo tee -a /etc/profile"))
        Execute(format("echo 'export PATH=$PATH:$NODE_REPO/bin' | sudo tee -a /etc/profile"))