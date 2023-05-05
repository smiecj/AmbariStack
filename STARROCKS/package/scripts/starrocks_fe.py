# -*- coding: utf-8 -*-

from resource_management import InlineTemplate
from resource_management.core.resources.system import Execute, File
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import format, check_process_status

class Frontend(Script):
    def install(self, env):
        import params
        env.set_params(params)

        Execute('ps -ef | grep "' + params.starrocks_fe_home + '" | grep -v grep | awk "{print \$2}" | xargs -I {} bash -c "sudo kill -9 {}"')
        Execute(format('sudo mkdir -p {starrocks_fe_home}'))
        Execute(format('cd {starrocks_fe_home} && sudo curl -LO {starrocks_pkg_url} && sudo tar -xzvf {starrocks_pkg} && sudo rm {starrocks_pkg}'))
        Execute(format('cd {starrocks_fe_home} && sudo cp -r {starrocks_pkg_folder}/fe/* ./ && sudo rm -r {starrocks_pkg_folder}'))
        Execute(format('sudo rm -r {starrocks_fe_meta_path}_bak && mv {starrocks_fe_meta_path} {starrocks_fe_meta_path}_bak || true'))
        Execute(format('sudo mkdir -p {starrocks_fe_meta_path}'))
        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(format('sudo {starrocks_fe_home}/bin/stop_fe.sh'))

    def start(self, env):
        self.configure(env)
        import params
        env.set_params(params)
        
        start_fe_param = ""
        master_host = self.get_fe_master_host()
        if not self.is_master_fe(master_host):
            start_fe_param = start_fe_param + " --helper {}:{}".format(master_host, params.fe_config_properties['starrocks_fe_log_port'])

        Execute(format('source /etc/profile && sudo -E {starrocks_fe_home}/bin/start_fe.sh {start_fe_param} --daemon'))

    # default use min ip as master node
    def get_fe_master_host(self):
        import params
        fe_hosts = params.config['clusterHostInfo']['starrocks_fe_hosts']
        fe_hosts.sort()
        return fe_hosts[0]

    def is_master_fe(self, master_host):
        import socket
        local_host = socket.gethostname()
        return master_host == local_host

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        import params
        Execute('sudo chmod 644 {} || true'.format(params.starrocks_fe_pid))
        check_process_status(params.starrocks_fe_pid)

    def configure(self, env):
        import params
        env.set_params(params)

        File(format("{starrocks_fe_conf}"),
            content = InlineTemplate(params.starrocks_fe_content),
            owner = "root"
        )

if __name__ == '__main__':
    Frontend().execute()
