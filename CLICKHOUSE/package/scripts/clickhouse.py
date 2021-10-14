# -*- coding: utf-8 -*-
from resource_management import *
from clickhouse_base import ClickhouseBase


class Clickhouse(ClickhouseBase):
    def install(self, env):

        # Install packages listed in metainfo.xml
        print("[debug] env: {}".format(env))
        self.configure(env)
        self.install_package(env)

    def configure(self, env):
        self.update_config(env)

    def start(self, env):
        self.configure(env)

        import params
        env.set_params(params)
        Execute('echo "Ready to start Clickhouse"')
        Execute("systemctl restart clickhouse-server")
        Execute('echo "Start clickhouse finish"')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('echo "Ready to stop Clickhouse"')
        Execute("systemctl stop clickhouse-server")
        Execute('echo "Stop Clickhouse finish"')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(format("{clickhouse_pid_path}"))

if __name__ == "__main__":
    Clickhouse().execute()
