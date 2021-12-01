# -*- coding: utf-8 -*-
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import format
from resource_management.libraries.functions.check_process_status import check_process_status
from jupyter_base import JupyterBase


class JupyterHub(JupyterBase):
    # Call setup.sh to install the service
    def install(self, env):

        # Install packages listed in metainfo.xml
        self.install_jupyter(env)

    def configure(self, env):
        self.configure_jupyter(env)

    # Call start.sh to start the service
    def start(self, env):
        self.configure(env)

        import params
        env.set_params(params)
        Execute('echo "Ready to start jupyterhub"')
        ## run jupyterhub background
        Execute(format("sudo mkdir -p {jupyterhub_pid_path} && username=`whoami` && sudo chown -R $username:$username {jupyter_install_path}"))
        cmd = format("source /etc/profile && cd {jupyter_install_path} && nohup conda run -n {conda_jupyter_env_name} jupyterhub --config {jupyterhub_conf_path}/{jupyterhub_conf_name} > /dev/null 2>&1 &")
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)
        Execute('echo "Start jupyterhub finish"')

    # Called to stop the service using the pidfile
    def stop(self, env):
        import params
        env.set_params(params)
        Execute('echo "Ready to stop jupyterhub"')
        cmd = format("test -e {jupyterhub_pid_path}/{jupyterhub_pid_name} && cat {jupyterhub_pid_path}/jupyterhub.pid | xargs --no-run-if-empty kill -9")
        cmd = format("ps -ef | grep '{conda_jupyter_env_name}'") + " | grep -v grep | awk '{print $2}' | xargs --no-run-if-empty kill -9"
        Execute(cmd)
        cmd = format("ps -ef | grep '{configurable_http_proxy_name}'") + " | grep -v grep | awk '{print $2}' | xargs --no-run-if-empty kill -9"
        Execute(cmd)
        Execute('echo "Stop jupyterhub finish"')

    # Called to get status of the service using the pidfile
    def status(self, env):
        check_process_status("/home/modules/jupyterhub/pid/jupyterhub.pid")

if __name__ == "__main__":
    JupyterHub().execute()
