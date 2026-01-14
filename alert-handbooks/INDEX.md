# 瑞幸咖啡美国运维告警响应参考手册

> **本手册为参考文档，请根据实际情况灵活处理。**

---

## 快速导航

| 类别 | 数量 | 说明 |
|------|------|------|
| [优先级告警](#优先级告警) | 4 | P0-P3优先级路由 |
| [数据链路告警](#数据链路告警) | 14 | ETL/数据同步监控 |
| [数据库-RDS告警](#数据库-rds告警) | 11 | MySQL/Aurora监控 |
| [数据库-MongoDB告警](#数据库-mongodb告警) | 3 | DocumentDB监控 |
| [数据库-OpenSearch告警](#数据库-opensearch告警) | 7 | Elasticsearch监控 |
| [数据库-Redis告警](#数据库-redis告警) | 10 | ElastiCache监控 |
| [数据库-Exporter告警](#数据库-exporter告警) | 1 | 数据库Exporter |
| [SMS-UPUSH告警](#sms-upush告警) | 9 | 短信推送服务监控 |
| [APM-iZeus策略告警](#apm-izeus策略告警) | 16 | 应用性能监控 |
| [APM-iZeus基础设施告警](#apm-izeus基础设施告警) | 9 | APM基础设施 |
| [默认策略告警](#默认策略告警) | 4 | 基础监控 |
| [Pod/容器告警](#pod容器告警) | 11 | Kubernetes工作负载 |
| [VM/主机告警](#vm主机告警) | 17 | EC2实例监控 |
| [业务告警](#业务告警) | 5 | 业务逻辑监控 |
| [风控告警](#风控告警) | 9 | 风控系统监控 |
| [网关告警](#网关告警) | 1 | API网关监控 |
| [网络告警](#网络告警) | 1 | 网络连接监控 |
| [Grafana告警](#grafana告警) | 3 | Grafana原生告警 |

---

## 响应时间参考

| 优先级 | 响应时间 | 说明 |
|--------|----------|------|
| **P0** | < 5分钟 | 立即响应，可能需要唤醒中国团队 |
| **P1** | < 15分钟 | 快速响应 |
| **P2** | < 30分钟 | 标准响应 |
| **P3** | < 2小时 | 低优先级响应 |

---

## 黄金流程说明

**黄金流程** 是指用户在瑞幸咖啡App上完成下单的核心流程：

1. 打开App → 2. 浏览菜单 → 3. 选择商品 → 4. 提交订单 → 5. 完成支付

**如果黄金流程受影响（用户无法下单），这是严重事故，需要立即唤醒所有相关团队成员处理。**

---

## 升级标准

| 条件 | 升级目标 |
|------|---------|
| 初次响应无法解决 | DevOps值班成员 |
| 问题持续恶化 | Team Lead |
| 需要外部支持 | AWS/供应商支持 |

---

## 优先级告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-001 | [[LCP-Prod-P0] P0级别告警](ALR-001_[LCP-Prod-P0].md) | P0 |
| ALR-002 | [[LCP-Prod-P1] P1级别告警](ALR-002_[LCP-Prod-P1].md) | P1 |
| ALR-003 | [[LCP-Prod-P2] P2级别告警](ALR-003_[LCP-Prod-P2].md) | P2 |
| ALR-004 | [[LCP-Prod-P3] P3级别告警](ALR-004_[LCP-Prod-P3].md) | P3 |

---

## 数据链路告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-005 | [黄金流程日间-延迟告警](ALR-005_datalink-golden-flow-delay-day.md) | P0 |
| ALR-006 | [黄金流程日间-异常告警](ALR-006_datalink-golden-flow-exception-day.md) | P0 |
| ALR-007 | [离线核心日间-延迟告警](ALR-007_datalink-offline-core-delay-day.md) | P0 |
| ALR-008 | [离线核心日间-异常告警](ALR-008_datalink-offline-core-exception-day.md) | P0 |
| ALR-009 | [重要任务日间-延迟告警](ALR-009_datalink-important-delay-day.md) | P1 |
| ALR-010 | [重要任务日间-异常告警](ALR-010_datalink-important-exception-day.md) | P1 |
| ALR-011 | [离线重要日间-延迟告警](ALR-011_datalink-offline-important-delay-day.md) | P1 |
| ALR-012 | [离线重要日间-异常告警](ALR-012_datalink-offline-important-exception-day.md) | P1 |
| ALR-013 | [任务夜间-延迟告警](ALR-013_datalink-task-delay-night.md) | P2 |
| ALR-014 | [任务夜间-异常告警](ALR-014_datalink-task-exception-night.md) | P2 |
| ALR-015 | [常规任务日间-延迟告警](ALR-015_datalink-regular-delay-day.md) | P2 |
| ALR-016 | [常规任务日间-异常告警](ALR-016_datalink-regular-exception-day.md) | P2 |
| ALR-017 | [离线常规日间-延迟告警](ALR-017_datalink-offline-regular-delay-day.md) | P2 |
| ALR-018 | [离线常规日间-异常告警](ALR-018_datalink-offline-regular-exception-day.md) | P2 |

---

## 数据库-RDS告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-019 | [AWS-RDS CPU使用率连续三分钟大于90%](ALR-019_db-rds-cpu-90-3min-v1.md) | P1 |
| ALR-020 | [AWS RDS CPU使用率连续三分钟大于90%](ALR-020_db-rds-cpu-90-3min-v2.md) | P1 |
| ALR-021 | [AWS RDS Vip 持续一分钟不通](ALR-021_db-rds-vip-unreachable.md) | P0 |
| ALR-022 | [AWS RDS Vip 持续一分钟不通 (Voice)](ALR-022_db-rds-vip-unreachable-voice.md) | P0 |
| ALR-023 | [AWS RDS Failover或重启](ALR-023_db-rds-failover-restart.md) | P0 |
| ALR-024 | [AWS RDS Failover或重启 (Voice)](ALR-024_db-rds-failover-restart-voice.md) | P0 |
| ALR-025 | [AWS-RDS 慢查询数量持续三分钟大于300个](ALR-025_db-rds-slow-queries-300-v1.md) | P1 |
| ALR-026 | [AWS RDS 慢查询数量持续三分钟大于300个](ALR-026_db-rds-slow-queries-300-v2.md) | P1 |
| ALR-027 | [AWS-RDS 活跃线程持续两分钟大于24](ALR-027_db-rds-active-threads-24-v1.md) | P1 |
| ALR-028 | [AWS RDS 活跃线程持续两分钟大于24](ALR-028_db-rds-active-threads-24-v2.md) | P1 |
| ALR-029 | [AWS RDS 磁盘空间连续3分钟不足10G](ALR-029_db-rds-disk-low-10g.md) | P1 |

---

## 数据库-MongoDB告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-030 | [AWS DocumentDB CPU使用率超过90%](ALR-030_db-mongo-cpu-90.md) | P1 |
| ALR-031 | [AWS DocumentDB CPU使用率超过90% (Voice)](ALR-031_db-mongo-cpu-90-voice.md) | P0 |
| ALR-032 | [DocumentDB 可用内存不足500MB](ALR-032_db-mongo-memory-500m.md) | P1 |

---

## 数据库-OpenSearch告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-033 | [OpenSearch CPU使用率超过90%](ALR-033_db-es-cpu-90.md) | P1 |
| ALR-034 | [OpenSearch CPU使用率超过90% (Voice)](ALR-034_db-es-cpu-90-voice.md) | P0 |
| ALR-035 | [OpenSearch集群状态为RED](ALR-035_db-es-cluster-red.md) | P0 |
| ALR-036 | [OpenSearch集群状态为RED (Voice)](ALR-036_db-es-cluster-red-voice.md) | P0 |
| ALR-037 | [OpenSearch集群状态为YELLOW](ALR-037_db-es-cluster-yellow.md) | P1 |
| ALR-038 | [OpenSearch磁盘空间不足10G](ALR-038_db-es-disk-10g.md) | P1 |
| ALR-039 | [OpenSearch磁盘空间不足10G (Voice)](ALR-039_db-es-disk-10g-voice.md) | P0 |

---

## 数据库-Redis告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-040 | [ElastiCache CPU使用率超过90%](ALR-040_db-redis-cpu-90.md) | P1 |
| ALR-041 | [ElastiCache CPU使用率连续三分钟超过70%](ALR-041_db-redis-cpu-70-3min.md) | P1 |
| ALR-042 | [ElastiCache 内存使用率超过70%](ALR-042_db-redis-memory-70.md) | P1 |
| ALR-043 | [ElastiCache 客户端阻塞](ALR-043_db-redis-client-blocked.md) | P1 |
| ALR-044 | [ElastiCache 延迟超过2ms](ALR-044_db-redis-latency-2ms.md) | P1 |
| ALR-045 | [ElastiCache 复制缓冲区超过32MB](ALR-045_db-redis-buffer-32m.md) | P2 |
| ALR-046 | [ElastiCache 网络流量超过32Mbps](ALR-046_db-redis-traffic-32mbps.md) | P2 |
| ALR-047 | [ElastiCache Key驱逐告警](ALR-047_db-redis-key-eviction.md) | P1 |
| ALR-048 | [ElastiCache 连接数超过30](ALR-048_db-redis-connections-30.md) | P2 |
| ALR-049 | [ElastiCache 数据采集失败](ALR-049_db-redis-collection-failed.md) | P2 |

---

## 数据库-Exporter告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-050 | [数据库Exporter异常](ALR-050_db-exporter-abnormal.md) | P2 |

---

## SMS-UPUSH告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-051 | [SMS通道下发失败次数超过50次](ALR-051_upush-sms-provider-failures-50.md) | P1 |
| ALR-052 | [SMS通道返回失败次数超过200次](ALR-052_upush-sms-return-failures-200.md) | P1 |
| ALR-053 | [营销短信回执率低于60%](ALR-053_upush-marketing-receipt-60.md) | P2 |
| ALR-054 | [营销短信被过滤次数超过100次](ALR-054_upush-marketing-filtered-100.md) | P2 |
| ALR-055 | [行业短信回执率低于70%](ALR-055_upush-industry-receipt-70.md) | P1 |
| ALR-056 | [行业短信被过滤次数超过50次](ALR-056_upush-industry-filtered-50.md) | P2 |
| ALR-057 | [验证码发送量低于30/分钟](ALR-057_upush-verification-volume-30.md) | P1 |
| ALR-058 | [验证码回执率低于70%](ALR-058_upush-verification-receipt-70.md) | P1 |
| ALR-059 | [验证码被过滤次数超过50次](ALR-059_upush-verification-filtered-50.md) | P1 |

---

## APM-iZeus策略告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-060 | [异常数量超过2个 (策略1)](ALR-060_izeus-strategy1-exceptions-2.md) | P1 |
| ALR-061 | [异常数量超过2个 (策略2)](ALR-061_izeus-strategy2-exceptions-2.md) | P1 |
| ALR-062 | [异常数量超过2个 (策略3)](ALR-062_izeus-strategy3-exceptions-2.md) | P1 |
| ALR-063 | [异常数量超过2个 (策略4)](ALR-063_izeus-strategy4-exceptions-2.md) | P1 |
| ALR-064 | [异常数量超过3个 (策略5)](ALR-064_izeus-strategy5-exceptions-3.md) | P1 |
| ALR-065 | [异常数量超过2个 (策略6)](ALR-065_izeus-strategy6-exceptions-2.md) | P1 |
| ALR-066 | [异常数量超过2个 (策略7)](ALR-066_izeus-strategy7-exceptions-2.md) | P1 |
| ALR-067 | [异常数量超过2个 (策略8)](ALR-067_izeus-strategy8-exceptions-2.md) | P1 |
| ALR-068 | [异常数量超过2个 (策略9)](ALR-068_izeus-strategy9-exceptions-2.md) | P1 |
| ALR-069 | [JVM CPU使用率超过20% (策略10)](ALR-069_izeus-strategy10-jvm-cpu-20.md) | P2 |
| ALR-070 | [响应时间超过1500ms (策略10)](ALR-070_izeus-strategy10-response-1500.md) | P1 |
| ALR-071 | [端点错误数超过1 (策略11)](ALR-071_izeus-strategy11-endpoint-1.md) | P1 |
| ALR-072 | [端点错误数超过1 (策略12)](ALR-072_izeus-strategy12-endpoint-1.md) | P1 |
| ALR-073 | [异常数量超过3个 (策略15)](ALR-073_izeus-strategy15-exceptions-3.md) | P1 |
| ALR-074 | [端点错误数超过2 (策略16)](ALR-074_izeus-strategy16-endpoint-2.md) | P1 |
| ALR-075 | [端点错误数超过3 (策略17)](ALR-075_izeus-strategy17-endpoint-3.md) | P1 |

---

## APM-iZeus基础设施告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-076 | [节点CPU使用率超过85%](ALR-076_izeus-node-cpu-85.md) | P1 |
| ALR-077 | [节点磁盘使用率超过85%](ALR-077_izeus-node-disk-85.md) | P1 |
| ALR-078 | [节点内存使用率超过95%](ALR-078_izeus-node-memory-95.md) | P0 |
| ALR-079 | [OAP Full GC次数超过5次](ALR-079_izeus-oap-fgc-5.md) | P1 |
| ALR-080 | [Thanos存储采集为0](ALR-080_izeus-storage-thanos-0.md) | P1 |
| ALR-081 | [VictoriaMetrics存储采集为0](ALR-081_izeus-storage-vm-0.md) | P1 |
| ALR-082 | [Agent到OAP传输为0](ALR-082_izeus-transfer-agent-oap-0.md) | P1 |
| ALR-083 | [OAP到OAP传输为0](ALR-083_izeus-transfer-oap-oap-0.md) | P1 |
| ALR-084 | [Trace Receiver传输为0](ALR-084_izeus-transfer-trace-receiver-0.md) | P1 |

---

## 默认策略告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-085 | [JVM GC告警](ALR-085_default-jvm-gc.md) | P2 |
| ALR-086 | [OkHttp错误数超过50](ALR-086_default-okhttp-50.md) | P2 |
| ALR-087 | [异常数量超过20个](ALR-087_default-exceptions-20.md) | P2 |
| ALR-088 | [异常数量超过5个](ALR-088_default-exceptions-5.md) | P2 |

---

## Pod/容器告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-089 | [CPU使用率超过85% (Fallback)](ALR-089_pod-cpu-fallback-85.md) | P1 |
| ALR-090 | [CPU使用率持续10分钟超过50%](ALR-090_pod-cpu-50-10min.md) | P2 |
| ALR-091 | [CPU使用率持续3分钟超过70%](ALR-091_pod-cpu-70-3min.md) | P1 |
| ALR-092 | [Node心跳丢失](ALR-092_pod-node-heartbeat-lost.md) | P0 |
| ALR-093 | [Pod在2分钟内重启](ALR-093_pod-restart-2min.md) | P1 |
| ALR-094 | [Pod内存OOM](ALR-094_pod-memory-oom.md) | P0 |
| ALR-095 | [Pod线程数超过3600](ALR-095_pod-threads-3600.md) | P1 |
| ALR-096 | [Pod IO写入超过50MB/s](ALR-096_pod-io-write-50mb.md) | P2 |
| ALR-097 | [Pod IO读取超过50MB/s](ALR-097_pod-io-read-50mb.md) | P2 |
| ALR-098 | [Pod入站流量超过30MB/s](ALR-098_pod-network-ingress-30mb.md) | P2 |
| ALR-099 | [Pod出站流量超过30MB/s](ALR-099_pod-network-egress-30mb.md) | P2 |

---

## VM/主机告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-100 | [CPU负载超过1倍核心数](ALR-100_vm-cpu-load-1x.md) | P2 |
| ALR-101 | [CPU平均使用率超过80%](ALR-101_vm-cpu-avg-80.md) | P1 |
| ALR-102 | [CPU IOWait超过80%](ALR-102_vm-cpu-iowait-80.md) | P1 |
| ALR-103 | [CPU Steal超过10%](ALR-103_vm-cpu-steal-10.md) | P2 |
| ALR-104 | [Inode使用率超过95%](ALR-104_vm-inodes-95.md) | P1 |
| ALR-105 | [文件系统只读](ALR-105_vm-filesystem-readonly.md) | P0 |
| ALR-106 | [IO延迟超过90ms](ALR-106_vm-io-latency-90ms.md) | P1 |
| ALR-107 | [IO使用率超过70%](ALR-107_vm-io-usage-70.md) | P2 |
| ALR-108 | [TCP重传次数超过200](ALR-108_vm-tcp-retransmits-200.md) | P2 |
| ALR-109 | [内存使用率持续10分钟超过90%](ALR-109_vm-memory-90-10min.md) | P1 |
| ALR-110 | [心跳丢失超过10分钟](ALR-110_vm-heartbeat-lost-10min.md) | P0 |
| ALR-111 | [磁盘使用率超过90%](ALR-111_vm-disk-90.md) | P1 |
| ALR-112 | [入站网络丢包超过20](ALR-112_vm-network-drop-in-20.md) | P2 |
| ALR-113 | [入站网络错误超过20](ALR-113_vm-network-error-in-20.md) | P2 |
| ALR-114 | [出站网络丢包超过20](ALR-114_vm-network-drop-out-20.md) | P2 |
| ALR-115 | [出站网络错误超过20](ALR-115_vm-network-error-out-20.md) | P2 |
| ALR-116 | [网卡Down](ALR-116_vm-nic-down.md) | P0 |

---

## 业务告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-117 | [取消订单数异常](ALR-117_business-cancelled-orders.md) | P1 |
| ALR-118 | [完成订单数为0](ALR-118_business-complete-orders-0.md) | P0 |
| ALR-119 | [订单支持数为0](ALR-119_business-order-support-0.md) | P0 |
| ALR-120 | [用户注册数为0](ALR-120_business-registrations-0.md) | P0 |
| ALR-121 | [支付金额异常(超过500)](ALR-121_business-payments-500.md) | P1 |

---

## 风控告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-122 | [全局预熔断](ALR-122_risk-global-prebreak.md) | P1 |
| ALR-123 | [全局熔断](ALR-123_risk-global-break.md) | P0 |
| ALR-124 | [场景预熔断](ALR-124_risk-scene-prebreak.md) | P1 |
| ALR-125 | [场景熔断](ALR-125_risk-scene-break.md) | P0 |
| ALR-126 | [订单RPC调用量飙升](ALR-126_risk-order-rpc-spike.md) | P1 |
| ALR-127 | [支付RPC调用量飙升](ALR-127_risk-payment-rpc-spike.md) | P1 |
| ALR-128 | [注册RPC调用量飙升](ALR-128_risk-register-rpc-spike.md) | P1 |
| ALR-129 | [登录RPC调用量飙升](ALR-129_risk-login-rpc-spike.md) | P1 |
| ALR-130 | [短信RPC调用量飙升](ALR-130_risk-sms-rpc-spike.md) | P1 |

---

## 网关告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-131 | [错误率超过15%](ALR-131_gateway-error-rate-15.md) | P1 |

---

## 网络告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-132 | [网络探测失败超过15秒](ALR-132_network-probe-failed-15s.md) | P1 |

---

## Grafana告警

| 告警ID | 告警名称 | 优先级 |
|--------|----------|--------|
| ALR-133 | [慢查询数量飙升](ALR-133_grafana-slow-query-spike.md) | P2 |
| ALR-134 | [慢查询数量严重](ALR-134_grafana-slow-query-critical.md) | P1 |
| ALR-135 | [慢查询数量周报](ALR-135_grafana-slow-query-weekly.md) | P3 |

---

## 统计信息

| 统计项 | 数量 |
|--------|------|
| **总告警数** | 135 |
| **P0告警** | 19 |
| **P1告警** | 79 |
| **P2告警** | 33 |
| **P3告警** | 4 |

---

> **瑞幸咖啡美国运维团队**
