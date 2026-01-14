#!/usr/bin/env python3
"""
Update runbooks with:
1. Remove 责任团队 row from overview table
2. Rename files to use actual alert names
3. Update content based on wiki information
4. Mark frequent alerts
"""

import re
import os
import shutil
from pathlib import Path

# Map current file names to actual alert names
ALERT_NAME_MAP = {
    "ALR-001_[LCP-Prod-P0].md": "ALR-001【LCP-Prod-P0】生产环境紧急告警.md",
    "ALR-002_[LCP-Prod-P1].md": "ALR-002【LCP-Prod-P1】生产环境高优先级告警.md",
    "ALR-003_[LCP-Prod-P2].md": "ALR-003【LCP-Prod-P2】生产环境中优先级告警.md",
    "ALR-004_[LCP-Prod-P3].md": "ALR-004【LCP-Prod-P3】生产环境低优先级告警.md",
    "ALR-005_datalink-golden-flow-delay-day.md": "ALR-005【Datalink】黄金流程任务延迟告警（白天）.md",
    "ALR-006_datalink-golden-flow-exception-day.md": "ALR-006【Datalink】黄金流程任务异常告警（白天）.md",
    "ALR-007_datalink-offline-core-delay-day.md": "ALR-007【Datalink】离线核心任务延迟告警（白天）.md",
    "ALR-008_datalink-offline-core-exception-day.md": "ALR-008【Datalink】离线核心任务异常告警（白天）.md",
    "ALR-009_datalink-important-delay-day.md": "ALR-009【Datalink】重要任务延迟告警（白天）.md",
    "ALR-010_datalink-important-exception-day.md": "ALR-010【Datalink】重要任务异常告警（白天）.md",
    "ALR-011_datalink-offline-important-delay-day.md": "ALR-011【Datalink】离线重要任务延迟告警（白天）.md",
    "ALR-012_datalink-offline-important-exception-day.md": "ALR-012【Datalink】离线重要任务异常告警（白天）.md",
    "ALR-013_datalink-task-delay-night.md": "ALR-013【Datalink】任务延迟告警（夜晚）.md",
    "ALR-014_datalink-task-exception-night.md": "ALR-014【Datalink】任务异常告警（夜晚）.md",
    "ALR-015_datalink-regular-delay-day.md": "ALR-015【Datalink】普通任务延迟告警（白天）.md",
    "ALR-016_datalink-regular-exception-day.md": "ALR-016【Datalink】普通任务异常告警（白天）.md",
    "ALR-017_datalink-offline-regular-delay-day.md": "ALR-017【Datalink】离线普通任务延迟告警（白天）.md",
    "ALR-018_datalink-offline-regular-exception-day.md": "ALR-018【Datalink】离线普通任务异常告警（白天）.md",
    "ALR-019_db-rds-cpu-90-3min-v1.md": "ALR-019【DB告警】AWS-RDS CPU使用率连续三分钟大于90%.md",
    "ALR-020_db-rds-cpu-90-3min-v2.md": "ALR-020【DB告警】AWS RDS CPU使用率连续三分钟大于90%.md",
    "ALR-021_db-rds-vip-unreachable.md": "ALR-021【DB告警】AWS RDS Vip 持续一分钟不通.md",
    "ALR-022_db-rds-vip-unreachable-voice.md": "ALR-022【DB告警】AWS RDS Vip 持续一分钟不通_语音.md",
    "ALR-023_db-rds-failover-restart.md": "ALR-023【DB告警】AWS RDS 发生重启或者主从切换.md",
    "ALR-024_db-rds-failover-restart-voice.md": "ALR-024【DB告警】AWS RDS 发生重启或者主从切换_语音.md",
    "ALR-025_db-rds-slow-queries-300-v1.md": "ALR-025【DB告警】AWS RDS 慢查询数量持续三分钟大于300个.md",
    "ALR-026_db-rds-slow-queries-300-v2.md": "ALR-026【DB告警】AWS-RDS 慢查询数量持续三分钟大于300个.md",
    "ALR-027_db-rds-active-threads-24-v1.md": "ALR-027【DB告警】AWS RDS 活跃线程持续两分钟大于24.md",
    "ALR-028_db-rds-active-threads-24-v2.md": "ALR-028【DB告警】AWS-RDS 活跃线程持续两分钟大于24.md",
    "ALR-029_db-rds-disk-low-10g.md": "ALR-029【DB告警】AWS RDS 磁盘空间连续3分钟不足10G.md",
    "ALR-030_db-mongo-cpu-90.md": "ALR-030【DB告警】AWS Mongo CPU使用率连续三分钟大于90%.md",
    "ALR-031_db-mongo-cpu-90-voice.md": "ALR-031【DB告警】AWS Mongo CPU使用率连续三分钟大于90%_语音.md",
    "ALR-032_db-mongo-memory-500m.md": "ALR-032【DB告警】AWS Mongo 可用内存连续三分钟不足500M.md",
    "ALR-033_db-es-cpu-90.md": "ALR-033【DB告警】AWS-ES CPU 使用率大于90%.md",
    "ALR-034_db-es-cpu-90-voice.md": "ALR-034【DB告警】AWS-ES CPU 使用率大于90%_语音.md",
    "ALR-035_db-es-cluster-red.md": "ALR-035【DB告警】AWS-ES 集群状态Red.md",
    "ALR-036_db-es-cluster-red-voice.md": "ALR-036【DB告警】AWS-ES 集群状态Red_语音.md",
    "ALR-037_db-es-cluster-yellow.md": "ALR-037【DB告警】AWS-ES 集群状态Yellow.md",
    "ALR-038_db-es-disk-10g.md": "ALR-038【DB告警】AWS-ES磁盘空间不足10G.md",
    "ALR-039_db-es-disk-10g-voice.md": "ALR-039【DB告警】AWS-ES磁盘空间不足10G_语音.md",
    "ALR-040_db-redis-cpu-90.md": "ALR-040【DB告警】AWS Redis CPU使用率大于90%.md",
    "ALR-041_db-redis-cpu-70-3min.md": "ALR-041【DB告警】Redis CPU使用率持续3分钟超过70%.md",
    "ALR-042_db-redis-memory-70.md": "ALR-042【DB告警】Redis 内存使用率持续3分钟超过70%.md",
    "ALR-043_db-redis-client-blocked.md": "ALR-043【DB告警】Redis 发生客户端堵塞.md",
    "ALR-044_db-redis-latency-2ms.md": "ALR-044【DB告警】Redis 实例命令平均时延大于2ms.md",
    "ALR-045_db-redis-buffer-32m.md": "ALR-045【DB告警】Redis 实例客户端nomal缓冲超过32m.md",
    "ALR-046_db-redis-traffic-32mbps.md": "ALR-046【DB告警】Redis 实例流量大于32Mbps.md",
    "ALR-047_db-redis-key-eviction.md": "ALR-047【DB告警】Redis 实例触发key淘汰.md",
    "ALR-048_db-redis-connections-30.md": "ALR-048【DB告警】Redis 实例连接数使用率大于30%.md",
    "ALR-049_db-redis-collection-failed.md": "ALR-049【DB告警】Redis 实例采集失败请检查是否存活.md",
    "ALR-050_db-exporter-abnormal.md": "ALR-050【DB告警】exporter 进程异常.md",
    "ALR-051_upush-sms-provider-failures-50.md": "ALR-051【UPUSH】五分钟短信供应商调用失败超过阈值50.md",
    "ALR-052_upush-sms-return-failures-200.md": "ALR-052【UPUSH】五分钟短信供应商返回值失败超过阈值200.md",
    "ALR-053_upush-marketing-receipt-60.md": "ALR-053【UPUSH】营销短信回执成功率低于60%.md",
    "ALR-054_upush-marketing-filtered-100.md": "ALR-054【UPUSH】营销短信过滤数超过100.md",
    "ALR-055_upush-industry-receipt-70.md": "ALR-055【UPUSH】行业短信回执成功率低于70%.md",
    "ALR-056_upush-industry-filtered-50.md": "ALR-056【UPUSH】行业短信过滤数超过50.md",
    "ALR-057_upush-verification-volume-30.md": "ALR-057【UPUSH】验证码发送量同比增加30%.md",
    "ALR-058_upush-verification-receipt-70.md": "ALR-058【UPUSH】验证码回执成功率低于70%.md",
    "ALR-059_upush-verification-filtered-50.md": "ALR-059【UPUSH】验证码过滤数超过50.md",
    "ALR-060_izeus-strategy1-exceptions-2.md": "ALR-060【iZeus-策略1】服务每分钟异常数大于2.md",
    "ALR-061_izeus-strategy2-exceptions-2.md": "ALR-061【iZeus-策略2】服务每分钟异常数大于2.md",
    "ALR-062_izeus-strategy3-exceptions-2.md": "ALR-062【iZeus-策略3】服务每分钟异常数大于2.md",
    "ALR-063_izeus-strategy4-exceptions-2.md": "ALR-063【iZeus-策略4】服务每分钟异常数大于2.md",
    "ALR-064_izeus-strategy5-exceptions-3.md": "ALR-064【iZeus-策略5】服务每分钟异常数大于3.md",
    "ALR-065_izeus-strategy6-exceptions-2.md": "ALR-065【iZeus-策略6】服务每分钟异常数大于2.md",
    "ALR-066_izeus-strategy7-exceptions-2.md": "ALR-066【iZeus-策略7】服务每分钟异常数大于2.md",
    "ALR-067_izeus-strategy8-exceptions-2.md": "ALR-067【iZeus-策略8】服务每分钟异常数大于2.md",
    "ALR-068_izeus-strategy9-exceptions-2.md": "ALR-068【iZeus-策略9】服务每分钟异常数大于2.md",
    "ALR-069_izeus-strategy10-jvm-cpu-20.md": "ALR-069【iZeus-策略10】JVM CPU使用率大于20.md",
    "ALR-070_izeus-strategy10-response-1500.md": "ALR-070【iZeus-策略10】服务响应时间大于1500ms.md",
    "ALR-071_izeus-strategy11-endpoint-1.md": "ALR-071【iZeus-策略11】端点每分钟失败数大于等于1.md",
    "ALR-072_izeus-strategy12-endpoint-1.md": "ALR-072【iZeus-策略12】端点每分钟失败数大于等于1.md",
    "ALR-073_izeus-strategy15-exceptions-3.md": "ALR-073【iZeus-策略15】服务每分钟异常数大于3.md",
    "ALR-074_izeus-strategy16-endpoint-2.md": "ALR-074【iZeus-策略16】端点每分钟失败数大于2.md",
    "ALR-075_izeus-strategy17-endpoint-3.md": "ALR-075【iZeus-策略17】端点每分钟失败数大于3.md",
    "ALR-076_izeus-node-cpu-85.md": "ALR-076【iZeus】Node-CPU-85 节点CPU使用率大于85%.md",
    "ALR-077_izeus-node-disk-85.md": "ALR-077【iZeus】Node-Disk-85 节点磁盘使用率大于85%.md",
    "ALR-078_izeus-node-memory-95.md": "ALR-078【iZeus】Node-Memory-95 节点内存使用率大于95%.md",
    "ALR-079_izeus-oap-fgc-5.md": "ALR-079【iZeus】OAP-FGC-5 Full GC次数大于5.md",
    "ALR-080_izeus-storage-thanos-0.md": "ALR-080【iZeus】Storage-Receiver2Thanos-Receiver-0.md",
    "ALR-081_izeus-storage-vm-0.md": "ALR-081【iZeus】Storage-Receiver2VM-0.md",
    "ALR-082_izeus-transfer-agent-oap-0.md": "ALR-082【iZeus】Transfer-Agent2OAP-0.md",
    "ALR-083_izeus-transfer-oap-oap-0.md": "ALR-083【iZeus】Transfer-OAP2OAP-0.md",
    "ALR-084_izeus-transfer-trace-receiver-0.md": "ALR-084【iZeus】Transfer-OAPTrace2Receiver-0.md",
    "ALR-085_default-jvm-gc.md": "ALR-085【默认策略】FGC次数大于0或YGC耗时大于500毫秒.md",
    "ALR-086_default-okhttp-50.md": "ALR-086【默认策略】异常okhttp总数大于等于50.md",
    "ALR-087_default-exceptions-20.md": "ALR-087【默认策略】服务器每分钟异常数大于20.md",
    "ALR-088_default-exceptions-5.md": "ALR-088【默认策略】服务器每分钟异常数大于5.md",
    "ALR-089_pod-cpu-fallback-85.md": "ALR-089【pod-cpu-兜底】P0 CPU使用率连续3分钟大于85%.md",
    "ALR-090_pod-cpu-50-10min.md": "ALR-090【pod-cpu】P0 CPU使用率连续10分钟大于50%.md",
    "ALR-091_pod-cpu-70-3min.md": "ALR-091【pod-cpu】P0 CPU使用率连续3分钟大于70%.md",
    "ALR-092_pod-node-heartbeat-lost.md": "ALR-092【pod-全局】P0 node节点up心跳丢失需检查节点是否宕机.md",
    "ALR-093_pod-restart-2min.md": "ALR-093【pod-全局】P0 Pod 2m内发生重启请关注.md",
    "ALR-094_pod-memory-oom.md": "ALR-094【pod-宕机】P1 WSS内存使用率连续3分钟等于100%(OOM参考).md",
    "ALR-095_pod-threads-3600.md": "ALR-095【pod-线程】P0 容器线程数连续3分钟超过3600.md",
    "ALR-096_pod-io-write-50mb.md": "ALR-096【pod-网卡】P0 分区写入速率连续3分钟大于50MBs.md",
    "ALR-097_pod-io-read-50mb.md": "ALR-097【pod-网卡】P0 分区读取速率连续3分钟大于50MBs.md",
    "ALR-098_pod-network-ingress-30mb.md": "ALR-098【pod-网卡】P0 网卡流入速率连续3分钟大于30MBs.md",
    "ALR-099_pod-network-egress-30mb.md": "ALR-099【pod-网卡】P0 网卡流出速率连续3分钟大于30MBs.md",
    "ALR-100_vm-cpu-load-1x.md": "ALR-100【vm-CPU】P1 CPU平均负载大于CPU核心数量的1倍已持续5分钟.md",
    "ALR-101_vm-cpu-avg-80.md": "ALR-101【vm-CPU】P1 服务整体CPU平均使用率超过80%.md",
    "ALR-102_vm-cpu-iowait-80.md": "ALR-102【vm-cpu】P0 5分钟内服务CPU_iowait每秒的使用率大于80%.md",
    "ALR-103_vm-cpu-steal-10.md": "ALR-103【vm-cpu】P0 服务CPU使用率窃取大于10%.md",
    "ALR-104_vm-inodes-95.md": "ALR-104【vm-fileSystem】P0 分区inodes使用率大于95%请立即处理.md",
    "ALR-105_vm-filesystem-readonly.md": "ALR-105【vm-fileSystem】P0 分区发送只读事件请检查分区读写情况.md",
    "ALR-106_vm-io-latency-90ms.md": "ALR-106【vm-io】P0 服务io耗时大于90ms且同比超过20ms.md",
    "ALR-107_vm-io-usage-70.md": "ALR-107【vm-io】P1 磁盘IO使用率大于70%且同比超过20.md",
    "ALR-108_vm-tcp-retransmits-200.md": "ALR-108【vm-tcp】P0 TCP每秒重传报文数超过200.md",
    "ALR-109_vm-memory-90-10min.md": "ALR-109【vm-内存】P1 内存使用率大于90% 持续10分钟.md",
    "ALR-110_vm-heartbeat-lost-10min.md": "ALR-110【vm-宕机】P0 up监控指标心跳丢失10分钟需检查设备是否宕机.md",
    "ALR-111_vm-disk-90.md": "ALR-111【vm-磁盘】P1 分区使用率大于90%请手动处理.md",
    "ALR-112_vm-network-drop-in-20.md": "ALR-112【vm-网卡】P0 入方向在5分钟内每秒丢弃的数据包大于20个.md",
    "ALR-113_vm-network-error-in-20.md": "ALR-113【vm-网卡】P0 入方向在5分钟内每秒错误的数据包大于20个.md",
    "ALR-114_vm-network-drop-out-20.md": "ALR-114【vm-网卡】P0 出方向在5分钟内每秒丢弃的数据包大于20个.md",
    "ALR-115_vm-network-error-out-20.md": "ALR-115【vm-网卡】P0 出方向在5分钟内每秒错误的数据包大于20个.md",
    "ALR-116_vm-nic-down.md": "ALR-116【vm-网卡】P0 网卡状态为down.md",
    "ALR-117_business-cancelled-orders.md": "ALR-117【北美-业务告警】取消订单持续5分钟大于1单.md",
    "ALR-118_business-complete-orders-0.md": "ALR-118【北美-业务告警】新建-付款-完成订单持续10分钟少于1单.md",
    "ALR-119_business-order-support-0.md": "ALR-119【北美-业务告警】订单支持持续10分钟小于1.md",
    "ALR-120_business-registrations-0.md": "ALR-120【北美-业务告警】过去10分钟注册数为0.md",
    "ALR-121_business-payments-500.md": "ALR-121【北美-业务告警】过去5分钟支付金额小于500分.md",
    "ALR-122_risk-global-prebreak.md": "ALR-122【北美亚风控】全局策略熔断前预告警.md",
    "ALR-123_risk-global-break.md": "ALR-123【北美亚风控】全局策略熔断告警.md",
    "ALR-124_risk-scene-prebreak.md": "ALR-124【北美亚风控】场景熔断前预告警.md",
    "ALR-125_risk-scene-break.md": "ALR-125【北美风控】场景熔断告警.md",
    "ALR-126_risk-order-rpc-spike.md": "ALR-126【国际化北美风控】下单rpc接口调用量超过200次且比上周多60%.md",
    "ALR-127_risk-payment-rpc-spike.md": "ALR-127【国际化北美风控】支付rpc接口调用量超过200次且比上周多60%.md",
    "ALR-128_risk-register-rpc-spike.md": "ALR-128【国际化北美风控】注册rpc接口调用量超过100次且比上周多60%.md",
    "ALR-129_risk-login-rpc-spike.md": "ALR-129【国际化北美风控】登录rpc接口调用量超过100次且比上周多60%.md",
    "ALR-130_risk-sms-rpc-spike.md": "ALR-130【国际化北美风控】短信rpc接口调用量超过100次且比上周多60%.md",
    "ALR-131_gateway-error-rate-15.md": "ALR-131【网关告警】错误率大于15%.md",
    "ALR-132_network-probe-failed-15s.md": "ALR-132【网络质量US-机房互拨】探测目标连续15s失败.md",
    "ALR-133_grafana-slow-query-spike.md": "ALR-133【Grafana】Slow Query Spike - High Rate Alert.md",
    "ALR-134_grafana-slow-query-critical.md": "ALR-134【Grafana】Slow Query Critical - Very High Rate Alert.md",
    "ALR-135_grafana-slow-query-weekly.md": "ALR-135【Grafana】Slow Query Weekly Increase - WoW Spike Alert.md",
}

