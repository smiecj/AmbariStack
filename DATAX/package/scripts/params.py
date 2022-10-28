# -*- coding: utf-8 -*-
from resource_management.libraries.script.script import Script

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
repo_url = "http://repo_url"
datax_pkg_url = repo_url + "/datax/datax.tar.gz"
jsch_new_jar_url = repo_url + "/datax/jsch-0.1.55.jar"
jsch_old_jar = "jsch-0.1.51.jar"
datax_install_path = config['configurations']['datax']['install_path']

# hadoop & hive config
hdfs_site_conf = "/etc/hadoop/conf/hdfs-site.xml"
core_site_conf = "/etc/hadoop/conf/core-site.xml"
hive_site_conf = "/etc/hive/conf/hive-site.xml"