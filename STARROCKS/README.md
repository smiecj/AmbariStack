# 环境准备

安装 starrocks 的节点需要安装 jdk 17 ，安装完成后，可配置JDK_HOME 环境变量，如下：
```
export JDK_HOME=/usr/java/jdk-17.0.6+10 # java
```

快速安装：参考项目 [shell-tools](https://github.com/smiecj/shell-tools) 执行 make java-new

# 选择 fe、be 节点

至少3节点起

# 配置

主要包含数据路径、端口配置，可根据需求自行修改

# 安装

等待安装完成，默认安装路径：/opt/modules/starrocks/StarRocks-2.5.3

接下来先做一些初始化操作

# 初始化

## 启动主节点 fe

默认主节点 fe 为 **ip 最小的**节点
直接在ambari界面重启即可

## 添加 fe 备节点 信息

```
# 主节点执行，默认 root 账号无密码
mysql -h127.0.0.1 -P9030 -uroot

# 添加 fe follower
ALTER SYSTEM ADD FOLLOWER "备节点1:9010";
ALTER SYSTEM ADD FOLLOWER "备节点2:9010";
```

**重启备节点 fe**，确认 /opt/modules/starrocks/StarRocks-2.5.3/fe/log/fe.log 中的日志显示正常，而不是

也可以打开主节点 fe 的 web 页面，确认fe状态

## 添加 backend 节点

```
# 主节点执行，默认 root 账号无密码
mysql -h127.0.0.1 -P9030 -uroot

# 添加 backend
ALTER SYSTEM ADD BACKEND "be节点1:9050";
ALTER SYSTEM ADD BACKEND "be节点2:9050";
ALTER SYSTEM ADD BACKEND "be节点3:9050";
```

重启所有节点be，确认 /opt/modules/starrocks/StarRocks-2.5.3/be/log/be.log 显示正常，或者到 fe 页面查看 backend 状态

# 用户管理

## 修改 root 密码

```
SET PASSWORD FOR 'root' = PASSWORD('root新密码');
```

## 添加新用户

```
# 创建用户
CREATE USER 'test' IDENTIFIED by '123456';

# 添加库操作权限
GRANT SELECT_PRIV,LOAD_PRIV,ALTER_PRIV,CREATE_PRIV,DROP_PRIV ON test_db.* TO 'test'@'%';

# 添加资源管理权限
GRANT USAGE_PRIV ON RESOURCE * TO 'test'@'%';
```

# 监控

[参考官方文档](https://docs.starrocks.io/zh-cn/2.5/administration/Monitor_and_Alert)

## 配置 prometheus

```
  - job_name: 'StarRocks_Cluster'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['fe节点1:8030','fe节点2:8030','fe节点3:8030']
        labels:
          group: fe
      - targets: ['be节点1:8040', 'be节点2:8040', 'be节点3:8040']
        labels:
          group: be
```

## 导入 grafana 看板

[最新看板地址](http://starrocks-thirdparty.oss-cn-zhangjiakou.aliyuncs.com/StarRocks-Overview-24.json)