# Alerts that are frequently occurring (based on wiki documentation)
FREQUENT_ALERTS = {
    "ALR-023": True,  # AWS RDS 发生重启或者主从切换
    "ALR-024": True,  # AWS RDS 发生重启或者主从切换_语音
    "ALR-027": True,  # AWS RDS 活跃线程持续两分钟大于24
    "ALR-028": True,  # AWS-RDS 活跃线程持续两分钟大于24
    "ALR-038": True,  # AWS-ES磁盘空间不足10G
    "ALR-039": True,  # AWS-ES磁盘空间不足10G_语音
    "ALR-042": True,  # Redis 内存使用率持续3分钟超过70%
    "ALR-093": True,  # Pod 2m内发生重启
    "ALR-094": True,  # WSS内存使用率连续3分钟等于100%(OOM)
    "ALR-131": True,  # 网关告警 错误率大于15%
}

# Wiki-based enhanced content for specific alerts
WIKI_ENHANCEMENTS = {
    "ALR-023": {
        "root_cause_detail": """
**根据实际案例分析（2025-10-24 aws-luckyus-opshop-rw案例）：**

本次重启与主从切换由**底层宿主机故障引发**，体现为"主机因网络连通性丢失不可达"，RDS 自动执行**主机替换 + 实例重启 + Multi-AZ Failover**。

**AWS 官方知识库说明：**
- 当primary host 不可达（网络连通性丢失）时会触发Multi-AZ failover 和实例重启，属于底层网络/基础设施瞬时异常场景
- 硬件问题会在 Multi-AZ 中触发failover，同时 RDS 可能进行底层宿主机替换；这是 RDS 的自动自愈行为
- Multi-AZ 的 failover 由 RDS 自动处理，常见时长**60-120秒**（受事务恢复、负载影响）
- Failover 发生时，RDS 会更新实例的 DNS 指向到新的主库，应用**必须重新建立连接**（特别注意 JVM 的 DNS 缓存 TTL）
""",
        "steps_detail": """
### 步骤1：确认告警信息

检查AWS RDS控制台 Event Log，关注以下事件：
- `Multi-AZ instance failover started`（开始主从切换）
- `DB instance restarted`（实例重启）
- `The primary host … is unreachable due to loss of network connectivity`（主库主机因网络连通性丢失不可达）
- `Multi-AZ instance failover completed`（主从切换完成）

### 步骤2：检查 Grafana / CloudWatch 监控面板

**数据库基础态势（Grafana/Performance Insights）：**
- CPU、内存、连接数（DatabaseConnections）、TPS/QPS、线程运行数
- 慢查询趋势（Slow query）

**CloudWatch 关键指标：**
- `CPUUtilization`、`DatabaseConnections`
- `FreeableMemory`（观察是否持续逼近极值）
- `DiskQueueDepth`（I/O 等待）

**指标时间范围聚焦：** 告警发生时间前后10分钟

**应用侧观测：**
- APM/网关错误峰值（`OperationalError`、`Connection reset by peer`、`too many connections`等）
- 连接重试/超时日志（是否按策略快速恢复）

### 步骤3：检查 LDAS（数据库审计/监控系统）

- 观察告警窗口内是否存在**长事务/锁等待**（用于排除负载诱因）
- 若发现异常语句，留存 SQL 与执行计划

### 步骤4：沟通确认

在服务树找到负责人并在告警群同步：
- 当时是否有**手工重启/维护操作**
- 当时是否有**批作业/峰值流量**
- 如未来**重复发生**，建议开AWS Support Case让官方排查AZ/宿主集群稳定性

### 步骤5：处理措施

**短期：**
- 观察应用恢复：确认所有连接池已恢复、业务无持续错误
- 开启/核对RDS 事件通知（SNS），确保此类 failover 能第一时间推送到告警系统
- 验证客户端**自动重连与指数退避**是否生效；JVM 场景下检查`networkaddress.cache.ttl`以降低 DNS 缓存带来的恢复延迟

**中长期：**
- **RDS Proxy**：在 MySQL/PostgreSQL 等引擎前加入 RDS Proxy，利用连接池与更平滑的故障切换降低应用可见中断
- **演练与指标**：定期在低峰期做手工 Failover 演练，记录实际 RTO（期望 60-120s 内）
- **事件覆盖**：在告警体系中补充 "RDS Event: failover started/completed、host replacement"等关键事件
""",
    },
    "ALR-027": {
        "root_cause_detail": """
**根据实际案例分析（2025-09-29 aws-luckyus-iluckyhealth-rw案例）：**

**重要提示：**
- **Luckyhealth数据库**是专门为Grafana做的监控数据库
- **Test数据库**上的操作相对安全
- **生产数据库**操作需要格外小心

**数据同步延迟说明：** Datalink等其他地方的数据都有同步延迟，爬取的数据会慢一点，Luckyhealth相对是快一些的。
""",
        "steps_detail": """
### 步骤1：确认告警信息

检查告警详情，确认：
- **告警等级**：P1
- **集群信息**：如 aws-luckyus-iluckyhealth-rw
- **当前值**：如 177（活跃线程数）
- **故障持续时间**

### 步骤2：检查Grafana监控面板

**Grafana关键指标检查：**

| 指标 | 正常范围 | 说明 |
|------|---------|------|
| CPU使用率 | <80% | 4.99%为正常 |
| 磁盘剩余空间 | >10GiB | 25.7 GiB为健康 |
| Current Thread Running | <24 | 监控当前运行线程 |
| Current QPS | 波动正常 | 2.67为低负载 |
| Thread Connected | 7-13范围 | 连接数正常范围 |

**性能指标分析：**
- **TPS/QPS**：正常波动范围
- **Slow Query（慢查询）**：检查是否有慢查询实例数增加
- **MySQL DML commands**：insert操作频率正常
- **DB Threads**：Thread Connected数量正常

### 步骤3：检查AWS CloudWatch监控

**关键指标检查：**
- `CPUUtilization`：检查是否有突增
- `DatabaseConnections`：查看连接数波动情况
- `FreeableMemory`：⚠️ **重点关注此参数**，观察内存使用趋势
- `CPUCreditBalance/CPUCreditUsage`：如果是突发型实例，检查CPU积分
- `DiskQueueDepth`：检查IO是否存在瓶颈

### 步骤4：检查LDAS数据库进程

**查看活跃进程：**
- 检查当前正在执行的SQL语句
- 查看进程运行时长
- 确认是否有长时间运行的事务

**慢查询分析：**
- 检查是否存在慢查询
- 分析慢查询的SQL语句
- 查看慢查询的执行计划

**锁等待检查：**
- 查看是否存在锁等待情况
- 确认是否有死锁或长时间持有锁的情况

### 步骤5：处理措施

**如果是慢查询导致：**
- **短期**：评估是否可以安全kill掉慢查询进程、联系业务方优化SQL语句
- **长期**：优化慢查询SQL、添加合适的索引、考虑数据归档方案

**如果是连接数过多：**
- 检查连接池配置是否合理
- 检查是否存在连接泄漏
- 考虑增加RDS实例规格或增加读副本分担读压力

**如果是内存不足：**
- **短期**：重启数据库释放缓存（需评估业务影响）
- **长期**：升级RDS实例规格、优化内存使用配置、数据归档或分库分表
""",
    },
    "ALR-042": {
        "root_cause_detail": """
**根据实际案例分析（2025-09-17 luckyus-web集群案例）：**

**触发规则（内存）：**
- FreeableMemory 持续 < 1 GiB（约等价使用率 > 70%），且一周趋势无回升 → **扩容**
- 若仅短时波动（Spike），且随即回升，可继续观察
- 如出现 **Evictions/SWAP**，优先扩容

**扩容方式（默认）：**
1. **纵向扩容（优先）**：节点规格上升一个档位，例如：`cache.t4g.medium` → `cache.t4g.large`
2. **读多写少**：可增加 Read Replica 分担读
3. **写入压力/键空间过大**：评估开启集群分片做水平扩展
""",
        "steps_detail": """
### 步骤1：确认内存与CPU状态

**登录AWS控制台：** Amazon ElastiCache → 选择 Redis 集群（如 luckyus-web）

**检查内存相关指标（CloudWatch → Metrics → ElastiCache）：**
- `FreeableMemory`（空闲可释放内存）一周趋势
- **判定标准**：若持续 < 1 GiB 且无回升趋势，判定为内存压力，需要扩容
- 同步查看 `Evictions`（是否发生驱逐）、`SwapUsage`（是否出现交换）
- `BytesUsedForCache / EngineUsedMemory`：确认已用内存接近总内存上限
- **截图**：保存一周趋势图（用于变更确认与复盘）

**检查 CPU 指标（建议）：**
- `CPUUtilization`：如持续高于 80%（或 2 核实例总CPU > ~45%），需一并评估

### 步骤2：访问集群与参数信息

**通过AWS控制台：** ElastiCache → Redis → Clusters → 点击集群名称

**查看 Nodes / Metrics / Parameter groups：**
- **参数组**：如 luckyus-ha-6（使用 LRU 驱逐策略 volatile-lru）
- **Multi-AZ 与副本**：Enabled（可降低扩容/故障切换影响）

### 步骤3：确定扩容策略

| 情况 | 处理方式 |
|------|---------|
| FreeableMemory 持续 < 1 GiB | 扩容（纵向） |
| 读多写少场景 | 增加 Read Replica |
| 写入压力/键空间过大 | 开启集群分片（水平扩展） |

### 步骤4：执行扩容操作

**截图记录（重要）：**
- 扩容前：FreeableMemory 一周趋势、Evictions/SwapUsage/CPU 指标截图
- 集群详情页（Engine、Multi-AZ、节点类型、参数组）截图

**通知方式：企业微信告警群/DBA值班**
- 说明：问题现象、阈值命中、建议动作（上调一档）、预计影响（短暂 failover/连接重试）

**控制台扩容：**
1. ElastiCache → Redis → Clusters → 选择集群 → Modify
2. Node type：从 cache.t4g.medium 调整为上一档
3. 其他项保持不变，提交变更
4. 关注状态：modifying → available

**监控恢复情况：**
- 等待 ~20 分钟（视数据量而定）
- 重新查看 FreeableMemory 是否显著回升（> 1 GiB）
- 确认告警解除、应用无持续报错

### 注意事项

⚠️ **关键提醒：**
- 扩容会触发**主从切换**，存在**短暂连接中断**；务必确认客户端具备**重连/重试**
- 若使用 **T 系列（t4g）**，避免长期高负载耗尽 CPU Credit；持续高负载建议改用 M/R 系列
- 仅当**持续性**内存紧张时扩容；瞬时峰值应结合 Evictions/Swap 判断
- 在业务低峰进行计划性扩容，降低影响面
- 变更前后务必**留痕**（截图/记录）
""",
    },
    "ALR-038": {
        "root_cause_detail": """
**根据实际案例分析（2025-09-13案例）：**

**日志保留规则（重要）：**

| 日志类型 | 保留策略 | 索引命名示例 |
|---------|---------|------------|
| 按月生成日志 | 保留 3-6 个月 | logs-2024.09 |
| 按日生成日志 | 保留 7 天 | logs-2024.09.13 |
| LFE集群 (luckylfe-log) | 保留 30 天 | - |
| urlog集群 (luckyur-log) | 保留 15 天 | - |
| dify集群 | 暂不处理 | - |

**清理优先级（默认）：**
1. **优先删除**：按日生成的过期日志（超过保留期限）
2. **次要删除**：大容量索引（> 1GB）中的过期数据
3. **谨慎删除**：按月生成的日志（除非确实超过 3-6 个月）
4. **不删除**：当前活跃索引、系统索引（.开头）、dify集群数据
""",
        "steps_detail": """
### 步骤1：确认磁盘空间与集群状态

**登录AWS控制台：** Amazon OpenSearch Service → 选择告警集群

**检查磁盘空间相关指标（CloudWatch → Metrics → OpenSearch）：**
- `FreeStorageSpace`（剩余可用空间）一周趋势
- **判定标准**：若持续 < 10 GiB 且呈下降趋势，判定为磁盘压力，需要立即清理
- 同步查看 `ClusterIndexWritesBlocked`（是否发生写入阻塞）、`JVMMemoryPressure`（内存压力）

**ClusterHealthStatus 确认：**
- **Red**：立即处理，可能已影响服务
- **Yellow**：需要关注，副本可能受影响
- **Green**：正常状态

### 步骤2：访问索引管理

**通过KBX（https://ikbx.luckincoffee.us/）或AWS Kibana：**
1. 左侧菜单选择 "Index Management" > "Indices"
2. 按 **Size** 降序排序，快速定位占用空间大的索引
3. 查看索引命名规则，区分按日/按月生成的索引

### 步骤3：确定清理策略

**触发规则（磁盘空间）：**
- FreeStorageSpace 持续 < 10 GiB（约等价使用率 > 85%），且一周趋势持续下降 → **立即清理**
- 若仅短时波动，可继续观察
- 如出现 `ClusterIndexWritesBlocked`，优先清理

### 步骤4：执行清理操作

**截图记录（重要）：**
- 清理前：FreeStorageSpace 一周趋势、ClusterHealthStatus 截图
- 索引列表截图（包含名称、大小、文档数）
- 记录要删除的具体索引名称列表

**通知方式：企业微信告警群/DBA值班**

**KBX清理操作：**
1. Stack Management → Index Management → Indices
2. 按 Size 排序，识别大容量索引
3. 核对索引日期，确认符合删除条件
4. 选中待删除索引，点击 Manage indices → Delete indices
5. **二次确认**：输入索引名称确认删除
6. **批量操作建议**：每次删除 5-10 个索引，观察集群响应

**监控恢复情况：**
- 等待 ~5-10 分钟
- 重新查看 FreeStorageSpace 是否显著回升（> 10 GiB）
- 确认 ClusterHealthStatus 保持 Green/Yellow
- 验证 ClusterIndexWritesBlocked 解除

### 注意事项

⚠️ **关键提醒：**
- 删除操作**不可恢复**，务必：二次确认索引名称和日期、确保符合保留策略、保存删除前截图
- **按月生成**的日志谨慎删除（通常是重要汇总数据）
- 优先在**业务低峰期（美国时间晚上）**执行
- 保持与团队沟通，避免重复操作
""",
    },
    "ALR-131": {
        "root_cause_detail": """
**根据实际案例分析（2025-10-03 luckycapiproxy案例）：**

本次告警为**偶发性网关错误率告警**，影响范围无实际业务影响，根本原因疑似网络抖动或短暂超时，3分钟内自动恢复。

**关键经验：**
- 历史告警记录是重要参考
- 必须验证业务实际影响
- 多维度交叉验证（Grafana + iZeus + 实际测试）
- 3-5分钟观察期是合理的处理窗口
- 自动恢复的短暂告警可以不升级
""",
        "steps_detail": """
### 步骤1：检查历史告警记录

**登录iZeus可观测平台：**
1. 进入 告警配置 → 基础告警 → 告警策略
2. 搜索：【网关告警】错误率大于15%
3. 查看历史告警记录
4. 同时检查企业微信历史记录

**判断依据：**
- 如果历史上有相同告警且已解决，可能是偶发性问题
- 查询LSOP中的服务树查询更多这个服务的细节

### 步骤2：验证业务影响 - Grafana订单监控

**打开Grafana监控面板：**
- 导航至：活动保障大盘 / 北美-运维决策报表
- 查看**所有订单_状态**图表

**重点关注：**
- 新建量（绿线）
- 已付款（黄线）
- 已完成（蓝线）
- 已取消（橙线）

**注意：** 监控数据存在一定延迟，属于正常现象

### 步骤3：查看整体告警态势 - iZeus报错大盘

**在iZeus平台操作：**
1. 进入 监控大盘 → 报错大盘（分钟级视图）
2. 选择告警发生时间段
3. 查看各服务报错分布情况

**关注重点：**
- 是否有多个服务同时报错
- luckycapiproxy的报错数量和频率
- 是否存在级联故障

### 步骤4：实际业务验证 - 下单测试

**打开瑞幸咖啡APP：**
1. 选择商品
2. 尝试下单
3. 完成支付流程
4. 观察是否流畅

**测试重点：**
- 加载速度
- 支付成功率
- 是否有报错提示

### 步骤5：图表分析 - Thanos

**在告警配置页面：**
1. 点击**数据查询**按钮
2. 自动跳转到Thanos界面
3. 切换到 **Graph** 标签页
4. 调整时间范围为1小时
5. 点击 Execute 执行

**分析要点：**
- 是否有规律性波动
- 确认是否为重复性问题
- 识别异常峰值的持续时间

### 步骤6：持续观察与决策

| 情况 | 处理方式 |
|------|---------|
| 3分钟内恢复正常 | 继续观察，记录事件 |
| 持续3-5分钟且有业务影响 | 准备通知中国团队 |
| 持续超过5分钟 | 立即升级至中国技术团队 |
| 影响用户下单 | 立即升级 |

### 升级标准

**需要升级中国团队的情况：**
- 告警持续超过5分钟
- Grafana订单数据明显下降
- 实际下单测试失败
- 多个服务同时告警
- 错误率持续上升
""",
    },
    "ALR-093": {
        "root_cause_detail": """
**根据实际案例分析（2025-09-16 iluckysentrybot-pd案例）：**

Pod重启可能由多种原因引起：
- 内存溢出（OOM）
- 健康检查失败
- 应用崩溃
- 资源限制触发
- Kubernetes调度变更

**服务等级说明：**
- L2（普通业务服务）：可按正常流程处理
- L0/L1（核心服务）：需要立即响应
""",
        "steps_detail": """
### 步骤1：确认告警信息

检查告警详情，确认：
- **告警等级**：P0/P1/P2
- **服务等级**：L0/L1/L2
- **Pod名称**
- **所属服务**

**打开Grafana链接查看告警详情**

### 步骤2：检查服务状态

**容器云平台检查：**
1. 登录容器云管理平台
2. 找到对应服务
3. 检查Pod状态：
   - Pod名称
   - 运行状态
   - 重启次数
   - CPU/内存使用率

### 步骤3：联系负责人

**通过服务树找到负责人信息：**
- 在LSOP → 服务树 → 基础信息中查找
- 在告警群组中询问是否知晓问题

### 步骤4：处理措施

**重启服务（如需要）：**

**方式一：持续交付平台操作：**
- 路径：PROD > LUCKY > WEB > [服务名]
- 选择受影响的Pod
- 执行滚动重启

**方式二：容器云平台操作：**
- 在Pod列表中选择对应实例
- 点击"重启"按钮
- 监控重启进度

**重启后验证：**
- 确认所有Pod恢复Running状态
- 检查健康检查endpoint响应正常
- 验证Grafana指标恢复正常

### 步骤5：问题解决确认

- [ ] 错误率恢复正常
- [ ] 响应时间符合预期
- [ ] 所有Pod运行正常
- [ ] 健康检查通过
""",
    },
    "ALR-094": {
        "root_cause_detail": """
**根据实际案例分析（2025-09-23 hello-world案例）：**

**注意：** 容器名字叫hello-world时，很可能是测试服务。在处理此类告警时应优先确认服务性质和业务影响范围。

**OOM（内存溢出）常见原因：**
- 内存限制配置过低
- 应用存在内存泄漏
- 突发流量导致内存暴涨
- JVM堆内存配置不当
""",
        "steps_detail": """
### 步骤1：确认告警信息

检查告警详情，确认：
- **告警等级**：P1
- **Pod信息**：Pod名称、Pod IP、所属服务
- **当前值**：如 +Inf（表示内存使用率达到100%）

### 步骤2：初步分析

**容器名称分析：**
- 注意容器名称，如 hello-world 可能是测试环境
- 评估业务影响

**初步判断：**
- 很可能是测试环境或测试服务
- 需要确认是否影响生产业务

### 步骤3：问题调研

**联系相关团队：**
- 在告警群组中询问是否知晓问题
- 确认服务归属（如dify相关服务）

### 步骤4：检查服务状态

**容器云平台检查：**
- 登录容器云管理平台
- 找到对应服务和Pod
- 检查：
  - Pod运行状态
  - 内存使用情况
  - CPU使用率
  - 重启次数
  - 是否存在OOM Kill

### 步骤5：处理措施

**如果是测试服务：**
- 确认测试完成后可以清理
- 通知相关开发人员

**如果是正式服务出现OOM：**
- 检查内存限制配置
- 分析内存泄漏可能性
- 考虑扩容或重启操作

**容器操作（如需要）：**
- 在Pod列表中选择对应实例
- 执行重启或扩容操作
- 监控处理进度

### 步骤6：问题解决确认

- [ ] 内存使用率恢复正常
- [ ] Pod运行状态正常
- [ ] 无业务影响
- [ ] 告警解除

### 总结

**后续建议：** 建议测试环境完善资源限制配置，避免类似告警
""",
    },
}


