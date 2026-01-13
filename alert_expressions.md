# Luckin Coffee USA - Grafana Alert Expressions Reference

**Generated:** 2026-01-13
**Total Alert Rules:** 122 (3 Grafana Native + 119 VMAlert)

---

## Table of Contents
1. [Grafana Native Alerts](#grafana-native-alerts)
2. [VMAlert Rules by Category](#vmalert-rules-by-category)
   - [Database Alerts (DB告警)](#database-alerts-db告警)
   - [Pod/Container Alerts](#podcontainer-alerts)
   - [VM/Host Alerts](#vmhost-alerts)
   - [APM/iZeus Alerts](#apmizeus-alerts)
   - [Business Alerts (业务告警)](#business-alerts-业务告警)
   - [Risk Control Alerts (风控)](#risk-control-alerts-风控)
   - [SMS/UPUSH Alerts](#smsupush-alerts)
   - [DataLink Pipeline Alerts](#datalink-pipeline-alerts)
   - [Network & Gateway Alerts](#network--gateway-alerts)
   - [Priority Level Alerts](#priority-level-alerts)

---

## Grafana Native Alerts

### DBA Monitoring Folder - slow-sql-governance Group

#### 1. Slow Query Spike - High Rate Alert
| Property | Value |
|----------|-------|
| **UID** | bf7zrw6q74e80a |
| **Expression** | `sum(rate(mysql_global_status_slow_queries[5m])) by (instance)` |
| **Condition** | Reduce (last) > 1 |
| **For Duration** | 5m |
| **Severity** | warning |
| **Labels** | category: slow-sql, team: dba |
| **Datasource** | prometheus (ff7hkeec6c9a8e) |

#### 2. Slow Query Critical - Very High Rate Alert
| Property | Value |
|----------|-------|
| **UID** | af7zrwm660su8d |
| **Expression** | `sum(rate(mysql_global_status_slow_queries[5m])) by (instance)` |
| **Condition** | Reduce (last) > 2 |
| **For Duration** | 5m |
| **Severity** | critical |
| **Labels** | category: slow-sql, team: dba |
| **Datasource** | prometheus (ff7hkeec6c9a8e) |

#### 3. Slow Query Weekly Increase - WoW Spike Alert
| Property | Value |
|----------|-------|
| **UID** | ef7zrx2gdoy68f |
| **Expression** | `sum(increase(mysql_global_status_slow_queries[7d])) by (instance)` |
| **Condition** | Reduce (last) > 10000 |
| **For Duration** | 1h |
| **Severity** | warning |
| **Labels** | category: slow-sql, team: dba |
| **Datasource** | prometheus (ff7hkeec6c9a8e) |

---

## VMAlert Rules by Category

> All VMAlert rules are defined in `/etc/rules/alert_rules.json` and evaluated by VictoriaMetrics Alert (vmalert).
> Job: `us_izeus_basic_vm_alert` and `us_izeus_apm_vm_alert`

---

### Database Alerts (DB告警)

#### AWS RDS MySQL Alerts

| Alert Name | Metric Type | Condition | Duration | Priority |
|------------|-------------|-----------|----------|----------|
| AWS-RDS CPU使用率连续三分钟大于90% | CPU | >90% | 3min | P1 |
| AWS RDS CPU使用率连续三分钟大于90% | CPU | >90% | 3min | P1 |
| AWS RDS Vip 持续一分钟不通 | Connectivity | VIP unreachable | 1min | P0 |
| AWS RDS Vip 持续一分钟不通_语音 | Connectivity | VIP unreachable | 1min | P0 (Voice) |
| AWS RDS 发生重启或者主从切换 | Failover | Detected | Instant | P0 |
| AWS RDS 发生重启或者主从切换_语音 | Failover | Detected | Instant | P0 (Voice) |
| AWS RDS 慢查询数量持续三分钟大于300个 | Performance | >300 slow queries | 3min | P2 |
| AWS-RDS 慢查询数量持续三分钟大于300个 | Performance | >300 slow queries | 3min | P2 |
| AWS RDS 活跃线程持续两分钟大于24 | Performance | >24 threads | 2min | P2 |
| AWS-RDS 活跃线程持续两分钟大于24 | Performance | >24 threads | 2min | P2 |
| AWS RDS 磁盘空间连续3分钟不足10G | Disk | <10GB | 3min | P1 |

#### AWS MongoDB Alerts

| Alert Name | Metric Type | Condition | Priority |
|------------|-------------|-----------|----------|
| AWS Mongo CPU使用率连续三分钟大于90% | CPU | >90% for 3min | P1 |
| AWS Mongo CPU使用率连续三分钟大于90%_语音 | CPU | >90% for 3min | P0 (Voice) |
| AWS Mongo 可用内存连续三分钟不足500M | Memory | <500MB for 3min | P1 |

#### AWS ElasticSearch Alerts

| Alert Name | Metric Type | Condition | Priority |
|------------|-------------|-----------|----------|
| AWS-ES CPU 使用率大于90% | CPU | >90% | P1 |
| AWS-ES CPU 使用率大于90%_语音 | CPU | >90% | P0 (Voice) |
| AWS-ES 集群状态Red | Cluster Health | Status Red | P0 |
| AWS-ES 集群状态Red_语音 | Cluster Health | Status Red | P0 (Voice) |
| AWS-ES 集群状态Yellow | Cluster Health | Status Yellow | P2 |
| AWS-ES磁盘空间不足10G | Disk | <10GB | P1 |
| AWS-ES磁盘空间不足10G_语音 | Disk | <10GB | P0 (Voice) |

#### AWS Redis/ElastiCache Alerts

| Alert Name | Metric Type | Condition | Priority |
|------------|-------------|-----------|----------|
| AWS Redis CPU使用率大于90% | CPU | >90% | P1 |
| Redis CPU使用率持续3分钟超过70% | CPU | >70% for 3min | P2 |
| Redis 内存使用率持续3分钟超过70% | Memory | >70% for 3min | P2 |
| Redis 发生客户端堵塞 | Connectivity | Client blocked | P1 |
| Redis 实例命令平均时延大于2ms | Latency | >2ms avg | P2 |
| Redis 实例客户端nomal缓冲超过32m | Memory | >32MB buffer | P2 |
| Redis 实例流量大于32Mbps | Network | >32Mbps | P2 |
| Redis 实例触发key淘汰 | Eviction | Key eviction | P2 |
| Redis 实例连接数使用率大于30% | Connections | >30% | P2 |
| Redis 实例采集失败请检查是否存活 | Availability | Collection failed | P0 |

#### Exporter Alerts

| Alert Name | Condition | Priority |
|------------|-----------|----------|
| exporter 进程异常 | Process abnormal | P0 |

---

### Pod/Container Alerts

| Alert Name | Metric Type | Condition | Duration | Priority |
|------------|-------------|-----------|----------|----------|
| P0 CPU使用率连续3分钟大于85% (兜底) | CPU | >85% | 3min | P0 |
| P0 CPU使用率连续10分钟大于50% | CPU | >50% | 10min | P0 |
| P0 CPU使用率连续3分钟大于70% | CPU | >70% | 3min | P0 |
| P0 node节点up心跳丢失 | Availability | Heartbeat lost | Instant | P0 |
| P0 Pod 2m内发生重启 | Stability | Restart detected | 2min | P0 |
| P1 WSS内存使用率连续3分钟等于100% | Memory | 100% (OOM) | 3min | P1 |
| P0 容器线程数连续3分钟超过3600 | Threads | >3600 | 3min | P0 |
| P0 分区写入速率连续3分钟大于50MBs | IO | >50MB/s write | 3min | P0 |
| P0 分区读取速率连续3分钟大于50MBs | IO | >50MB/s read | 3min | P0 |
| P0 网卡流入速率连续3分钟大于30MBs | Network | >30MB/s in | 3min | P0 |
| P0 网卡流出速率连续3分钟大于30MBs | Network | >30MB/s out | 3min | P0 |

---

### VM/Host Alerts

| Alert Name | Metric Type | Condition | Duration | Priority |
|------------|-------------|-----------|----------|----------|
| P1 CPU平均负载大于CPU核心数量的1倍 | CPU | Load >1x cores | 5min | P1 |
| P1 服务整体CPU平均使用率超过80% | CPU | >80% avg | Instant | P1 |
| P0 5分钟内服务CPU_iowait使用率大于80% | CPU | >80% iowait | 5min | P0 |
| P0 服务CPU使用率窃取大于10% | CPU | >10% steal | Instant | P0 |
| P0 分区inodes使用率大于95% | Disk | >95% inodes | Instant | P0 |
| P0 分区发送只读事件 | Disk | RO event | Instant | P0 |
| P0 服务io耗时大于90ms且同比超过20ms | IO | >90ms latency | Instant | P0 |
| P1 磁盘IO使用率大于70%且同比超过20 | IO | >70% usage | Instant | P1 |
| P0 TCP每秒重传报文数超过200 | Network | >200 retrans/s | Instant | P0 |
| P1 内存使用率大于90% | Memory | >90% | 10min | P1 |
| P0 up监控指标心跳丢失10分钟 | Availability | Heartbeat lost | 10min | P0 |
| P1 分区使用率大于90% | Disk | >90% | Instant | P1 |
| P0 入方向每秒丢弃数据包大于20个 | Network | >20 dropped/s in | 5min | P0 |
| P0 入方向每秒错误数据包大于20个 | Network | >20 errors/s in | 5min | P0 |
| P0 出方向每秒丢弃数据包大于20个 | Network | >20 dropped/s out | 5min | P0 |
| P0 出方向每秒错误数据包大于20个 | Network | >20 errors/s out | 5min | P0 |
| P0 网卡状态为down | Network | NIC down | Instant | P0 |

---

### APM/iZeus Alerts

#### Strategy-Based Alerts (策略)

| Alert Name | Metric Type | Condition | Priority |
|------------|-------------|-----------|----------|
| 策略10 - JVM CPU使用率大于20 | JVM CPU | >20% | P2 |
| 策略10 - 服务响应时间(ms)大于1500 | Latency | >1500ms | P2 |
| 策略11-17 - 端点每分钟失败数大于N | Errors | >=1 to >3 failures/min | P2 |
| 策略1-9 - 服务每分钟异常数大于2-3 | Errors | >2-3 exceptions/min | P2 |

#### Infrastructure Alerts

| Alert Name | Metric Type | Condition | Priority |
|------------|-------------|-----------|----------|
| Node-CPU-85 | CPU | >85% | P1 |
| Node-Disk-85 | Disk | >85% | P1 |
| Node-Memory-95 | Memory | >95% | P1 |
| OAP-FGC-5 | JVM | FGC >5 | P2 |
| Storage-Receiver2Thanos-Receiver-0 | Storage | Issue detected | P1 |
| Storage-Receiver2VM-0 | Storage | Issue detected | P1 |
| Transfer-Agent2OAP-0 | Transfer | Issue detected | P1 |
| Transfer-OAP2OAP-0 | Transfer | Issue detected | P1 |
| Transfer-OAPTrace2Receiver-0 | Transfer | Issue detected | P1 |

#### Default Strategy Alerts (默认策略)

| Alert Name | Condition | Priority |
|------------|-----------|----------|
| FGC次数大于0或YGC耗时大于500毫秒 | FGC >0 OR YGC >500ms | P2 |
| 异常okhttp总数大于等于50 | >=50 okhttp exceptions | P2 |
| 服务器每分钟异常数大于20 | >20 exceptions/min | P1 |
| 服务器每分钟异常数大于5 | >5 exceptions/min | P2 |

---

### Business Alerts (业务告警)

| Alert Name | Metric Type | Condition | Duration | Priority |
|------------|-------------|-----------|----------|----------|
| 取消订单持续5分钟大于1单 | Orders | >1 cancelled | 5min | P1 |
| 新建-付款-完成订单持续10分钟少于1单 | Orders | <1 complete | 10min | P0 |
| 订单支持持续10分钟小于1 | Orders | <1 support | 10min | P0 |
| 过去10分钟注册数为0 | Registration | 0 registrations | 10min | P0 |
| 过去5分钟支付金额小于500分 | Payments | <500 cents | 5min | P0 |

---

### Risk Control Alerts (风控)

| Alert Name | Metric Type | Condition | Priority |
|------------|-------------|-----------|----------|
| 全局策略熔断前预告警 | Circuit Breaker | Pre-break warning | P1 |
| 全局策略熔断告警 | Circuit Breaker | Break triggered | P0 |
| 场景熔断前预告警 | Circuit Breaker | Pre-break warning | P1 |
| 场景熔断告警 | Circuit Breaker | Break triggered | P0 |
| 下单rpc接口5分钟调用>200次且比上周+60% | Traffic | Anomaly detected | P1 |
| 支付rpc接口5分钟调用>200次且比上周+60% | Traffic | Anomaly detected | P1 |
| 注册rpc接口5分钟调用>100次且比上周+60% | Traffic | Anomaly detected | P1 |
| 登录rpc接口5分钟调用>100次且比上周+60% | Traffic | Anomaly detected | P1 |
| 短信rpc接口5分钟调用>100次且比上周+60% | Traffic | Anomaly detected | P1 |

---

### SMS/UPUSH Alerts

| Alert Name | Metric Type | Condition | Priority |
|------------|-------------|-----------|----------|
| 五分钟短信供应商调用失败超过阈值50 | API | >50 failures in 5min | P1 |
| 五分钟短信供应商返回值失败超过阈值200 | API | >200 return failures | P1 |
| 营销短信回执成功率低于60% | Success Rate | <60% | P2 |
| 营销短信过滤数超过100 | Filter | >100 filtered | P2 |
| 行业短信回执成功率低于70% | Success Rate | <70% | P1 |
| 行业短信过滤数超过50 | Filter | >50 filtered | P2 |
| 验证码发送量同比增加30% | Volume | +30% YoY | P2 |
| 验证码回执成功率低于70% | Success Rate | <70% | P1 |
| 验证码过滤数超过50 | Filter | >50 filtered | P2 |

---

### DataLink Pipeline Alerts

| Alert Name | Type | Time | Priority |
|------------|------|------|----------|
| 任务延迟告警(夜晚) | Delay | Night | P2 |
| 任务异常告警(夜晚) | Exception | Night | P2 |
| 普通任务延迟(白天) | Delay | Day | P3 |
| 普通任务异常(白天) | Exception | Day | P3 |
| 离线普通任务延迟(白天) | Delay | Day | P3 |
| 离线普通任务异常(白天) | Exception | Day | P3 |
| 离线核心任务延迟(白天) | Delay | Day | P1 |
| 离线核心任务异常(白天) | Exception | Day | P1 |
| 离线重要任务延迟(白天) | Delay | Day | P2 |
| 离线重要任务异常(白天) | Exception | Day | P2 |
| 重要任务延迟(白天) | Delay | Day | P2 |
| 重要任务异常(白天) | Exception | Day | P2 |
| 黄金流程任务延迟(白天) | Delay | Day | P0 |
| 黄金流程任务异常(白天) | Exception | Day | P0 |

---

### Network & Gateway Alerts

| Alert Name | Metric Type | Condition | Priority |
|------------|-------------|-----------|----------|
| 【网关告警】错误率大于15% | Errors | >15% error rate | P0 |
| 【网络质量US-机房互拨】探测目标连续15s失败 | Connectivity | 15s probe failure | P0 |

---

### Priority Level Alerts

| Alert Name | Description | Priority |
|------------|-------------|----------|
| [LCP-Prod-P0] | LCP Production Critical Alerts | P0 |
| [LCP-Prod-P1] | LCP Production High Priority Alerts | P1 |
| [LCP-Prod-P2] | LCP Production Medium Priority Alerts | P2 |
| [LCP-Prod-P3] | LCP Production Low Priority Alerts | P3 |

---

## Contact Points

| Name | Type | UID |
|------|------|-----|
| email receiver | email | ff46tgx17x7cwa |

---

## Notification Summary

- **Total Contact Points:** 1
- **Notification Method:** Email
- **Default Routing:** All alerts routed to email receiver

---

*Document generated automatically by Grafana Alert Discovery System*
