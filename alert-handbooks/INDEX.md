# Luckin Coffee USA - Alert Response Handbook Index
# 瑞幸咖啡美国 - 告警响应手册索引

> **Version:** 1.0
> **Generated:** 2026-01-14
> **Total Alerts:** 135
> **Document Owner:** DevOps Team

---

## Quick Navigation 快速导航

- [Priority Level Alerts 优先级聚合告警](#priority-level-alerts-优先级聚合告警)
- [DataLink Pipeline Alerts 数据链路告警](#datalink-pipeline-alerts-数据链路告警)
- [Database - RDS MySQL Alerts 数据库-RDS告警](#database---rds-mysql-alerts-数据库-rds告警)
- [Database - MongoDB Alerts 数据库-MongoDB告警](#database---mongodb-alerts-数据库-mongodb告警)
- [Database - OpenSearch Alerts 数据库-ES告警](#database---opensearch-alerts-数据库-es告警)
- [Database - Redis Alerts 数据库-Redis告警](#database---redis-alerts-数据库-redis告警)
- [Database - Exporter Alerts 数据库-导出器告警](#database---exporter-alerts-数据库-导出器告警)
- [SMS/UPUSH Alerts 短信/推送告警](#smsupush-alerts-短信推送告警)
- [APM/iZeus Strategy Alerts APM策略告警](#apizeus-strategy-alerts-apm策略告警)
- [APM/iZeus Infrastructure Alerts APM基础设施告警](#apizeus-infrastructure-alerts-apm基础设施告警)
- [Default Strategy Alerts 默认策略告警](#default-strategy-alerts-默认策略告警)
- [Pod/Container Alerts 容器告警](#podcontainer-alerts-容器告警)
- [VM/Host Alerts 虚拟机告警](#vmhost-alerts-虚拟机告警)
- [Business Alerts 业务告警](#business-alerts-业务告警)
- [Risk Control Alerts 风控告警](#risk-control-alerts-风控告警)
- [Gateway/Network Alerts 网关/网络告警](#gatewaynetwork-alerts-网关网络告警)
- [Grafana Native Alerts Grafana原生告警](#grafana-native-alerts-grafana原生告警)

---

## Response Time Quick Reference 响应时间快速参考

| Priority | Service Level | Response Time | Description |
|----------|---------------|---------------|-------------|
| **P0** | L0 | **IMMEDIATE (< 5 min)** | 核心业务关键 Core Business Critical |
| **P1** | L0/L1 | **HIGH (< 15 min)** | 重要服务 Important Services |
| **P2** | L1/L2 | **STANDARD (< 30 min)** | 标准优先级 Standard Priority |
| **P3** | L2 | **LOW (< 2 hr)** | 低优先级 Low Priority |

---

## Escalation Matrix 升级矩阵

| Team | Chinese | Domain | On-Call | Slack |
|------|---------|--------|---------|-------|
| DBA | 数据库管理 | All Databases | dba-oncall@luckin.com | #dba-alerts |
| SRE | SRE | Infrastructure | sre-oncall@luckin.com | #sre-alerts |
| DevOps | 运维开发 | CI/CD, Containers | devops-oncall@luckin.com | #devops-alerts |
| Sales | 销售业务 | Orders, Payments | sales-oncall@luckin.com | #sales-alerts |
| RiskControl | 风控 | Fraud Prevention | risk-oncall@luckin.com | #risk-control-alerts |
| MiddlePlatform | 中台 | SMS, MDM | middle-oncall@luckin.com | #middle-platform-alerts |
| CommonMonitor | 监控平台 | iZeus, Grafana | monitor-oncall@luckin.com | #monitoring-alerts |
| MicroService | 微服务 | Gateway, Nacos | microservice-oncall@luckin.com | #microservice-alerts |
| ArchitectureData | 架构数据 | DataLink | arch-oncall@luckin.com | #architecture-alerts |
| StoragePlatform | 存储平台 | Redis Cloud | storage-oncall@luckin.com | #storage-alerts |

---

## Priority Level Alerts 优先级聚合告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-001 | [LCP-Prod-P0] | P0 | SRE | [View](./ALR-001_LCP-Prod-P0.md) |
| ALR-002 | [LCP-Prod-P1] | P1 | SRE | [View](./ALR-002_LCP-Prod-P1.md) |
| ALR-003 | [LCP-Prod-P2] | P2 | SRE | [View](./ALR-003_LCP-Prod-P2.md) |
| ALR-004 | [LCP-Prod-P3] | P3 | SRE | [View](./ALR-004_LCP-Prod-P3.md) |

---

## DataLink Pipeline Alerts 数据链路告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-005 | datalink黄金流程任务延迟(白天) | P0 | ArchitectureData | [View](./ALR-005_datalink-golden-flow-delay-day.md) |
| ALR-006 | datalink黄金流程任务异常(白天) | P0 | ArchitectureData | [View](./ALR-006_datalink-golden-flow-exception-day.md) |
| ALR-007 | datalink离线核心任务延迟(白天) | P1 | ArchitectureData | [View](./ALR-007_datalink-offline-core-delay-day.md) |
| ALR-008 | datalink离线核心任务异常(白天) | P1 | ArchitectureData | [View](./ALR-008_datalink-offline-core-exception-day.md) |
| ALR-009 | datalink重要任务延迟(白天) | P2 | ArchitectureData | [View](./ALR-009_datalink-important-delay-day.md) |
| ALR-010 | datalink重要任务异常(白天) | P2 | ArchitectureData | [View](./ALR-010_datalink-important-exception-day.md) |
| ALR-011 | datalink离线重要任务延迟(白天) | P2 | ArchitectureData | [View](./ALR-011_datalink-offline-important-delay-day.md) |
| ALR-012 | datalink离线重要任务异常(白天) | P2 | ArchitectureData | [View](./ALR-012_datalink-offline-important-exception-day.md) |
| ALR-013 | datalink任务延迟告警(夜晚) | P2 | ArchitectureData | [View](./ALR-013_datalink-task-delay-night.md) |
| ALR-014 | datalink任务异常告警(夜晚) | P2 | ArchitectureData | [View](./ALR-014_datalink-task-exception-night.md) |
| ALR-015 | datalink普通任务延迟(白天) | P3 | ArchitectureData | [View](./ALR-015_datalink-regular-delay-day.md) |
| ALR-016 | datalink普通任务异常(白天) | P3 | ArchitectureData | [View](./ALR-016_datalink-regular-exception-day.md) |
| ALR-017 | datalink离线普通任务延迟(白天) | P3 | ArchitectureData | [View](./ALR-017_datalink-offline-regular-delay-day.md) |
| ALR-018 | datalink离线普通任务异常(白天) | P3 | ArchitectureData | [View](./ALR-018_datalink-offline-regular-exception-day.md) |

---

## Database - RDS MySQL Alerts 数据库-RDS告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-019 | 【DB告警】AWS-RDS CPU使用率连续三分钟大于90% | P1 | DBA | [View](./ALR-019_db-rds-cpu-90-3min-v1.md) |
| ALR-020 | 【DB告警】AWS RDS CPU使用率连续三分钟大于90% | P1 | DBA | [View](./ALR-020_db-rds-cpu-90-3min-v2.md) |
| ALR-021 | 【DB告警】AWS RDS Vip 持续一分钟不通 | P0 | DBA | [View](./ALR-021_db-rds-vip-unreachable.md) |
| ALR-022 | 【DB告警】AWS RDS Vip 持续一分钟不通_语音 | P0 | DBA | [View](./ALR-022_db-rds-vip-unreachable-voice.md) |
| ALR-023 | 【DB告警】AWS RDS 发生重启或者主从切换 | P0 | DBA | [View](./ALR-023_db-rds-failover-restart.md) |
| ALR-024 | 【DB告警】AWS RDS 发生重启或者主从切换_语音 | P0 | DBA | [View](./ALR-024_db-rds-failover-restart-voice.md) |
| ALR-025 | 【DB告警】AWS RDS 慢查询数量持续三分钟大于300个 | P2 | DBA | [View](./ALR-025_db-rds-slow-queries-300-v1.md) |
| ALR-026 | 【DB告警】AWS-RDS 慢查询数量持续三分钟大于300个 | P2 | DBA | [View](./ALR-026_db-rds-slow-queries-300-v2.md) |
| ALR-027 | 【DB告警】AWS RDS 活跃线程持续两分钟大于24 | P2 | DBA | [View](./ALR-027_db-rds-active-threads-24-v1.md) |
| ALR-028 | 【DB告警】AWS-RDS 活跃线程持续两分钟大于24 | P2 | DBA | [View](./ALR-028_db-rds-active-threads-24-v2.md) |
| ALR-029 | 【DB告警】AWS RDS 磁盘空间连续3分钟不足10G | P1 | DBA | [View](./ALR-029_db-rds-disk-low-10g.md) |

---

## Database - MongoDB Alerts 数据库-MongoDB告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-030 | 【DB告警】AWS Mongo CPU使用率连续三分钟大于90% | P1 | DBA | [View](./ALR-030_db-mongo-cpu-90.md) |
| ALR-031 | 【DB告警】AWS Mongo CPU使用率连续三分钟大于90%_语音 | P0 | DBA | [View](./ALR-031_db-mongo-cpu-90-voice.md) |
| ALR-032 | 【DB告警】AWS Mongo 可用内存连续三分钟不足500M | P1 | DBA | [View](./ALR-032_db-mongo-memory-500m.md) |

---

## Database - OpenSearch Alerts 数据库-ES告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-033 | 【DB告警】AWS-ES CPU 使用率大于90% | P1 | DBA | [View](./ALR-033_db-es-cpu-90.md) |
| ALR-034 | 【DB告警】AWS-ES CPU 使用率大于90%_语音 | P0 | DBA | [View](./ALR-034_db-es-cpu-90-voice.md) |
| ALR-035 | 【DB告警】AWS-ES 集群状态Red | P0 | DBA | [View](./ALR-035_db-es-cluster-red.md) |
| ALR-036 | 【DB告警】AWS-ES 集群状态Red_语音 | P0 | DBA | [View](./ALR-036_db-es-cluster-red-voice.md) |
| ALR-037 | 【DB告警】AWS-ES 集群状态Yellow | P2 | DBA | [View](./ALR-037_db-es-cluster-yellow.md) |
| ALR-038 | 【DB告警】AWS-ES磁盘空间不足10G | P1 | DBA | [View](./ALR-038_db-es-disk-10g.md) |
| ALR-039 | 【DB告警】AWS-ES磁盘空间不足10G_语音 | P0 | DBA | [View](./ALR-039_db-es-disk-10g-voice.md) |

---

## Database - Redis Alerts 数据库-Redis告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-040 | 【DB告警】AWS Redis CPU使用率大于90% | P1 | StoragePlatform | [View](./ALR-040_db-redis-cpu-90.md) |
| ALR-041 | 【DB告警】Redis CPU使用率持续3分钟超过70% | P2 | StoragePlatform | [View](./ALR-041_db-redis-cpu-70-3min.md) |
| ALR-042 | 【DB告警】Redis 内存使用率持续3分钟超过70% | P2 | StoragePlatform | [View](./ALR-042_db-redis-memory-70.md) |
| ALR-043 | 【DB告警】Redis 发生客户端堵塞 | P1 | StoragePlatform | [View](./ALR-043_db-redis-client-blocked.md) |
| ALR-044 | 【DB告警】Redis 实例命令平均时延大于2ms | P2 | StoragePlatform | [View](./ALR-044_db-redis-latency-2ms.md) |
| ALR-045 | 【DB告警】Redis 实例客户端nomal缓冲超过32m | P2 | StoragePlatform | [View](./ALR-045_db-redis-buffer-32m.md) |
| ALR-046 | 【DB告警】Redis 实例流量大于32Mbps | P2 | StoragePlatform | [View](./ALR-046_db-redis-traffic-32mbps.md) |
| ALR-047 | 【DB告警】Redis 实例触发key淘汰 | P2 | StoragePlatform | [View](./ALR-047_db-redis-key-eviction.md) |
| ALR-048 | 【DB告警】Redis 实例连接数使用率大于30% | P2 | StoragePlatform | [View](./ALR-048_db-redis-connections-30.md) |
| ALR-049 | 【DB告警】Redis 实例采集失败请检查是否存活 | P0 | StoragePlatform | [View](./ALR-049_db-redis-collection-failed.md) |

---

## Database - Exporter Alerts 数据库-导出器告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-050 | 【DB告警】exporter 进程异常 | P0 | DBA | [View](./ALR-050_db-exporter-abnormal.md) |

---

## SMS/UPUSH Alerts 短信/推送告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-051 | 【UPUSH】【北美】五分钟短信供应商调用失败超过阈值 50 | P1 | MiddlePlatform | [View](./ALR-051_upush-sms-provider-failures-50.md) |
| ALR-052 | 【UPUSH】【北美】五分钟短信供应商返回值失败超过阈值 200 | P1 | MiddlePlatform | [View](./ALR-052_upush-sms-return-failures-200.md) |
| ALR-053 | 【UPUSH】【北美】营销短信回执成功率低于 60% | P2 | MiddlePlatform | [View](./ALR-053_upush-marketing-receipt-60.md) |
| ALR-054 | 【UPUSH】【北美】营销短信过滤数超过 100 | P2 | MiddlePlatform | [View](./ALR-054_upush-marketing-filtered-100.md) |
| ALR-055 | 【UPUSH】【北美】行业短信回执成功率低于 70% | P1 | MiddlePlatform | [View](./ALR-055_upush-industry-receipt-70.md) |
| ALR-056 | 【UPUSH】【北美】行业短信过滤数超过 50 | P2 | MiddlePlatform | [View](./ALR-056_upush-industry-filtered-50.md) |
| ALR-057 | 【UPUSH】【北美】验证码发送量同比增加 30% | P2 | MiddlePlatform | [View](./ALR-057_upush-verification-volume-30.md) |
| ALR-058 | 【UPUSH】【北美】验证码回执成功率低于 70% | P1 | MiddlePlatform | [View](./ALR-058_upush-verification-receipt-70.md) |
| ALR-059 | 【UPUSH】【北美】验证码过滤数超过 50 | P2 | MiddlePlatform | [View](./ALR-059_upush-verification-filtered-50.md) |

---

## APM/iZeus Strategy Alerts APM策略告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-060 | 【iZeus-策略1】-服务每分钟异常数大于2 | P2 | CommonMonitor | [View](./ALR-060_izeus-strategy1-exceptions-2.md) |
| ALR-061 | 【iZeus-策略2】-服务每分钟异常数大于2 | P2 | CommonMonitor | [View](./ALR-061_izeus-strategy2-exceptions-2.md) |
| ALR-062 | 【iZeus-策略3】-服务每分钟异常数大于2 | P2 | CommonMonitor | [View](./ALR-062_izeus-strategy3-exceptions-2.md) |
| ALR-063 | 【iZeus-策略4】-服务每分钟异常数大于2 | P2 | CommonMonitor | [View](./ALR-063_izeus-strategy4-exceptions-2.md) |
| ALR-064 | 【iZeus-策略5】-服务每分钟异常数大于3 | P2 | CommonMonitor | [View](./ALR-064_izeus-strategy5-exceptions-3.md) |
| ALR-065 | 【iZeus-策略6】-服务每分钟异常数大于2 | P2 | CommonMonitor | [View](./ALR-065_izeus-strategy6-exceptions-2.md) |
| ALR-066 | 【iZeus-策略7】-服务每分钟异常数大于2 | P2 | CommonMonitor | [View](./ALR-066_izeus-strategy7-exceptions-2.md) |
| ALR-067 | 【iZeus-策略8】-服务每分钟异常数大于2 | P2 | CommonMonitor | [View](./ALR-067_izeus-strategy8-exceptions-2.md) |
| ALR-068 | 【iZeus-策略9】-服务每分钟异常数大于2 | P2 | CommonMonitor | [View](./ALR-068_izeus-strategy9-exceptions-2.md) |
| ALR-069 | 【iZeus-策略10】-JVM CPU使用率大于20 | P2 | CommonMonitor | [View](./ALR-069_izeus-strategy10-jvm-cpu-20.md) |
| ALR-070 | 【iZeus-策略10】-服务响应时间（ms）大于1500 | P2 | CommonMonitor | [View](./ALR-070_izeus-strategy10-response-1500.md) |
| ALR-071 | 【iZeus-策略11】-端点每分钟失败数大于等于1 | P2 | CommonMonitor | [View](./ALR-071_izeus-strategy11-endpoint-1.md) |
| ALR-072 | 【iZeus-策略12】-端点每分钟失败数大于等于1 | P2 | CommonMonitor | [View](./ALR-072_izeus-strategy12-endpoint-1.md) |
| ALR-073 | 【iZeus-策略15】-服务每分钟异常数大于3 | P2 | CommonMonitor | [View](./ALR-073_izeus-strategy15-exceptions-3.md) |
| ALR-074 | 【iZeus-策略16】-端点每分钟失败数大于2 | P2 | CommonMonitor | [View](./ALR-074_izeus-strategy16-endpoint-2.md) |
| ALR-075 | 【iZeus-策略17】-端点每分钟失败数大于3 | P2 | CommonMonitor | [View](./ALR-075_izeus-strategy17-endpoint-3.md) |

---

## APM/iZeus Infrastructure Alerts APM基础设施告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-076 | 【iZeus】Node-CPU-85 | P1 | CommonMonitor | [View](./ALR-076_izeus-node-cpu-85.md) |
| ALR-077 | 【iZeus】Node-Disk-85 | P1 | CommonMonitor | [View](./ALR-077_izeus-node-disk-85.md) |
| ALR-078 | 【iZeus】Node-Memory-95 | P1 | CommonMonitor | [View](./ALR-078_izeus-node-memory-95.md) |
| ALR-079 | 【iZeus】OAP-FGC-5 | P2 | CommonMonitor | [View](./ALR-079_izeus-oap-fgc-5.md) |
| ALR-080 | 【iZeus】Storage-Receiver2Thanos-Receiver-0 | P1 | CommonMonitor | [View](./ALR-080_izeus-storage-thanos-0.md) |
| ALR-081 | 【iZeus】Storage-Receiver2VM-0 | P1 | CommonMonitor | [View](./ALR-081_izeus-storage-vm-0.md) |
| ALR-082 | 【iZeus】Transfer-Agent2OAP-0 | P1 | CommonMonitor | [View](./ALR-082_izeus-transfer-agent-oap-0.md) |
| ALR-083 | 【iZeus】Transfer-OAP2OAP-0 | P1 | CommonMonitor | [View](./ALR-083_izeus-transfer-oap-oap-0.md) |
| ALR-084 | 【iZeus】Transfer-OAPTrace2Receiver-0 | P1 | CommonMonitor | [View](./ALR-084_izeus-transfer-trace-receiver-0.md) |

---

## Default Strategy Alerts 默认策略告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-085 | 【默认策略】FGC次数大于0或YGC耗时大于500毫秒 | P2 | DevOps | [View](./ALR-085_default-jvm-gc.md) |
| ALR-086 | 【默认策略】异常okhttp总数大于等于50 | P2 | DevOps | [View](./ALR-086_default-okhttp-50.md) |
| ALR-087 | 【默认策略】服务器每分钟异常数大于20 | P1 | DevOps | [View](./ALR-087_default-exceptions-20.md) |
| ALR-088 | 【默认策略】服务器每分钟异常数大于5 | P2 | DevOps | [View](./ALR-088_default-exceptions-5.md) |

---

## Pod/Container Alerts 容器告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-089 | 【pod-cpu-兜底】P0 CPU使用率连续3分钟大于85% | P0 | DevOps | [View](./ALR-089_pod-cpu-fallback-85.md) |
| ALR-090 | 【pod-cpu】P0 CPU使用率连续10分钟大于50% | P0 | DevOps | [View](./ALR-090_pod-cpu-50-10min.md) |
| ALR-091 | 【pod-cpu】P0 CPU使用率连续3分钟大于70% | P0 | DevOps | [View](./ALR-091_pod-cpu-70-3min.md) |
| ALR-092 | 【pod-全局】P0 node节点up心跳丢失需检查节点是否宕机 | P0 | SRE | [View](./ALR-092_pod-node-heartbeat-lost.md) |
| ALR-093 | 【pod-全局】P0 Pod 2m内发生重启请关注 | P0 | DevOps | [View](./ALR-093_pod-restart-2min.md) |
| ALR-094 | 【pod-宕机】P1 WSS内存使用率连续3分钟等于100% | P1 | DevOps | [View](./ALR-094_pod-memory-oom.md) |
| ALR-095 | 【pod-线程】P0 容器线程数连续3分钟超过3600 | P0 | DevOps | [View](./ALR-095_pod-threads-3600.md) |
| ALR-096 | 【pod-网卡】P0 分区写入速率连续3分钟大于50MBs | P0 | DevOps | [View](./ALR-096_pod-io-write-50mb.md) |
| ALR-097 | 【pod-网卡】P0 分区读取速率连续3分钟大于50MBs | P0 | DevOps | [View](./ALR-097_pod-io-read-50mb.md) |
| ALR-098 | 【pod-网卡】P0 网卡流入速率连续3分钟大于30MBs | P0 | DevOps | [View](./ALR-098_pod-network-ingress-30mb.md) |
| ALR-099 | 【pod-网卡】P0 网卡流出速率连续3分钟大于30MBs | P0 | DevOps | [View](./ALR-099_pod-network-egress-30mb.md) |

---

## VM/Host Alerts 虚拟机告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-100 | 【vm-CPU】P1 CPU平均负载大于CPU核心数量的1倍已持续5分钟 | P1 | SRE | [View](./ALR-100_vm-cpu-load-1x.md) |
| ALR-101 | 【vm-CPU】P1 服务整体CPU平均使用率超过80% | P1 | SRE | [View](./ALR-101_vm-cpu-avg-80.md) |
| ALR-102 | 【vm-cpu】P0 5分钟内服务CPU_iowait每秒的使用率大于80% | P0 | SRE | [View](./ALR-102_vm-cpu-iowait-80.md) |
| ALR-103 | 【vm-cpu】P0 服务CPU使用率窃取大于10% | P0 | SRE | [View](./ALR-103_vm-cpu-steal-10.md) |
| ALR-104 | 【vm-fileSystem】P0 分区inodes使用率大于95%请立即处理 | P0 | SRE | [View](./ALR-104_vm-inodes-95.md) |
| ALR-105 | 【vm-fileSystem】P0 分区发送只读事件请检查分区读写情况 | P0 | SRE | [View](./ALR-105_vm-filesystem-readonly.md) |
| ALR-106 | 【vm-io】P0 服务io耗时大于90ms且同比超过20ms | P0 | SRE | [View](./ALR-106_vm-io-latency-90ms.md) |
| ALR-107 | 【vm-io】P1 磁盘IO使用率大于70%且同比超过20 | P1 | SRE | [View](./ALR-107_vm-io-usage-70.md) |
| ALR-108 | 【vm-tcp】P0 TCP每秒重传报文数超过200 | P0 | SRE | [View](./ALR-108_vm-tcp-retransmits-200.md) |
| ALR-109 | 【vm-内存】P1 内存使用率大于90% 持续10分钟 | P1 | SRE | [View](./ALR-109_vm-memory-90-10min.md) |
| ALR-110 | 【vm-宕机】P0 up监控指标心跳丢失10分钟需检查设备是否宕机 | P0 | SRE | [View](./ALR-110_vm-heartbeat-lost-10min.md) |
| ALR-111 | 【vm-磁盘】P1 分区使用率大于90%请手动处理 | P1 | SRE | [View](./ALR-111_vm-disk-90.md) |
| ALR-112 | 【vm-网卡】P0 入方向在5分钟内每秒丢弃的数据包大于20个 | P0 | SRE | [View](./ALR-112_vm-network-drop-in-20.md) |
| ALR-113 | 【vm-网卡】P0 入方向在5分钟内每秒错误的数据包大于20个 | P0 | SRE | [View](./ALR-113_vm-network-error-in-20.md) |
| ALR-114 | 【vm-网卡】P0 出方向在5分钟内每秒丢弃的数据包大于20个 | P0 | SRE | [View](./ALR-114_vm-network-drop-out-20.md) |
| ALR-115 | 【vm-网卡】P0 出方向在5分钟内每秒错误的数据包大于20个 | P0 | SRE | [View](./ALR-115_vm-network-error-out-20.md) |
| ALR-116 | 【vm-网卡】P0 网卡状态为down | P0 | SRE | [View](./ALR-116_vm-nic-down.md) |

---

## Business Alerts 业务告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-117 | 【北美-业务告警】取消订单持续5分钟大于1单 | P1 | Sales | [View](./ALR-117_business-cancelled-orders.md) |
| ALR-118 | 【北美-业务告警】新建-付款-完成订单持续10分钟少于1单 | P0 | Sales | [View](./ALR-118_business-complete-orders-0.md) |
| ALR-119 | 【北美-业务告警】订单支持持续10分钟小于1 | P0 | Sales | [View](./ALR-119_business-order-support-0.md) |
| ALR-120 | 【北美-业务告警】过去10分钟注册数为0 | P0 | Sales | [View](./ALR-120_business-registrations-0.md) |
| ALR-121 | 【北美-业务告警】过去5分钟支付金额小于500分 | P0 | Sales | [View](./ALR-121_business-payments-500.md) |

---

## Risk Control Alerts 风控告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-122 | 【北美亚风控】全局策略熔断前预告警 | P1 | RiskControl | [View](./ALR-122_risk-global-prebreak.md) |
| ALR-123 | 【北美亚风控】全局策略熔断告警 | P0 | RiskControl | [View](./ALR-123_risk-global-break.md) |
| ALR-124 | 【北美亚风控】场景熔断前预告警 | P1 | RiskControl | [View](./ALR-124_risk-scene-prebreak.md) |
| ALR-125 | 【北美风控】场景熔断告警 | P0 | RiskControl | [View](./ALR-125_risk-scene-break.md) |
| ALR-126 | 【国际化北美风控】下单rpc接口最近5分钟调用总量超过200次且比上周同时段多60% | P1 | RiskControl | [View](./ALR-126_risk-order-rpc-spike.md) |
| ALR-127 | 【国际化北美风控】支付rpc接口最近5分钟调用总量超过200次且比上周同时段多60% | P1 | RiskControl | [View](./ALR-127_risk-payment-rpc-spike.md) |
| ALR-128 | 【国际化北美风控】注册rpc接口最近5分钟调用总量超过100次且比上周同时段多60% | P1 | RiskControl | [View](./ALR-128_risk-register-rpc-spike.md) |
| ALR-129 | 【国际化北美风控】登录rpc接口最近5分钟调用总量超过100次且比上周同时段多60% | P1 | RiskControl | [View](./ALR-129_risk-login-rpc-spike.md) |
| ALR-130 | 【国际化北美风控】短信rpc接口最近5分钟调用总量超过100次且比上周同时段多60% | P1 | RiskControl | [View](./ALR-130_risk-sms-rpc-spike.md) |

---

## Gateway/Network Alerts 网关/网络告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-131 | 【网关告警】错误率大于15% | P0 | MicroService | [View](./ALR-131_gateway-error-rate-15.md) |
| ALR-132 | 【网络质量US-机房互拨】探测目标连续15s失败 | P0 | SRE | [View](./ALR-132_network-probe-failed-15s.md) |

---

## Grafana Native Alerts Grafana原生告警

| ID | Alert Name | Priority | Team | Handbook |
|----|------------|----------|------|----------|
| ALR-133 | Slow Query Spike - High Rate Alert | P2 | DBA | [View](./ALR-133_grafana-slow-query-spike.md) |
| ALR-134 | Slow Query Critical - Very High Rate Alert | P1 | DBA | [View](./ALR-134_grafana-slow-query-critical.md) |
| ALR-135 | Slow Query Weekly Increase - WoW Spike Alert | P2 | DBA | [View](./ALR-135_grafana-slow-query-weekly.md) |

---

## Statistics Summary 统计摘要

### By Priority 按优先级分布

| Priority | Count | Percentage |
|----------|-------|------------|
| P0 | 45 | 33.3% |
| P1 | 41 | 30.4% |
| P2 | 42 | 31.1% |
| P3 | 7 | 5.2% |

### By Category 按类别分布

| Category | Count |
|----------|-------|
| Database Alerts | 32 |
| Pod/Container Alerts | 11 |
| VM/Host Alerts | 17 |
| APM/iZeus Alerts | 25 |
| DataLink Alerts | 14 |
| Business Alerts | 5 |
| Risk Control Alerts | 9 |
| SMS/UPUSH Alerts | 9 |
| Gateway/Network Alerts | 2 |
| Default Strategy Alerts | 4 |
| Priority Level Alerts | 4 |
| Grafana Native Alerts | 3 |

### By Team 按团队分布

| Team | Alert Count |
|------|-------------|
| DBA | 25 |
| SRE | 21 |
| DevOps | 15 |
| CommonMonitor | 25 |
| ArchitectureData | 14 |
| StoragePlatform | 10 |
| MiddlePlatform | 9 |
| RiskControl | 9 |
| Sales | 5 |
| MicroService | 1 |

---

## Appendices 附录

### Appendix A: AWS CLI Quick Reference
See [AWS_CLI_REFERENCE.md](./AWS_CLI_REFERENCE.md) for commonly used AWS CLI commands.

### Appendix B: Kubernetes Commands Quick Reference
See [KUBERNETES_COMMANDS.md](./KUBERNETES_COMMANDS.md) for commonly used kubectl commands.

### Appendix C: Database Diagnostic Queries
See [DATABASE_DIAGNOSTICS.md](./DATABASE_DIAGNOSTICS.md) for database-specific diagnostic queries.

### Appendix D: Grafana Dashboard Reference
See [GRAFANA_DASHBOARDS.md](./GRAFANA_DASHBOARDS.md) for dashboard references.

---

## Document History 文档历史

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-14 | DevOps Team | Initial creation of 135 alert handbooks |

---

> **Note:** This index is automatically generated. For individual alert handbooks, click the "View" links in the tables above.
>
> **备注:** 此索引为自动生成。如需查看单个告警手册，请点击上表中的"View"链接。
