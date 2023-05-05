# -*- coding: utf-8 -*-

from resource_management import InlineTemplate
from resource_management.core.resources.system import Execute, File
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import format, check_process_status

class Broker(Script):
    def install(self, env):
        import params
        env.set_params(params)

        Execute('ps -ef | grep "' + params.starrocks_broker_home + '" | grep -v grep | awk "{print \$2}" | xargs -I {} bash -c "sudo kill -9 {}"')
        Execute(format('sudo mkdir -p {starrocks_broker_home}'))
        Execute(format('cd {starrocks_broker_home} && sudo curl -LO {starrocks_pkg_url} && sudo tar -xzvf {starrocks_pkg} && sudo rm {starrocks_pkg}'))
        Execute(format('cd {starrocks_broker_home} && sudo cp -r {starrocks_pkg_folder}/apache_hdfs_broker/* ./ && sudo rm -r {starrocks_pkg_folder}'))
        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(format('sudo {starrocks_broker_home}/bin/stop_broker.sh || true'))

    def start(self, env):
        self.configure(env)
        import params
        env.set_params(params)

        Execute(format('source /etc/profile && sudo -E {starrocks_broker_home}/bin/start_broker.sh --daemon'))

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        import params
        Execute('sudo chmod 644 {} || true'.format(params.starrocks_broker_pid))
        check_process_status(params.starrocks_broker_pid)

    def configure(self, env):
        import params
        env.set_params(params)

        File(format("{starrocks_broker_conf}"),
            content = InlineTemplate(params.starrocks_broker_content),
            owner = "root"
        )

        Execute(format('sudo cp -f /etc/hadoop/conf/hdfs-site.xml {starrocks_broker_conf_home}'))

if __name__ == '__main__':
    Broker().execute()
