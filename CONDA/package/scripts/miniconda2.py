# -*- coding: utf-8 -*-
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import format
from resource_management.libraries.functions.check_process_status import check_process_status
from conda_base import CondaBase

class Miniconda2(CondaBase):
    def install(self, env):
        self.install_conda(env)

    def configure(self, env):
        print("no need configure")

    def service_check(self, env):
        import params
        env.set_params(params)
        ## test install pytz plugin to verify conda
        Execute(format("conda install -y -n {conda_jupyter_env_name} pytz"))

if __name__ == "__main__":
    Miniconda2().execute()
