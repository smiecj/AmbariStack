from resource_management import *
from resource_management.libraries.script.script import Script
import os, socket

script_dir = os.path.dirname(os.path.realpath(__file__))
files_dir = os.path.join(os.path.dirname(script_dir), 'files')

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()
stack_name = default("/hostLevelParams/stack_name", None)
stack_version_buildnum = default("/commandParams/version", None)

repo_url = "http://repo_url"

main_config_file_name = "main_config.xml"
main_config_repo_url = repo_url + "/EMR_V1.0/clickhouse/etc/" + main_config_file_name

user_config_file_path = "/opt/modules/clickhouse"
user_config_file_name = "user_config.yml"
user_config_content = config['configurations']['user_config']['content']
main_script_name = "clickhouse.sh"
main_script_relate_path = "./cache/stacks/HDP/2.6/services/CLICKHOUSE/package/scripts"

default_password = config['configurations']['user_config']['default_password']
zookeeper_nodes = config['configurations']['user_config']['zookeeper_nodes']
replica_nodes = config['configurations']['user_config']['replica_nodes']
monitor_port = config['configurations']['user_config']['monitor_port']

clickhouse_pid_path = "/run/clickhouse-server/clickhouse-server.pid"