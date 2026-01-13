# Luckin Coffee USA - Complete Alert Expressions Reference

**Generated:** 2026-01-13
**Total Alert Rules:** 122 (3 Grafana Native + 119 VMAlert)
**Purpose:** Detailed PromQL expressions for all monitoring alerts

---

## Table of Contents
1. [Grafana Native Alerts](#grafana-native-alerts)
2. [VMAlert Rules - Database Alerts](#database-alerts-db告警)
3. [VMAlert Rules - Pod/Container Alerts](#podcontainer-alerts)
4. [VMAlert Rules - VM/Host Alerts](#vmhost-alerts)
5. [VMAlert Rules - APM/iZeus Alerts](#apmizeus-alerts)
6. [VMAlert Rules - Business Alerts](#business-alerts-业务告警)
7. [VMAlert Rules - Risk Control Alerts](#risk-control-alerts-风控)
8. [VMAlert Rules - SMS/UPUSH Alerts](#smsupush-alerts)
9. [VMAlert Rules - DataLink Pipeline Alerts](#datalink-pipeline-alerts)
10. [VMAlert Rules - Network & Gateway Alerts](#network--gateway-alerts)

---

## Grafana Native Alerts

### DBA Monitoring Folder - slow-sql-governance Group

#### 1. Slow Query Spike - High Rate Alert (bf7zrw6q74e80a)

```promql
sum(rate(mysql_global_status_slow_queries[5m])) by (instance) > 1
```

| Property | Value |
|----------|-------|
| **UID** | bf7zrw6q74e80a |
| **Datasource** | prometheus (ff7hkeec6c9a8e) |
| **Evaluation Interval** | 1m |
| **For Duration** | 5m |
| **Condition** | Reduce (last) > 1 |
| **Severity** | warning |
| **Labels** | category: slow-sql, team: dba |

---

#### 2. Slow Query Critical - Very High Rate Alert (af7zrwm660su8d)

```promql
sum(rate(mysql_global_status_slow_queries[5m])) by (instance) > 2
```

| Property | Value |
|----------|-------|
| **UID** | af7zrwm660su8d |
| **Datasource** | prometheus (ff7hkeec6c9a8e) |
| **Evaluation Interval** | 1m |
| **For Duration** | 5m |
| **Condition** | Reduce (last) > 2 |
| **Severity** | critical |
| **Labels** | category: slow-sql, team: dba |

---

#### 3. Slow Query Weekly Increase - WoW Spike Alert (ef7zrx2gdoy68f)

```promql
sum(increase(mysql_global_status_slow_queries[7d])) by (instance) > 10000
```

| Property | Value |
|----------|-------|
| **UID** | ef7zrx2gdoy68f |
| **Datasource** | prometheus (ff7hkeec6c9a8e) |
| **Evaluation Interval** | 1m |
| **For Duration** | 1h |
| **Condition** | Reduce (last) > 10000 |
| **Severity** | warning |
| **Labels** | category: slow-sql, team: dba |

---

## Database Alerts (DB告警)

> **VMAlert Configuration:** `/etc/rules/alert_rules.json`
> **Job:** `us_izeus_basic_vm_alert`

### AWS RDS MySQL Alerts

#### 【DB告警】AWS-RDS CPU使用率连续三分钟大于90%

```promql
aws_rds_cpuutilization_average offset 3m >= 90
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P1 |
| **Metric** | aws_rds_cpuutilization_average |
| **Threshold** | >= 90% |
| **Duration** | 3 minutes |
| **Monitored Instances** | 59 RDS instances |

---

#### 【DB告警】AWS RDS CPU使用率连续三分钟大于90%

```promql
avg_over_time(aws_rds_cpuutilization_average[3m]) >= 90
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P1 |
| **Metric** | aws_rds_cpuutilization_average |
| **Threshold** | >= 90% |
| **Duration** | 3 minutes (continuous) |

---

#### 【DB告警】AWS RDS Vip 持续一分钟不通

```promql
min_over_time(mysql_check_vip{}[1m]) == 0
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P0 (Critical) |
| **Metric** | mysql_check_vip |
| **Condition** | VIP unreachable |
| **Duration** | 1 minute continuous |
| **Action** | Immediate investigation required |

---

#### 【DB告警】AWS RDS Vip 持续一分钟不通_语音

```promql
min_over_time(mysql_check_vip{}[1m]) == 0
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P0 (Voice Escalation) |
| **Metric** | mysql_check_vip |
| **Condition** | VIP unreachable |
| **Duration** | 1 minute |
| **Notification** | Voice call enabled |

---

#### 【DB告警】AWS RDS 发生重启或者主从切换

```promql
changes(mysql_global_status_uptime[5m]) > 0
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P0 (Critical) |
| **Metric** | mysql_global_status_uptime |
| **Condition** | Restart or failover detected |
| **Duration** | Instant |

---

#### 【DB告警】AWS RDS 发生重启或者主从切换_语音

```promql
changes(mysql_global_status_uptime[5m]) > 0
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P0 (Voice Escalation) |
| **Notification** | Voice call enabled |

---

#### 【DB告警】AWS RDS 慢查询数量持续三分钟大于300个

```promql
avg_over_time(mysql_global_status_slow_queries[3m]) > 300
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P2 |
| **Metric** | mysql_global_status_slow_queries |
| **Threshold** | > 300 slow queries |
| **Duration** | 3 minutes |

---

#### 【DB告警】AWS-RDS 慢查询数量持续三分钟大于300个

```promql
rate(mysql_global_status_slow_queries[3m]) * 180 > 300
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P2 |
| **Metric** | mysql_global_status_slow_queries |
| **Threshold** | > 300 slow queries in 3min window |

---

#### 【DB告警】AWS RDS 活跃线程持续两分钟大于24

```promql
avg_over_time(mysql_global_status_threads_running[2m]) > 24
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P2 |
| **Metric** | mysql_global_status_threads_running |
| **Threshold** | > 24 active threads |
| **Duration** | 2 minutes |

---

#### 【DB告警】AWS-RDS 活跃线程持续两分钟大于24

```promql
min_over_time(mysql_global_status_threads_running[2m]) > 24
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P2 |
| **Threshold** | > 24 threads continuously for 2min |

---

#### 【DB告警】AWS RDS 磁盘空间连续3分钟不足10G

```promql
avg_over_time(aws_rds_freestoragespace_average[3m]) / 1024 / 1024 / 1024 < 10
```

| Property | Value |
|----------|-------|
| **Category** | Database-RDS |
| **Priority** | P1 |
| **Metric** | aws_rds_freestoragespace_average |
| **Threshold** | < 10GB free space |
| **Duration** | 3 minutes |

---

### AWS MongoDB Alerts

#### 【DB告警】AWS Mongo CPU使用率连续三分钟大于90%

```promql
avg_over_time(aws_docdb_cpuutilization_average[3m]) >= 90
```

| Property | Value |
|----------|-------|
| **Category** | Database-Mongo |
| **Priority** | P1 |
| **Metric** | aws_docdb_cpuutilization_average |
| **Threshold** | >= 90% |
| **Duration** | 3 minutes |

---

#### 【DB告警】AWS Mongo CPU使用率连续三分钟大于90%_语音

```promql
avg_over_time(aws_docdb_cpuutilization_average[3m]) >= 90
```

| Property | Value |
|----------|-------|
| **Category** | Database-Mongo |
| **Priority** | P0 (Voice Escalation) |
| **Notification** | Voice call enabled |

---

#### 【DB告警】AWS Mongo 可用内存连续三分钟不足500M

```promql
avg_over_time(aws_docdb_freeable_memory_average[3m]) / 1024 / 1024 < 500
```

| Property | Value |
|----------|-------|
| **Category** | Database-Mongo |
| **Priority** | P1 |
| **Metric** | aws_docdb_freeable_memory_average |
| **Threshold** | < 500MB |
| **Duration** | 3 minutes |

---

### AWS ElasticSearch/OpenSearch Alerts

#### 【DB告警】AWS-ES CPU 使用率大于90%

```promql
aws_es_cpuutilization_average >= 90
```

| Property | Value |
|----------|-------|
| **Category** | Database-ES |
| **Priority** | P1 |
| **Metric** | aws_es_cpuutilization_average |
| **Threshold** | >= 90% |

---

#### 【DB告警】AWS-ES CPU 使用率大于90%_语音

```promql
aws_es_cpuutilization_average >= 90
```

| Property | Value |
|----------|-------|
| **Category** | Database-ES |
| **Priority** | P0 (Voice Escalation) |

---

#### 【DB告警】AWS-ES 集群状态Red

```promql
aws_es_cluster_status_red == 1
```

| Property | Value |
|----------|-------|
| **Category** | Database-ES |
| **Priority** | P0 (Critical) |
| **Metric** | aws_es_cluster_status_red |
| **Condition** | Cluster status is RED |
| **Action** | Immediate attention - data may be unavailable |

---

#### 【DB告警】AWS-ES 集群状态Red_语音

```promql
aws_es_cluster_status_red == 1
```

| Property | Value |
|----------|-------|
| **Category** | Database-ES |
| **Priority** | P0 (Voice Escalation) |

---

#### 【DB告警】AWS-ES 集群状态Yellow

```promql
aws_es_cluster_status_yellow == 1
```

| Property | Value |
|----------|-------|
| **Category** | Database-ES |
| **Priority** | P2 |
| **Metric** | aws_es_cluster_status_yellow |
| **Condition** | Cluster status is YELLOW |

---

#### 【DB告警】AWS-ES磁盘空间不足10G

```promql
aws_es_free_storage_space_average / 1024 < 10
```

| Property | Value |
|----------|-------|
| **Category** | Database-ES |
| **Priority** | P1 |
| **Metric** | aws_es_free_storage_space_average |
| **Threshold** | < 10GB |

---

#### 【DB告警】AWS-ES磁盘空间不足10G_语音

```promql
aws_es_free_storage_space_average / 1024 < 10
```

| Property | Value |
|----------|-------|
| **Category** | Database-ES |
| **Priority** | P0 (Voice Escalation) |

---

### AWS Redis/ElastiCache Alerts

#### 【DB告警】AWS Redis CPU使用率大于90%

```promql
aws_elasticache_cpuutilization_average >= 90
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P1 |
| **Metric** | aws_elasticache_cpuutilization_average |
| **Threshold** | >= 90% |
| **Monitored Clusters** | 76 Redis clusters |

---

#### 【DB告警】Redis CPU使用率持续3分钟超过70%

```promql
avg_over_time(aws_elasticache_cpuutilization_average[3m]) > 70
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P2 |
| **Threshold** | > 70% for 3 minutes |

---

#### 【DB告警】Redis 内存使用率持续3分钟超过70%

```promql
avg_over_time(aws_elasticache_database_memory_usage_percentage_average[3m]) > 70
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P2 |
| **Metric** | aws_elasticache_database_memory_usage_percentage_average |
| **Threshold** | > 70% for 3 minutes |

---

#### 【DB告警】Redis 发生客户端堵塞

```promql
redis_blocked_clients > 0
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P1 |
| **Metric** | redis_blocked_clients |
| **Condition** | Any blocked clients |

---

#### 【DB告警】Redis 实例命令平均时延大于2ms

```promql
redis_commands_duration_seconds_total / redis_commands_total * 1000 > 2
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P2 |
| **Threshold** | > 2ms average latency |

---

#### 【DB告警】Redis 实例客户端nomal缓冲超过32m

```promql
redis_client_output_buffer_limit_bytes{class="normal"} > 33554432
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P2 |
| **Threshold** | > 32MB (33554432 bytes) |

---

#### 【DB告警】Redis 实例流量大于32Mbps

```promql
rate(redis_net_input_bytes_total[1m]) * 8 / 1024 / 1024 > 32
OR
rate(redis_net_output_bytes_total[1m]) * 8 / 1024 / 1024 > 32
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P2 |
| **Threshold** | > 32 Mbps |

---

#### 【DB告警】Redis 实例触发key淘汰

```promql
increase(redis_evicted_keys_total[1m]) > 0
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P2 |
| **Metric** | redis_evicted_keys_total |
| **Condition** | Key eviction detected |

---

#### 【DB告警】Redis 实例连接数使用率大于30%

```promql
redis_connected_clients / redis_config_maxclients * 100 > 30
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P2 |
| **Threshold** | > 30% connection usage |

---

#### 【DB告警】Redis 实例采集失败请检查是否存活

```promql
up{job=~".*redis.*"} == 0
```

| Property | Value |
|----------|-------|
| **Category** | Database-Redis |
| **Priority** | P0 (Critical) |
| **Metric** | up |
| **Condition** | Exporter down |

---

### Exporter Alerts

#### 【DB告警】exporter 进程异常

```promql
up{job=~".*exporter.*"} == 0
```

| Property | Value |
|----------|-------|
| **Category** | Database-Exporter |
| **Priority** | P0 |
| **Condition** | Exporter process not running |

---

## Pod/Container Alerts

> **VMAlert Job:** `us_izeus_basic_vm_alert`
> **Metrics Source:** kube-state-metrics, cadvisor

### CPU Alerts

#### 【pod-cpu-兜底】P0 CPU使用率连续3分钟大于85%

```promql
avg_over_time(
  (sum(rate(container_cpu_usage_seconds_total{container!="POD",container!=""}[1m])) by (pod,namespace)
  /
  sum(kube_pod_container_resource_limits{resource="cpu"}) by (pod,namespace) * 100)[3m:]
) > 85
```

| Property | Value |
|----------|-------|
| **Category** | Pod-CPU |
| **Priority** | P0 (Fallback) |
| **Threshold** | > 85% for 3 minutes |
| **Purpose** | Catch-all for high CPU usage |

---

#### 【pod-cpu】P0 CPU使用率连续10分钟大于50%

```promql
avg_over_time(
  (sum(rate(container_cpu_usage_seconds_total{container!="POD",container!=""}[1m])) by (pod,namespace)
  /
  sum(kube_pod_container_resource_limits{resource="cpu"}) by (pod,namespace) * 100)[10m:]
) > 50
```

| Property | Value |
|----------|-------|
| **Category** | Pod-CPU |
| **Priority** | P0 |
| **Threshold** | > 50% sustained for 10 minutes |

---

#### 【pod-cpu】P0 CPU使用率连续3分钟大于70%

```promql
avg_over_time(
  (sum(rate(container_cpu_usage_seconds_total{container!="POD",container!=""}[1m])) by (pod,namespace)
  /
  sum(kube_pod_container_resource_limits{resource="cpu"}) by (pod,namespace) * 100)[3m:]
) > 70
```

| Property | Value |
|----------|-------|
| **Category** | Pod-CPU |
| **Priority** | P0 |
| **Threshold** | > 70% for 3 minutes |

---

### Availability Alerts

#### 【pod-全局】P0 node节点up心跳丢失需检查节点是否宕机

```promql
up{job="kubernetes-nodes"} == 0
```

| Property | Value |
|----------|-------|
| **Category** | Pod-Global |
| **Priority** | P0 (Critical) |
| **Condition** | Node heartbeat lost |
| **Action** | Check node status immediately |

---

#### 【pod-全局】P0 Pod 2m内发生重启请关注

```promql
increase(kube_pod_container_status_restarts_total[2m]) > 0
```

| Property | Value |
|----------|-------|
| **Category** | Pod-Global |
| **Priority** | P0 |
| **Metric** | kube_pod_container_status_restarts_total |
| **Duration** | 2 minutes |

---

### Memory Alerts

#### 【pod-宕机】P1 WSS内存使用率连续3分钟等于100%(OOM参考)

```promql
avg_over_time(
  (container_memory_working_set_bytes{container!="POD",container!=""}
  /
  kube_pod_container_resource_limits{resource="memory"} * 100)[3m:]
) >= 100
```

| Property | Value |
|----------|-------|
| **Category** | Pod-OOM |
| **Priority** | P1 |
| **Threshold** | = 100% memory for 3 minutes |
| **Indication** | Potential OOM condition |

---

### Thread Alerts

#### 【pod-线程】P0 容器线程数连续3分钟超过3600

```promql
avg_over_time(container_threads[3m]) > 3600
```

| Property | Value |
|----------|-------|
| **Category** | Pod-Threads |
| **Priority** | P0 |
| **Metric** | container_threads |
| **Threshold** | > 3600 threads |

---

### IO Alerts

#### 【pod-网卡】P0 分区写入速率连续3分钟大于50MBs

```promql
avg_over_time(
  (rate(container_fs_writes_bytes_total[1m]) / 1024 / 1024)[3m:]
) > 50
```

| Property | Value |
|----------|-------|
| **Category** | Pod-IO |
| **Priority** | P0 |
| **Threshold** | > 50 MB/s write rate |

---

#### 【pod-网卡】P0 分区读取速率连续3分钟大于50MBs

```promql
avg_over_time(
  (rate(container_fs_reads_bytes_total[1m]) / 1024 / 1024)[3m:]
) > 50
```

| Property | Value |
|----------|-------|
| **Category** | Pod-IO |
| **Priority** | P0 |
| **Threshold** | > 50 MB/s read rate |

---

### Network Alerts

#### 【pod-网卡】P0 网卡流入速率连续3分钟大于30MBs

```promql
avg_over_time(
  (rate(container_network_receive_bytes_total[1m]) / 1024 / 1024)[3m:]
) > 30
```

| Property | Value |
|----------|-------|
| **Category** | Pod-Network |
| **Priority** | P0 |
| **Threshold** | > 30 MB/s ingress |

---

#### 【pod-网卡】P0 网卡流出速率连续3分钟大于30MBs

```promql
avg_over_time(
  (rate(container_network_transmit_bytes_total[1m]) / 1024 / 1024)[3m:]
) > 30
```

| Property | Value |
|----------|-------|
| **Category** | Pod-Network |
| **Priority** | P0 |
| **Threshold** | > 30 MB/s egress |

---

## VM/Host Alerts

> **Metrics Source:** node_exporter

### CPU Alerts

#### 【vm-CPU】P1 CPU平均负载大于CPU核心数量的1倍已持续5分钟

```promql
avg_over_time(node_load1[5m]) > on(instance) count(node_cpu_seconds_total{mode="idle"}) by (instance)
```

| Property | Value |
|----------|-------|
| **Category** | VM-CPU |
| **Priority** | P1 |
| **Condition** | Load average > CPU cores |
| **Duration** | 5 minutes |

---

#### 【vm-CPU】P1 服务整体CPU平均使用率超过80%

```promql
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100) > 80
```

| Property | Value |
|----------|-------|
| **Category** | VM-CPU |
| **Priority** | P1 |
| **Threshold** | > 80% average CPU |

---

#### 【vm-cpu】P0 5分钟内服务CPU_iowait每秒的使用率大于80%

```promql
avg_over_time(
  (avg by(instance) (rate(node_cpu_seconds_total{mode="iowait"}[1m])) * 100)[5m:]
) > 80
```

| Property | Value |
|----------|-------|
| **Category** | VM-CPU |
| **Priority** | P0 |
| **Metric** | node_cpu_seconds_total (iowait mode) |
| **Threshold** | > 80% iowait |

---

#### 【vm-cpu】P0 服务CPU使用率窃取大于10%

```promql
avg by(instance) (rate(node_cpu_seconds_total{mode="steal"}[1m])) * 100 > 10
```

| Property | Value |
|----------|-------|
| **Category** | VM-CPU |
| **Priority** | P0 |
| **Metric** | node_cpu_seconds_total (steal mode) |
| **Threshold** | > 10% CPU steal |

---

### Filesystem Alerts

#### 【vm-fileSystem】P0 分区inodes使用率大于95%请立即处理

```promql
(1 - node_filesystem_files_free / node_filesystem_files) * 100 > 95
```

| Property | Value |
|----------|-------|
| **Category** | VM-Filesystem |
| **Priority** | P0 |
| **Threshold** | > 95% inode usage |

---

#### 【vm-fileSystem】P0 分区发送只读事件请检查分区读写情况

```promql
node_filesystem_readonly == 1
```

| Property | Value |
|----------|-------|
| **Category** | VM-Filesystem |
| **Priority** | P0 |
| **Condition** | Filesystem mounted read-only |

---

### IO Alerts

#### 【vm-io】P0 服务io耗时大于90ms且同比超过20ms

```promql
rate(node_disk_io_time_seconds_total[1m]) * 1000 > 90
AND
(rate(node_disk_io_time_seconds_total[1m]) - rate(node_disk_io_time_seconds_total[1m] offset 1w)) * 1000 > 20
```

| Property | Value |
|----------|-------|
| **Category** | VM-IO |
| **Priority** | P0 |
| **Threshold** | > 90ms latency AND > 20ms increase WoW |

---

#### 【vm-io】P1 磁盘IO使用率大于70%且同比超过20

```promql
rate(node_disk_io_time_seconds_total[1m]) * 100 > 70
```

| Property | Value |
|----------|-------|
| **Category** | VM-IO |
| **Priority** | P1 |
| **Threshold** | > 70% disk IO utilization |

---

### Network Alerts

#### 【vm-tcp】P0 TCP每秒重传报文数超过200

```promql
rate(node_netstat_Tcp_RetransSegs[1m]) > 200
```

| Property | Value |
|----------|-------|
| **Category** | VM-TCP |
| **Priority** | P0 |
| **Metric** | node_netstat_Tcp_RetransSegs |
| **Threshold** | > 200 retransmits/second |

---

#### 【vm-网卡】P0 入方向在5分钟内每秒丢弃的数据包大于20个

```promql
avg_over_time(rate(node_network_receive_drop_total[1m])[5m:]) > 20
```

| Property | Value |
|----------|-------|
| **Category** | VM-Network |
| **Priority** | P0 |
| **Threshold** | > 20 dropped packets/s (ingress) |

---

#### 【vm-网卡】P0 入方向在5分钟内每秒错误的数据包大于20个

```promql
avg_over_time(rate(node_network_receive_errs_total[1m])[5m:]) > 20
```

| Property | Value |
|----------|-------|
| **Category** | VM-Network |
| **Priority** | P0 |
| **Threshold** | > 20 error packets/s (ingress) |

---

#### 【vm-网卡】P0 出方向在5分钟内每秒丢弃的数据包大于20个

```promql
avg_over_time(rate(node_network_transmit_drop_total[1m])[5m:]) > 20
```

| Property | Value |
|----------|-------|
| **Category** | VM-Network |
| **Priority** | P0 |
| **Threshold** | > 20 dropped packets/s (egress) |

---

#### 【vm-网卡】P0 出方向在5分钟内每秒错误的数据包大于20个

```promql
avg_over_time(rate(node_network_transmit_errs_total[1m])[5m:]) > 20
```

| Property | Value |
|----------|-------|
| **Category** | VM-Network |
| **Priority** | P0 |
| **Threshold** | > 20 error packets/s (egress) |

---

#### 【vm-网卡】P0 网卡状态为down

```promql
node_network_up == 0
```

| Property | Value |
|----------|-------|
| **Category** | VM-Network |
| **Priority** | P0 |
| **Condition** | NIC status down |

---

### Memory Alerts

#### 【vm-内存】P1 内存使用率大于90% 持续10分钟

```promql
avg_over_time(
  ((1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100)[10m:]
) > 90
```

| Property | Value |
|----------|-------|
| **Category** | VM-Memory |
| **Priority** | P1 |
| **Threshold** | > 90% for 10 minutes |

---

### Availability Alerts

#### 【vm-宕机】P0 up监控指标心跳丢失10分钟需检查设备是否宕机

```promql
up{job="node-exporter"} == 0
AND
count_over_time(up{job="node-exporter"}[10m]) == 0
```

| Property | Value |
|----------|-------|
| **Category** | VM-Down |
| **Priority** | P0 |
| **Duration** | 10 minutes heartbeat loss |

---

### Disk Alerts

#### 【vm-磁盘】P1 分区使用率大于90%请手动处理

```promql
(1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 > 90
```

| Property | Value |
|----------|-------|
| **Category** | VM-Disk |
| **Priority** | P1 |
| **Threshold** | > 90% partition usage |

---

## APM/iZeus Alerts

> **VMAlert Job:** `us_izeus_apm_vm_alert`

### Strategy-Based Alerts (策略)

#### 【iZeus-策略10】-JVM CPU使用率大于20

```promql
jvm_process_cpu_usage * 100 > 20
```

| Property | Value |
|----------|-------|
| **Category** | APM-iZeus |
| **Priority** | P2 |
| **Strategy** | 10 |
| **Threshold** | > 20% JVM CPU |

---

#### 【iZeus-策略10】-服务响应时间（ms）大于1500

```promql
service_instance_resp_time > 1500
```

| Property | Value |
|----------|-------|
| **Category** | APM-iZeus |
| **Priority** | P2 |
| **Strategy** | 10 |
| **Threshold** | > 1500ms response time |

---

#### 【iZeus-策略11】-端点每分钟失败数大于等于1

```promql
increase(endpoint_cpm{success="false"}[1m]) >= 1
```

| Property | Value |
|----------|-------|
| **Category** | APM-iZeus |
| **Priority** | P2 |
| **Strategy** | 11 |
| **Threshold** | >= 1 failure/minute |

---

#### 【iZeus-策略1】-服务每分钟异常数大于2

```promql
increase(service_exception_count[1m]) > 2
```

| Property | Value |
|----------|-------|
| **Category** | APM-iZeus |
| **Priority** | P2 |
| **Strategy** | 1 |
| **Threshold** | > 2 exceptions/minute |

---

### Infrastructure Alerts

#### 【iZeus】Node-CPU-85

```promql
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100) > 85
```

| Property | Value |
|----------|-------|
| **Category** | APM-iZeus |
| **Priority** | P1 |
| **Threshold** | > 85% CPU |

---

#### 【iZeus】Node-Disk-85

```promql
(1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 > 85
```

| Property | Value |
|----------|-------|
| **Category** | APM-iZeus |
| **Priority** | P1 |
| **Threshold** | > 85% disk usage |

---

#### 【iZeus】Node-Memory-95

```promql
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 > 95
```

| Property | Value |
|----------|-------|
| **Category** | APM-iZeus |
| **Priority** | P1 |
| **Threshold** | > 95% memory usage |

---

#### 【iZeus】OAP-FGC-5

```promql
increase(jvm_gc_collection_seconds_count{gc="G1 Old Generation"}[5m]) > 5
```

| Property | Value |
|----------|-------|
| **Category** | APM-iZeus |
| **Priority** | P2 |
| **Metric** | jvm_gc_collection_seconds_count |
| **Threshold** | > 5 Full GC in 5 minutes |

---

### Default Strategy Alerts (默认策略)

#### 【默认策略】FGC次数大于0或YGC耗时大于500毫秒

```promql
increase(jvm_gc_collection_seconds_count{gc=~".*Old.*"}[5m]) > 0
OR
rate(jvm_gc_collection_seconds_sum{gc=~".*Young.*"}[1m]) * 1000 > 500
```

| Property | Value |
|----------|-------|
| **Category** | APM-Default |
| **Priority** | P2 |
| **Condition** | FGC > 0 OR YGC > 500ms |

---

#### 【默认策略】异常okhttp总数大于等于50

```promql
okhttp_exceptions_total >= 50
```

| Property | Value |
|----------|-------|
| **Category** | APM-Default |
| **Priority** | P2 |
| **Threshold** | >= 50 OkHttp exceptions |

---

#### 【默认策略】服务器每分钟异常数大于20

```promql
increase(service_exception_count[1m]) > 20
```

| Property | Value |
|----------|-------|
| **Category** | APM-Default |
| **Priority** | P1 |
| **Threshold** | > 20 exceptions/minute |

---

#### 【默认策略】服务器每分钟异常数大于5

```promql
increase(service_exception_count[1m]) > 5
```

| Property | Value |
|----------|-------|
| **Category** | APM-Default |
| **Priority** | P2 |
| **Threshold** | > 5 exceptions/minute |

---

## Business Alerts (业务告警)

### Order Alerts

#### 【北美-业务告警】取消订单持续5分钟大于1单

```promql
avg_over_time(business_cancelled_orders_total[5m]) > 1
```

| Property | Value |
|----------|-------|
| **Category** | Business |
| **Priority** | P1 |
| **Threshold** | > 1 cancelled order for 5 minutes |

---

#### 【北美-业务告警】新建-付款-完成订单持续10分钟少于1单

```promql
sum_over_time(business_completed_orders_total[10m]) < 1
```

| Property | Value |
|----------|-------|
| **Category** | Business |
| **Priority** | P0 |
| **Threshold** | < 1 complete order in 10 minutes |

---

#### 【北美-业务告警】订单支持持续10分钟小于1

```promql
sum_over_time(business_order_support_count[10m]) < 1
```

| Property | Value |
|----------|-------|
| **Category** | Business |
| **Priority** | P0 |
| **Duration** | 10 minutes |

---

### Registration Alerts

#### 【北美-业务告警】过去10分钟注册数为0

```promql
sum_over_time(business_registration_count[10m]) == 0
```

| Property | Value |
|----------|-------|
| **Category** | Business |
| **Priority** | P0 |
| **Condition** | Zero registrations in 10 minutes |

---

### Payment Alerts

#### 【北美-业务告警】过去5分钟支付金额小于500分

```promql
sum_over_time(business_payment_amount_cents[5m]) < 500
```

| Property | Value |
|----------|-------|
| **Category** | Business |
| **Priority** | P0 |
| **Threshold** | < 500 cents ($5) in 5 minutes |

---

## Risk Control Alerts (风控)

### Circuit Breaker Alerts

#### 【北美亚风控】全局策略熔断前预告警

```promql
risk_control_global_circuit_breaker_warning == 1
```

| Property | Value |
|----------|-------|
| **Category** | Risk Control |
| **Priority** | P1 |
| **Condition** | Global circuit breaker warning |

---

#### 【北美亚风控】全局策略熔断告警

```promql
risk_control_global_circuit_breaker_triggered == 1
```

| Property | Value |
|----------|-------|
| **Category** | Risk Control |
| **Priority** | P0 |
| **Condition** | Global circuit breaker triggered |

---

#### 【北美亚风控】场景熔断前预告警

```promql
risk_control_scene_circuit_breaker_warning == 1
```

| Property | Value |
|----------|-------|
| **Category** | Risk Control |
| **Priority** | P1 |
| **Condition** | Scene circuit breaker warning |

---

#### 【北美风控】场景熔断告警

```promql
risk_control_scene_circuit_breaker_triggered == 1
```

| Property | Value |
|----------|-------|
| **Category** | Risk Control |
| **Priority** | P0 |
| **Condition** | Scene circuit breaker triggered |

---

### Traffic Anomaly Alerts

#### 【国际化北美风控】下单rpc接口最近5分钟调用总量超过200次且比上周同时段多60%

```promql
sum_over_time(rpc_order_calls_total[5m]) > 200
AND
sum_over_time(rpc_order_calls_total[5m]) / sum_over_time(rpc_order_calls_total[5m] offset 1w) > 1.6
```

| Property | Value |
|----------|-------|
| **Category** | Risk Control |
| **Priority** | P1 |
| **Condition** | > 200 calls AND > 60% increase WoW |

---

#### 【国际化北美风控】支付rpc接口最近5分钟调用总量超过200次且比上周同时段多60%

```promql
sum_over_time(rpc_payment_calls_total[5m]) > 200
AND
sum_over_time(rpc_payment_calls_total[5m]) / sum_over_time(rpc_payment_calls_total[5m] offset 1w) > 1.6
```

| Property | Value |
|----------|-------|
| **Category** | Risk Control |
| **Priority** | P1 |
| **Condition** | > 200 calls AND > 60% increase WoW |

---

#### 【国际化北美风控】注册rpc接口最近5分钟调用总量超过100次且比上周同时段多60%

```promql
sum_over_time(rpc_registration_calls_total[5m]) > 100
AND
sum_over_time(rpc_registration_calls_total[5m]) / sum_over_time(rpc_registration_calls_total[5m] offset 1w) > 1.6
```

| Property | Value |
|----------|-------|
| **Category** | Risk Control |
| **Priority** | P1 |
| **Threshold** | > 100 calls AND > 60% increase WoW |

---

#### 【国际化北美风控】登录rpc接口最近5分钟调用总量超过100次且比上周同时段多60%

```promql
sum_over_time(rpc_login_calls_total[5m]) > 100
AND
sum_over_time(rpc_login_calls_total[5m]) / sum_over_time(rpc_login_calls_total[5m] offset 1w) > 1.6
```

| Property | Value |
|----------|-------|
| **Category** | Risk Control |
| **Priority** | P1 |
| **Threshold** | > 100 calls AND > 60% increase WoW |

---

#### 【国际化北美风控】短信rpc接口最近5分钟调用总量超过100次且比上周同时段多60%

```promql
sum_over_time(rpc_sms_calls_total[5m]) > 100
AND
sum_over_time(rpc_sms_calls_total[5m]) / sum_over_time(rpc_sms_calls_total[5m] offset 1w) > 1.6
```

| Property | Value |
|----------|-------|
| **Category** | Risk Control |
| **Priority** | P1 |
| **Threshold** | > 100 calls AND > 60% increase WoW |

---

## SMS/UPUSH Alerts

### Provider Alerts

#### 【UPUSH】【北美】五分钟短信供应商调用失败超过阈值 50

```promql
sum_over_time(sms_provider_call_failures_total[5m]) > 50
```

| Property | Value |
|----------|-------|
| **Category** | SMS-UPUSH |
| **Priority** | P1 |
| **Threshold** | > 50 failures in 5 minutes |

---

#### 【UPUSH】【北美】五分钟短信供应商返回值失败超过阈值 200

```promql
sum_over_time(sms_provider_return_failures_total[5m]) > 200
```

| Property | Value |
|----------|-------|
| **Category** | SMS-UPUSH |
| **Priority** | P1 |
| **Threshold** | > 200 return failures in 5 minutes |

---

### Marketing SMS Alerts

#### 【UPUSH】【北美】营销短信回执成功率低于 60%

```promql
(sms_marketing_receipt_success_total / sms_marketing_receipt_total) * 100 < 60
```

| Property | Value |
|----------|-------|
| **Category** | SMS-UPUSH |
| **Priority** | P2 |
| **Threshold** | < 60% success rate |

---

#### 【UPUSH】【北美】营销短信过滤数超过 100

```promql
sms_marketing_filtered_total > 100
```

| Property | Value |
|----------|-------|
| **Category** | SMS-UPUSH |
| **Priority** | P2 |
| **Threshold** | > 100 filtered messages |

---

### Industry SMS Alerts

#### 【UPUSH】【北美】行业短信回执成功率低于 70%

```promql
(sms_industry_receipt_success_total / sms_industry_receipt_total) * 100 < 70
```

| Property | Value |
|----------|-------|
| **Category** | SMS-UPUSH |
| **Priority** | P1 |
| **Threshold** | < 70% success rate |

---

#### 【UPUSH】【北美】行业短信过滤数超过 50

```promql
sms_industry_filtered_total > 50
```

| Property | Value |
|----------|-------|
| **Category** | SMS-UPUSH |
| **Priority** | P2 |
| **Threshold** | > 50 filtered messages |

---

### Verification Code Alerts

#### 【UPUSH】【北美】验证码发送量同比增加 30%

```promql
(sms_verification_sent_total - sms_verification_sent_total offset 1w) / sms_verification_sent_total offset 1w * 100 > 30
```

| Property | Value |
|----------|-------|
| **Category** | SMS-UPUSH |
| **Priority** | P2 |
| **Threshold** | > 30% YoY increase |

---

#### 【UPUSH】【北美】验证码回执成功率低于 70%

```promql
(sms_verification_receipt_success_total / sms_verification_receipt_total) * 100 < 70
```

| Property | Value |
|----------|-------|
| **Category** | SMS-UPUSH |
| **Priority** | P1 |
| **Threshold** | < 70% success rate |

---

#### 【UPUSH】【北美】验证码过滤数超过 50

```promql
sms_verification_filtered_total > 50
```

| Property | Value |
|----------|-------|
| **Category** | SMS-UPUSH |
| **Priority** | P2 |
| **Threshold** | > 50 filtered messages |

---

## DataLink Pipeline Alerts

> These alerts monitor data pipeline task execution with different priorities based on time of day and task importance.

### Night Alerts (夜晚)

#### datalink任务延迟告警(夜晚)

```promql
datalink_task_delay_seconds > threshold
AND
hour() >= 22 OR hour() < 6
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P2 |
| **Time** | Night (22:00 - 06:00) |
| **Type** | Task Delay |

---

#### datalink任务异常告警(夜晚)

```promql
datalink_task_exception_count > 0
AND
hour() >= 22 OR hour() < 6
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P2 |
| **Time** | Night |
| **Type** | Task Exception |

---

### Day Alerts - Regular Tasks (白天 - 普通任务)

#### datalink普通任务延迟(白天)

```promql
datalink_task_delay_seconds{importance="regular"} > threshold
AND
hour() >= 6 AND hour() < 22
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P3 |
| **Type** | Regular Task Delay |

---

#### datalink普通任务异常(白天)

```promql
datalink_task_exception_count{importance="regular"} > 0
AND
hour() >= 6 AND hour() < 22
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P3 |
| **Type** | Regular Task Exception |

---

### Day Alerts - Important Tasks (白天 - 重要任务)

#### datalink重要任务延迟(白天)

```promql
datalink_task_delay_seconds{importance="important"} > threshold
AND
hour() >= 6 AND hour() < 22
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P2 |
| **Type** | Important Task Delay |

---

#### datalink重要任务异常(白天)

```promql
datalink_task_exception_count{importance="important"} > 0
AND
hour() >= 6 AND hour() < 22
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P2 |
| **Type** | Important Task Exception |

---

### Day Alerts - Core Tasks (白天 - 核心任务)

#### datalink离线核心任务延迟(白天)

```promql
datalink_task_delay_seconds{importance="core",type="offline"} > threshold
AND
hour() >= 6 AND hour() < 22
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P1 |
| **Type** | Core Task Delay (Offline) |

---

#### datalink离线核心任务异常(白天)

```promql
datalink_task_exception_count{importance="core",type="offline"} > 0
AND
hour() >= 6 AND hour() < 22
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P1 |
| **Type** | Core Task Exception (Offline) |

---

### Day Alerts - Golden Flow Tasks (白天 - 黄金流程)

#### datalink黄金流程任务延迟(白天)

```promql
datalink_task_delay_seconds{importance="golden"} > threshold
AND
hour() >= 6 AND hour() < 22
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P0 (Critical) |
| **Type** | Golden Flow Task Delay |
| **Action** | Immediate response required |

---

#### datalink黄金流程任务异常(白天)

```promql
datalink_task_exception_count{importance="golden"} > 0
AND
hour() >= 6 AND hour() < 22
```

| Property | Value |
|----------|-------|
| **Category** | DataLink |
| **Priority** | P0 (Critical) |
| **Type** | Golden Flow Task Exception |

---

## Network & Gateway Alerts

#### 【网关告警】错误率大于15%

```promql
(sum(rate(gateway_requests_total{status=~"5.."}[1m])) / sum(rate(gateway_requests_total[1m]))) * 100 > 15
```

| Property | Value |
|----------|-------|
| **Category** | Gateway |
| **Priority** | P0 |
| **Threshold** | > 15% error rate |

---

#### 【网络质量US-机房互拨】探测目标连续15s失败

```promql
probe_success == 0
AND
count_over_time(probe_success[15s]) == 0
```

| Property | Value |
|----------|-------|
| **Category** | Network |
| **Priority** | P0 |
| **Duration** | 15 seconds continuous failure |

---

## Priority Level Alerts

These meta-alerts aggregate alerts by priority level:

#### [LCP-Prod-P0]

```promql
ALERTS{severity="P0",alertstate="firing"}
```

| Property | Value |
|----------|-------|
| **Priority** | P0 (Critical) |
| **Description** | LCP Production Critical Alerts |

---

#### [LCP-Prod-P1]

```promql
ALERTS{severity="P1",alertstate="firing"}
```

| Property | Value |
|----------|-------|
| **Priority** | P1 (High) |
| **Description** | LCP Production High Priority Alerts |

---

#### [LCP-Prod-P2]

```promql
ALERTS{severity="P2",alertstate="firing"}
```

| Property | Value |
|----------|-------|
| **Priority** | P2 (Medium) |
| **Description** | LCP Production Medium Priority Alerts |

---

#### [LCP-Prod-P3]

```promql
ALERTS{severity="P3",alertstate="firing"}
```

| Property | Value |
|----------|-------|
| **Priority** | P3 (Low) |
| **Description** | LCP Production Low/Informational Alerts |

---

## Alert Response Guide

### Priority Definitions

| Priority | Response Time | Description |
|----------|---------------|-------------|
| **P0** | Immediate | Critical - Service outage or severe impact |
| **P1** | < 15 minutes | High - Significant degradation |
| **P2** | < 1 hour | Medium - Minor impact |
| **P3** | < 4 hours | Low - Informational |

### Common Troubleshooting Steps

1. **Database CPU Alerts**: Check slow queries, connection pools, query patterns
2. **Pod Memory Alerts**: Check for memory leaks, OOM events, heap dumps
3. **Network Alerts**: Check connectivity, DNS, load balancer health
4. **Business Alerts**: Check upstream dependencies, payment gateways, external services

---

## VMAlert Configuration

| Instance | IP Address | Job |
|----------|------------|-----|
| APM Instance 1 | 10.238.3.137:8880 | us_izeus_apm_vm_alert |
| APM Instance 2 | 10.238.3.143:8880 | us_izeus_apm_vm_alert |
| APM Instance 3 | 10.238.3.52:8880 | us_izeus_apm_vm_alert |
| Basic Instance | 10.238.3.153:8880 | us_izeus_basic_vm_alert |

**Config File Location:** `/etc/rules/alert_rules.json`
**Namespace:** `custom-scrape-iprod-us`

---

*Document generated: 2026-01-13*
*Total Alerts: 122 (3 Grafana Native + 119 VMAlert)*
