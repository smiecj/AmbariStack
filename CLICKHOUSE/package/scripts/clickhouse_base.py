#!/usr/bin/python
# -*- coding: utf-8 -*-
from resource_management import *
import os

class ClickhouseBase(Script):

    def init_config(self, env):
        import params
        env.set_params(params)
        ## copy user config file and main config file
        Execute(format("mkdir -p {user_config_file_path}"))
        Execute(format("wget {main_config_repo_url} && mv -f {main_config_file_name} {user_config_file_path}"))
        Execute(format("wget {users_config_repo_url} && mv -f {users_config_file_name} {user_config_file_path}"))
        File(format("{user_config_file_path}/{user_config_file_name}"),
            content = InlineTemplate(params.user_config_content),
            owner = "root"
        )

        ## copy clickhouse.sh
        Execute(format("cp -f {main_script_relate_path}/{main_script_name} {user_config_file_path}"))

    def update_config(self, env):
        import params
        env.set_params(params)
        self.init_config(env)
        Execute(format("sh {user_config_file_path}/clickhouse.sh update_config"))

    def install_package(self, env):
        import params
        env.set_params(params)
        ## Execute clickhouse.sh to install clickhouse
        Execute(format("sh {user_config_file_path}/clickhouse.sh install"))

