# ambari stack

## clickhouse
install clickhouse

### restart clickhouse
if clickhouse install failed, before restart clickhouse, you may need do these job:

rm -rf data_path
mkdir -p data_path
mkdir -p /var/log/clickhouse-server
chown -R clickhouse:clickhouse /var/log/clickhouse-server
chown -R clickhouse:clickhouse data_path
chown -R clickhouse:clickhouse /var/lib/clickhouse
systemctl restart clickhouse-server
tail -f /var/log/clickhouse-server/clickhouse-server.log

## conda
install miniconda2

## jupyter
install jupyterhub

## npm
install nodejs