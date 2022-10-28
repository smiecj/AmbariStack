#!/usr/bin/python
# -*- coding: utf-8 -*-
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import format
from resource_management.core.resources.system import Execute

class DataxBase(Script):
    def install_datax(self, env):
        import params
        env.set_params(params)
        self._install_datax(params)

    def _install_datax(self, params):
        datax_url_split_arr = params.datax_pkg_url.split("/")
        datax_pkg_name = datax_url_split_arr[len(datax_url_split_arr)-1]
        datax_pkg_tmp_full_path = format("{tmp_dir}/{datax_pkg_name}")
        
        datax_install_path_split_arr = params.datax_install_path.split("/")
        datax_install_parent_path = "/".join(datax_install_path_split_arr[0:len(datax_install_path_split_arr)-1])

        Execute(format("cd {tmp_dir} && sudo rm -f {datax_pkg_name} && sudo wget {datax_pkg_url}"))
        Execute(format("sudo rm -rf {datax_install_path} && cd {datax_install_parent_path} && sudo mv {datax_pkg_tmp_full_path} ./ && sudo tar -xzvf {datax_pkg_name}"))
        # fix: sftp: connect failed
        # refer: https://github.com/is/jsch/issues/2
        Execute(format("cd {datax_install_parent_path}/datax/plugin/reader/ftpreader/libs && sudo rm -f {jsch_old_jar} && sudo wget {jsch_new_jar_url}"))
        self._input_hadoop_config_to_hdfs_jar(self, params)

    def _input_hadoop_config_to_hdfs_jar(self, params):
        from os.path import exists

        # support namenode ha
        # https://github.com/alibaba/DataX/issues/197#issuecomment-436843464
        if exists(params.hdfs_site_conf):
            Execute(format("cd {datax_install_path}/plugin/reader/hdfsreader/ && unzip hdfsreader-0.0.1-SNAPSHOT.jar -d hdfsreader && " + 
                "cd hdfsreader/ && cp {hdfs_site_conf} ./ && cp {core_site_conf} ./ && cp {hive_site_conf} ./ && " + 
                "jar -cvf hdfsreader-0.0.1-SNAPSHOT.jar . && mv hdfsreader-0.0.1-SNAPSHOT.jar ../ && cd .. && rm -rf hdfsreader"))
            Execute(format("cd {datax_install_path}/plugin/writer/hdfswriter/ && unzip hdfswriter-0.0.1-SNAPSHOT.jar -d hdfswriter && " + 
                "cd hdfswriter/ && cp {hdfs_site_conf} ./ && cp {core_site_conf} ./ && cp {hive_site_conf} ./ && " + 
                "jar -cvf hdfswriter-0.0.1-SNAPSHOT.jar . && mv hdfswriter-0.0.1-SNAPSHOT.jar ../ && cd .. && rm -rf hdfswriter"))