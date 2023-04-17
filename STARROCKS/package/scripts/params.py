#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource_management.libraries.script.script import Script
config = Script.get_config()

repo_url = "http://repo_url"
starrocks_version = "2.5.3"
starrocks_pkg_folder = "StarRocks-" + starrocks_version
starrocks_pkg = starrocks_pkg_folder + ".tar.gz"

starrocks_pkg_url = repo_url + "/starrocks/" + starrocks_pkg
starrocks_module_home = "/opt/modules/starrocks"
starrocks_pkg_home = starrocks_module_home + "/" + starrocks_pkg_folder
starrocks_fe_home = starrocks_pkg_home + "/fe"
starrocks_be_home = starrocks_pkg_home + "/be"
starrocks_fe_pid = starrocks_fe_home + "/bin/fe.pid"
starrocks_be_pid = starrocks_be_home + "/bin/be.pid"
starrocks_fe_conf = starrocks_fe_home + "/conf/fe.conf"
starrocks_be_conf = starrocks_be_home + "/conf/be.conf"

# load config
fe_config_properties = config['configurations']['starrocks.fe.conf']
be_config_properties = config['configurations']['starrocks.be.conf']

## config to replace
starrocks_fe_content = fe_config_properties['content']
starrocks_fe_http_port = fe_config_properties['starrocks_fe_http_port']
starrocks_fe_rpc_port = fe_config_properties['starrocks_fe_rpc_port']
starrocks_fe_query_port = fe_config_properties['starrocks_fe_query_port']
starrocks_fe_log_port = fe_config_properties['starrocks_fe_log_port']
starrocks_fe_meta_path = fe_config_properties['starrocks_fe_meta_path']

starrocks_be_content = be_config_properties['content']
starrocks_be_port = be_config_properties['starrocks_be_port']
starrocks_be_webserver_port = be_config_properties['starrocks_be_webserver_port']
starrocks_be_heartbeat_port = be_config_properties['starrocks_be_heartbeat_port']
starrocks_be_brpc_port = be_config_properties['starrocks_be_brpc_port']
starrocks_be_storage_path = be_config_properties['starrocks_be_storage_path']

starrocks_config_home = '/etc/starrocks'
starrocks_fe_config_directory = '/etc/starrocks/fe'
starrocks_be_config_directory = '/etc/starrocks/be'