def remove_responsibility_team_row(content):
    """Remove the 责任团队 row from the overview table."""
    # Pattern to match the responsibility team row in the table
    content = re.sub(
        r'\| \*\*责任团队\*\* \| [^\|]+ \|\n',
        '',
        content
    )
    return content


def add_frequent_alert_badge(content, alert_id):
    """Add a frequent alert badge if applicable."""
    if alert_id in FREQUENT_ALERTS:
        # Add badge after the title
        content = re.sub(
            r'(# .+)\n',
            r'\1\n\n> **⭐ 高频告警** - 此告警在生产环境中频繁出现，已有详细处理案例和最佳实践。\n',
            content,
            count=1
        )
    return content


def update_title_in_content(content, new_filename):
    """Update the title inside the markdown to match the new filename."""
    # Extract alert name from filename (remove ALR-XXX prefix and .md suffix)
    alert_name_match = re.search(r'ALR-\d+(.+)\.md$', new_filename)
    if alert_name_match:
        new_title = f"# {new_filename.replace('.md', '')}"
        # Replace the first heading
        content = re.sub(r'^# .+$', new_title, content, count=1, flags=re.MULTILINE)
    return content


def enhance_with_wiki_content(content, alert_id):
    """Enhance runbook content with wiki-based information."""
    if alert_id not in WIKI_ENHANCEMENTS:
        return content

    wiki_data = WIKI_ENHANCEMENTS[alert_id]

    # Add root cause detail if available
    if "root_cause_detail" in wiki_data:
        # Find the root cause section and enhance it
        if "## 根因分析" in content:
            detail = wiki_data["root_cause_detail"]
            content = re.sub(
                r'(## 根因分析\n\n### 常见原因)',
                f'## 根因分析\n{detail}\n\n### 常见原因',
                content
            )

    # Add detailed steps if available
    if "steps_detail" in wiki_data:
        # Find the processing steps section and replace it
        if "## 处理步骤" in content:
            steps = wiki_data["steps_detail"]
            # Replace the existing processing steps with enhanced version
            content = re.sub(
                r'## 处理步骤\n\n.+?(?=\n---|\n## |$)',
                f'## 处理步骤\n{steps}\n',
                content,
                flags=re.DOTALL
            )

    return content


