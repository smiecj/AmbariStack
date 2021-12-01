#!/usr/bin/python
# -*- coding: utf-8 -*-
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import format
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import File, Execute
import os


class JupyterBase(Script):

    def install_jupyter(self, env):
        import params
        env.set_params(params)
        self._install_jupyter(params)

    def configure_jupyter(self, env):
        import params
        env.set_params(params)
        Execute(format("sudo mkdir -p {jupyterhub_conf_path}"))
        File(format("{jupyterhub_conf_path}/{jupyterhub_conf_name}"),
            content = InlineTemplate(params.jupyterhub_conf_content),
            owner = "root"
        )

    def _install_jupyter(self, params):
        ## There is no need to install python component because conda zip has include all dependencies

        # create share folder
        Execute(format("sudo mkdir -p {juputerhub_share_folder} && sudo chmod 777 {juputerhub_share_folder}"))
