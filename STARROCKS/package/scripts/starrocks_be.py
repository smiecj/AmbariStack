# -*- coding: utf-8 -*-

from resource_management import InlineTemplate
from resource_management.core.resources.system import Execute, File
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import format, check_process_status

## 当前: 写到这里
class Backend(Script):
    def install(self, env):
        import params
        env.set_params(params)

        Execute('ps -ef | grep "' + params.starrocks_be_home + '" | grep -v grep | awk "{print \$2}" | xargs -I {} bash -c "sudo kill -9 {}"')
        Execute(format('sudo mkdir -p {starrocks_be_home}'))
        Execute(format('cd {starrocks_be_home} && sudo curl -LO {starrocks_pkg_url} && sudo tar -xzvf {starrocks_pkg} && sudo rm {starrocks_pkg}'))
        Execute(format('cd {starrocks_be_home} && sudo cp -r {starrocks_pkg_folder}/be/* ./ && sudo rm -r {starrocks_pkg_folder}'))
        Execute(format('sudo rm -r {starrocks_be_storage_path}_bak && mv {starrocks_be_storage_path} {starrocks_be_storage_path}_bak || true'))
        Execute(format('sudo mkdir -p {starrocks_be_storage_path}'))
        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(format('sudo {starrocks_be_home}/bin/stop_be.sh'))

    def start(self, env):
        self.configure(env)
        import params
        env.set_params(params)
        Execute(format('source /etc/profile && sudo -E {starrocks_be_home}/bin/start_be.sh --daemon'))

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        import params
        print("[test] to print all configs: {}".format(params.config))
        Execute('sudo chmod 644 {} || true'.format(params.starrocks_be_pid))
        check_process_status(params.starrocks_be_pid)

    def configure(self, env):
        import params
        env.set_params(params)

        File(format("{starrocks_be_conf}"),
            content = InlineTemplate(params.starrocks_be_content),
            owner = "root"
        )

if __name__ == '__main__':
    Backend().execute()