def process_runbook(filepath, handbook_dir):
    """Process a single runbook file."""
    filename = filepath.name

    # Skip if not in our mapping
    if filename not in ALERT_NAME_MAP:
        print(f"  Skipping (not in mapping): {filename}")
        return None

    new_filename = ALERT_NAME_MAP[filename]
    alert_id = filename.split('_')[0]  # e.g., ALR-023

    # Read content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Remove 责任团队 row
    content = remove_responsibility_team_row(content)

    # 2. Add frequent alert badge if applicable
    content = add_frequent_alert_badge(content, alert_id)

    # 3. Update title in content
    content = update_title_in_content(content, new_filename)

    # 4. Enhance with wiki content
    content = enhance_with_wiki_content(content, alert_id)

    # Write updated content to new filename
    new_filepath = handbook_dir / new_filename
    with open(new_filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Remove old file if different name
    if new_filename != filename:
        os.remove(filepath)

    return new_filename


def main():
    handbook_dir = Path("/app/luckin-alerts-repo/alert-handbooks")

    print("Updating alert handbooks...")
    print("-" * 60)

    processed = 0
    renamed = 0

    for filepath in sorted(handbook_dir.glob("ALR-*.md")):
        old_name = filepath.name
        new_name = process_runbook(filepath, handbook_dir)

        if new_name:
            processed += 1
            if new_name != old_name:
                renamed += 1
                print(f"  {old_name}")
                print(f"    → {new_name}")
            else:
                print(f"  Updated: {old_name}")

    print("-" * 60)
    print(f"Processed {processed} files, renamed {renamed} files")
    print(f"Frequent alerts marked: {len(FREQUENT_ALERTS)}")


if __name__ == "__main__":
    main()
