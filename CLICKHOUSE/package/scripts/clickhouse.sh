#!/bin/bash
## a shell for install or update clickhouse config
### update: sh clickhouse.sh update
### install: sh clickhouse.sh install
### rely: user_config.yml which store custom configuration

## env prepare
home=/home/modules/clickhouse
main_config_file="main_config.xml"
user_config_file="user_config.yml"
users_config_file="users_config.xml"
clickhouse_config_path="/etc/clickhouse-server"
clickhouse_data_home_path="/opt/clickhouse"
clickhouse_pid_path="/var/run/clickhouse-server"
clickhouse_pid_full_path="/run/clickhouse-server/clickhouse-server.pid"

zk_nodes_key="zookeeper_nodes"
default_zk_port="2181"
replica_nodes_key="replica_nodes"
clickhouse_default_username="default"
clickhouse_default_password_key="default_password"
clickhouse_default_port="9000"
clickhouse_default_database="db"
clickhouse_default_database_key="default_database"

repo_url_key="repo_url"
monitor_port_key="monitor_port"
data_path_key="data_path_key"
tmp_path_key="tmp_path_key"

normal_user_key="normal_user"
normal_user_password_key="normal_user_password"
normal_user_allow_databases_key="normal_user_allow_databases"

cluster_name="my_cluster"

mkdir -p $home
pushd $home

## get current node hostname by /etc/hosts
get_hostname() {
    local local_ip=`ifconfig | grep -A 1 ens160 | sed -n '2p' | awk -F' {1,}' '{print $3}'`
    if [[ -z $local_ip ]]; then
        local_ip=`ifconfig | grep -A 1 eth0 | sed -n '2p' | awk -F' {1,}' '{print $3}'`
    fi
    if [[ -z $local_ip ]]; then
        echo "[ERROR] get local ip failed"
        exit
    fi

    local host_list=(`cat /etc/hosts | grep -e task -e core -e common -e router | awk -F' {1,}' '{print $3}'`)
    local ip_list=(`cat /etc/hosts | grep -e task -e core -e common -e router | awk -F' {1,}' '{print $1}'`)

    local local_host=""
    for i in ${!ip_list[@]};
    do
    if [ ${ip_list[$i]} == $local_ip ]; then
        local_host=${host_list[$i]}
    fi
    done
    echo "$local_host"
}

declare -A config_map
declare -A config_update_func_map

## get config: recur every line in user config and get config content, prepare for update config
get_config() {
    while read line
    do
        if [[ $line == *" = "* ]]; then
            config_key=`echo $line | awk -F' = {1,}' '{print $1}'`
            config_value=`echo $line | awk -F' = {1,}' '{print $2}'`
            config_map[$config_key]=$config_value
        fi
    done < $user_config_file
}

## update config: execute every update config function
update_config() {
    config_update_func_map["$zk_nodes_key"]=update_zookeeper_nodes_config
    config_update_func_map["$replica_nodes_key"]=update_replica_nodes_config
    config_update_func_map["$monitor_port_key"]=update_monitor_port_config
    config_update_func_map["$data_path_key"]=update_data_path_config
    config_update_func_map["$tmp_path_key"]=update_tmp_path_config

    config_update_func_map["$clickhouse_default_database_key"]=update_default_database

    config_update_func_map["$normal_user_key"]=update_normal_user
    config_update_func_map["$normal_user_password_key"]=update_normal_user_password
    config_update_func_map["$normal_user_allow_databases_key"]=update_normal_user_allow_databases

    ### set config with order
    config_key_arr=("$zk_nodes_key" "$clickhouse_default_database_key" "$replica_nodes_key" "$monitor_port_key" \
        "$data_path_key" "$tmp_path_key" "$normal_user_key" "$normal_user_password_key" "$normal_user_allow_databases_key")
    for config_key in ${config_key_arr[@]}
    do
        if [ -n "${config_update_func_map[${config_key}]:-}" ]; then
            ${config_update_func_map[${config_key}]} ${config_map[${config_key}]}
        fi
    done

    ### move current config to clickhouse server config folder
    #### the origin config file usually come from file server (refer clickhouse_base.py)
    mkdir -p $clickhouse_config_path
    cp -f $main_config_file $clickhouse_config_path/config.xml
    cp -f $users_config_file $clickhouse_config_path/users.xml
}

