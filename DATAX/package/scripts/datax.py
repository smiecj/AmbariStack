# -*- coding: utf-8 -*-
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import format
from resource_management.libraries.functions.check_process_status import check_process_status
from datax_base import DataxBase

class Datax(DataxBase):
    def install(self, env):
        self.install_datax(env)

    def configure(self, env):
        print("no need configure")

    def service_check(self, env):
        import params
        env.set_params(params)
        Execute(format("python {datax_install_path}/bin/datax.py {datax_install_path}/job/job.json"))

if __name__ == "__main__":
    Datax().execute()
