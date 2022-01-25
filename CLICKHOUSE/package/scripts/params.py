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
users_config_file_name = "users_config.xml"
main_config_repo_url = repo_url + "/clickhouse/etc/" + main_config_file_name

user_config_file_path = "/home/modules/clickhouse"
user_config_file_name = "user_config.yml"
user_config_content = config['configurations']['user_config']['content']
main_script_name = "clickhouse.sh"
main_script_relate_path = "./cache/stacks/HDP/2.6/services/CLICKHOUSE/package/scripts"

default_password = config['configurations']['user_config']['default_password']
zookeeper_nodes = config['configurations']['user_config']['zookeeper_nodes']
replica_nodes = config['configurations']['user_config']['replica_nodes']
monitor_port = config['configurations']['user_config']['monitor_port']
data_path = config['configurations']['user_config']['data_path']
tmp_path = config['configurations']['user_config']['tmp_path']

default_database = config['configurations']['user_config']['default_database']
normal_user = config['configurations']['user_config']['normal_user']
normal_user_password = config['configurations']['user_config']['normal_user_password']
normal_user_allow_databases = config['configurations']['user_config']['normal_user_allow_databases']

clickhouse_pid_path = "/run/clickhouse-server/clickhouse-server.pid"