## replace zookeeper nodes config
update_zookeeper_nodes_config() {
    ### zookeeper config
    zookeeper_node_list_str=$1
    zk_address_list=($(echo $zookeeper_node_list_str | tr "," "\n" | sort | uniq))
    space_4="    "
    zk_replace_str="<zookeeper>"
    for zk_address in ${zk_address_list[@]}
    do
        IFS=':' read -r -a zk_split_list <<< $zk_address
        zk_host=${zk_split_list[0]}
        zk_port=${zk_split_list[1]}
        if [ -z $zk_port ]; then
            zk_port=$default_zk_port
        fi
        zk_replace_str="$zk_replace_str\n$space_4$space_4<node>"
        zk_replace_str="$zk_replace_str\n$space_4$space_4$space_4<host>$zk_host</host>"
        zk_replace_str="$zk_replace_str\n$space_4$space_4$space_4<port>$zk_port</port>"
        zk_replace_str="$zk_replace_str\n$space_4$space_4</node>"
    done
    zk_replace_str="$zk_replace_str\n$space_4</zookeeper>"

    zk_replace_str=$(echo "$zk_replace_str" | sed 's/<\//<\\\//g')
    sed -e "s/<zookeeper>.*<\/zookeeper>/$zk_replace_str/g" $main_config_file > test_file \
        && mv -f test_file $main_config_file && sed -i 's/\r//' $main_config_file
}

