# -*- coding: utf-8 -*-
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import format
from resource_management.libraries.functions.check_process_status import check_process_status
from nodejs_base import NodejsBase

class Nodejs(NodejsBase):
    def install(self, env):
        self.install_node(env)
        self.install_packages()

    def configure(self, env):
        self.install_packages()

    def service_check(self, env):
        import params
        env.set_params(params)
        Execute("npm -v")
        Execute("node -v")

if __name__ == "__main__":
    Nodejs().execute()