## replace replica nodes config
update_replica_nodes_config() {
    ### replica config
    #### get current node hostname and all to install hostname, to get current node number
    replica_node_list_str=$1
    clickhouse_username=$clickhouse_default_username
    clickhouse_password=${config_map[${clickhouse_default_password_key}]}
    space_4="    "
    local_host=$(get_hostname)
    node_list=($(echo $replica_node_list_str | tr "," "\n" | sort | uniq))
    current_node_no=0
    for i in ${!node_list[@]};
    do
        if [ ${node_list[$i]} == $local_host ]; then
            current_node_no=$i
            break
        fi
    done
    current_node_no=$(printf "%02d" $current_node_no)

    #### default: shard count: same as node count; replica count: node count - 1
    node_replace_str="<$cluster_name_${#node_list[@]}shards_2replicas>"
    allow_internal_replication_str="<internal_replication>true</internal_replication>"
    for i in ${!node_list[@]};
    do
        #### add two replica node
        next_node=""
        if [[ $i -lt $((${#node_list[@]}-1)) ]]; then
            next_node=${node_list[$i+1]}
        else
            next_node=${node_list[0]}
        fi
        replica_node_arr=(${node_list[$i]} $next_node)

        node_num_str=$(printf "%02d" $i)
        database_num="$default_database$node_num_str"
        for replica_node in ${replica_node_arr[@]}
        do
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4<shard>"
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4$space_4$allow_internal_replication_str"
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4$space_4<replica>"
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4$space_4$space_4<default_database>$database_num</default_database>"
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4$space_4$space_4<host>$replica_node</host>"
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4$space_4$space_4<port>$clickhouse_default_port</port>"
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4$space_4$space_4<user>$clickhouse_username</user>"
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4$space_4$space_4<password>$clickhouse_password</password>"
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4$space_4</replica>"
            node_replace_str="$node_replace_str\n$space_4$space_4$space_4</shard>"
        done
    done
    node_replace_str="$node_replace_str\n$space_4$space_4</$cluster_name_${#node_list[@]}shards_2replicas>"

    node_replace_str=$(echo "$node_replace_str" | sed 's/<\//<\\\//g')
    sed -e "s/<cluster_nshards_2replicas>.*<\/cluster_nshards_2replicas>/$node_replace_str/g" $main_config_file > test_file \
        && mv -f test_file $main_config_file && sed -i 's/\r//' $main_config_file

    #### todo: support set more replica env (in one node, maybe more than 1 replica)
    sed -i "s/<shard>shard_no<\/shard>/<shard>$current_node_no<\/shard>/g" $main_config_file
    sed -i "s/<replica>replica_no<\/replica>/<replica>$current_node_no<\/replica>/g" $main_config_file
}

## replace monitor port config
update_monitor_port_config() {
    monitor_port=$1
    sed -i "s/{monitor_port}/$monitor_port/g" $main_config_file
}

## replace data path config
update_data_path_config() {
    data_path=$1
    sed -i "s/{data_path}/$data_path/g" $main_config_file
}

## replace tmp path config
update_tmp_path_config() {
    tmp_path=$1
    sed -i "s/{tmp_path}/$tmp_path/g" $main_config_file
}


## set default database
update_default_database() {
    if [ -n "$1" ]; then
        default_database=$1
    fi
}

## set normal user
update_normal_user() {
    if [ -n "$1" ]; then
        normal_user=$1
    fi
}

## set normal user password
update_normal_user_password() {
    if [ -n "$1" ]; then
        normal_user_password=$1
    fi
}

## set normal user allow database and set config file
update_normal_user_allow_databases() {
    if [ -n "$1" ]; then
        normal_user_allow_databases=$1
    fi
    space_4="    "

    # split normal user and password
    normal_user_arr=${normal_user}
    normal_user_password_arr=${normal_user_password}
    normal_user_allow_databases_arr=${normal_user_allow_databases}
    if [[ ${normal_user} == *";"* ]]; then
        normal_user_arr=($(echo ${normal_user} | tr ";" "\n"))
        normal_user_password_arr=($(echo ${normal_user_password} | tr ";" "\n"))
        normal_user_allow_databases_arr=($(echo ${normal_user_allow_databases} | tr ";" "\n"))
    fi

    normal_user_replace_str=""
    for index in ${!normal_user_arr[@]}
    do
        local normal_user=${normal_user_arr[${index}]}
        local normal_user_password=${normal_user_password_arr[${index}]}
        local normal_user_allow_databases=${normal_user_allow_databases_arr[${index}]}

        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4<$normal_user>"
        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4$space_4<password>$normal_user_password</password>"
        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4$space_4<profile>default</profile>"
        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4$space_4<quota>default</quota>"
        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4$space_4<networks>"
        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4$space_4$space_4<ip>::/0</ip>"
        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4$space_4</networks>"
        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4$space_4<allow_databases>"
        allow_database_list=($(echo $normal_user_allow_databases | tr "," "\n" | sort | uniq))
        for allow_database in ${allow_database_list[@]}
        do
            normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4$space_4$space_4<database>$allow_database</database>"
        done
        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4$space_4</allow_databases>"
        normal_user_replace_str="$normal_user_replace_str\n$space_4$space_4</$normal_user>"
    done
    normal_user_replace_str=$(echo "$normal_user_replace_str" | sed 's/<\//<\\\//g')
    normal_user_replace_str=$(echo "$normal_user_replace_str" | sed 's/\/0/\\\/0/g')
    sed -ie "s/<normal_user><\/normal_user>/$normal_user_replace_str/g" $users_config_file
    sed -i "s/<max_memory_usage>10000000000<\/max_memory_usage>/<max_memory_usage>10000000000<\/max_memory_usage>\n$space_4$space_4$space_4<max_partitions_per_insert_block>1000<\/max_partitions_per_insert_block>/g" $users_config_file
}

install() {
    ## install clickhouse
    repo_url=${config_map[${repo_url_key}]}
    clickhouse_default_password=${config_map[${clickhouse_default_password_key}]}
    rpm_path="/clickhouse/rpm"
    yum -y install expect

    ### remove old package
    ps -ef | grep "$clickhouse_pid_full_path" | grep -v grep | awk '{print $2}' | xargs --no-run-if-empty kill -9
    rpm -qa | grep clickhouse | xargs --no-run-if-empty rpm -e || true
    
    rm -rf /var/lib/clickhouse
    rm -rf $clickhouse_config_path
    rm -rf /var/log/clickhouse-server
    rm -rf /var/run/clickhouse-server
    rm -rf /usr/bin/clickhouse
    ### data folder backup
    if [ -d "/opt/clickhouse" ]; then
        rm -rf /opt/clickhouse_bak && mv /opt/clickhouse /opt/clickhouse_bak
    fi
    rm -rf /usr/share/bash-completion/completions/clickhouse*

    ## recreate user
    id -u clickhouse &>/dev/null && userdel clickhouse && rm -rf /home/clickhouse && rm -f /var/spool/mail/clickhouse
    id -u clickhouse-bridge &>/dev/null && userdel clickhouse-bridge && rm -rf /home/clickhouse-bridge && rm -f /var/spool/mail/clickhouse-bridge

    id -u clickhouse &>/dev/null || useradd clickhouse || true
    id -u clickhouse-bridge &>/dev/null || useradd clickhouse-bridge || true

    ## download rpm package from repo
    clickhouse_rpm_common_name="clickhouse-common-static-21.7.8.58-2.x86_64.rpm"
    clickhouse_rpm_client_name="clickhouse-client-21.7.8.58-2.noarch.rpm"
    clickhouse_rpm_server_name="clickhouse-server-21.7.8.58-2.noarch.rpm"

    rm -f $clickhouse_rpm_common_name && rm -f $clickhouse_rpm_client_name && rm -f $clickhouse_rpm_server_name 
    wget $repo_url/$rpm_path/$clickhouse_rpm_common_name
    wget $repo_url/$rpm_path/$clickhouse_rpm_client_name
    wget $repo_url/$rpm_path/$clickhouse_rpm_server_name

    expect_password_str="Enter password for default user"
    rpm -ivh $clickhouse_rpm_common_name
    rpm -ivh $clickhouse_rpm_client_name
    expect -c "spawn rpm -ivh $clickhouse_rpm_server_name;expect \"$expect_password_str\";send \"$clickhouse_default_password\n\";interact"

    mkdir -p $clickhouse_data_home_path && chown -R clickhouse:clickhouse $clickhouse_data_home_path
    mkdir -p $clickhouse_pid_path && chown -R clickhouse:clickhouse $clickhouse_pid_path
    chown -R clickhouse:clickhouse $clickhouse_config_path

    ## install finish
    ### clean rpm package
    rm -f $clickhouse_rpm_common_name && rm -f $clickhouse_rpm_client_name && rm -f $clickhouse_rpm_server_name
}

restart() {
    systemctl restart clickhouse-server
}

command=$1
shift
args=$@

case $command in
   (install)
      get_config
      install
      update_config
      ;;
   (update_config)
      get_config
      update_config
      ;;
   (restart)
      restart
      ;;
   (*)
      echo "$command is not valid, please check!"
      exit 1
      ;;
esac
