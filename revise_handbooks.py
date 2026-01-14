#!/usr/bin/env python3
"""
Revise all alert handbooks according to new requirements:
1. Keep only Chinese as display language
2. Remove initial acknowledgment steps
3. Add golden flow (黄金流程) impact check as first step
4. Remove escalation contacts section
5. Remove L2 Support and SRE On-Call from escalation targets
6. Remove document information and revision history sections
7. Remove notes sections at bottom
8. Add reference handbook notice at top
9. Title should be alert name only
"""

import os
import re
import glob

# Alert definitions with their Chinese names
ALERTS = [
    {"id": "ALR-001", "name": "[LCP-Prod-P0]", "chinese_name": "[LCP-Prod-P0] P0级别告警", "category": "Priority Levels", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-002", "name": "[LCP-Prod-P1]", "chinese_name": "[LCP-Prod-P1] P1级别告警", "category": "Priority Levels", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-003", "name": "[LCP-Prod-P2]", "chinese_name": "[LCP-Prod-P2] P2级别告警", "category": "Priority Levels", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-004", "name": "[LCP-Prod-P3]", "chinese_name": "[LCP-Prod-P3] P3级别告警", "category": "Priority Levels", "priority": "P3", "service_level": "L2"},
    {"id": "ALR-005", "name": "datalink-golden-flow-delay-day", "chinese_name": "【数据链路】黄金流程日间-延迟告警", "category": "DataLink", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-006", "name": "datalink-golden-flow-exception-day", "chinese_name": "【数据链路】黄金流程日间-异常告警", "category": "DataLink", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-007", "name": "datalink-offline-core-delay-day", "chinese_name": "【数据链路】离线核心日间-延迟告警", "category": "DataLink", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-008", "name": "datalink-offline-core-exception-day", "chinese_name": "【数据链路】离线核心日间-异常告警", "category": "DataLink", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-009", "name": "datalink-important-delay-day", "chinese_name": "【数据链路】重要任务日间-延迟告警", "category": "DataLink", "priority": "P1", "service_level": "L1"},
    {"id": "ALR-010", "name": "datalink-important-exception-day", "chinese_name": "【数据链路】重要任务日间-异常告警", "category": "DataLink", "priority": "P1", "service_level": "L1"},
    {"id": "ALR-011", "name": "datalink-offline-important-delay-day", "chinese_name": "【数据链路】离线重要日间-延迟告警", "category": "DataLink", "priority": "P1", "service_level": "L1"},
    {"id": "ALR-012", "name": "datalink-offline-important-exception-day", "chinese_name": "【数据链路】离线重要日间-异常告警", "category": "DataLink", "priority": "P1", "service_level": "L1"},
    {"id": "ALR-013", "name": "datalink-task-delay-night", "chinese_name": "【数据链路】任务夜间-延迟告警", "category": "DataLink", "priority": "P2", "service_level": "L2"},
    {"id": "ALR-014", "name": "datalink-task-exception-night", "chinese_name": "【数据链路】任务夜间-异常告警", "category": "DataLink", "priority": "P2", "service_level": "L2"},
    {"id": "ALR-015", "name": "datalink-regular-delay-day", "chinese_name": "【数据链路】常规任务日间-延迟告警", "category": "DataLink", "priority": "P2", "service_level": "L2"},
    {"id": "ALR-016", "name": "datalink-regular-exception-day", "chinese_name": "【数据链路】常规任务日间-异常告警", "category": "DataLink", "priority": "P2", "service_level": "L2"},
    {"id": "ALR-017", "name": "datalink-offline-regular-delay-day", "chinese_name": "【数据链路】离线常规日间-延迟告警", "category": "DataLink", "priority": "P2", "service_level": "L2"},
    {"id": "ALR-018", "name": "datalink-offline-regular-exception-day", "chinese_name": "【数据链路】离线常规日间-异常告警", "category": "DataLink", "priority": "P2", "service_level": "L2"},
    {"id": "ALR-019", "name": "db-rds-cpu-90-3min-v1", "chinese_name": "【DB告警】AWS-RDS CPU使用率连续三分钟大于90%", "category": "Database-RDS", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-020", "name": "db-rds-cpu-90-3min-v2", "chinese_name": "【DB告警】AWS RDS CPU使用率连续三分钟大于90%", "category": "Database-RDS", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-021", "name": "db-rds-vip-unreachable", "chinese_name": "【DB告警】AWS RDS Vip 持续一分钟不通", "category": "Database-RDS", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-022", "name": "db-rds-vip-unreachable-voice", "chinese_name": "【DB告警】AWS RDS Vip 持续一分钟不通 (Voice)", "category": "Database-RDS", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-023", "name": "db-rds-failover-restart", "chinese_name": "【DB告警】AWS RDS Failover或重启", "category": "Database-RDS", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-024", "name": "db-rds-failover-restart-voice", "chinese_name": "【DB告警】AWS RDS Failover或重启 (Voice)", "category": "Database-RDS", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-025", "name": "db-rds-slow-queries-300-v1", "chinese_name": "【DB告警】AWS-RDS 慢查询数量持续三分钟大于300个", "category": "Database-RDS", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-026", "name": "db-rds-slow-queries-300-v2", "chinese_name": "【DB告警】AWS RDS 慢查询数量持续三分钟大于300个", "category": "Database-RDS", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-027", "name": "db-rds-active-threads-24-v1", "chinese_name": "【DB告警】AWS-RDS 活跃线程持续两分钟大于24", "category": "Database-RDS", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-028", "name": "db-rds-active-threads-24-v2", "chinese_name": "【DB告警】AWS RDS 活跃线程持续两分钟大于24", "category": "Database-RDS", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-029", "name": "db-rds-disk-low-10g", "chinese_name": "【DB告警】AWS RDS 磁盘空间连续3分钟不足10G", "category": "Database-RDS", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-030", "name": "db-mongo-cpu-90", "chinese_name": "【MongoDB告警】AWS DocumentDB CPU使用率超过90%", "category": "Database-MongoDB", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-031", "name": "db-mongo-cpu-90-voice", "chinese_name": "【MongoDB告警】AWS DocumentDB CPU使用率超过90% (Voice)", "category": "Database-MongoDB", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-032", "name": "db-mongo-memory-500m", "chinese_name": "【MongoDB告警】DocumentDB 可用内存不足500MB", "category": "Database-MongoDB", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-033", "name": "db-es-cpu-90", "chinese_name": "【ES告警】OpenSearch CPU使用率超过90%", "category": "Database-OpenSearch", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-034", "name": "db-es-cpu-90-voice", "chinese_name": "【ES告警】OpenSearch CPU使用率超过90% (Voice)", "category": "Database-OpenSearch", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-035", "name": "db-es-cluster-red", "chinese_name": "【ES告警】OpenSearch集群状态为RED", "category": "Database-OpenSearch", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-036", "name": "db-es-cluster-red-voice", "chinese_name": "【ES告警】OpenSearch集群状态为RED (Voice)", "category": "Database-OpenSearch", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-037", "name": "db-es-cluster-yellow", "chinese_name": "【ES告警】OpenSearch集群状态为YELLOW", "category": "Database-OpenSearch", "priority": "P1", "service_level": "L1"},
    {"id": "ALR-038", "name": "db-es-disk-10g", "chinese_name": "【ES告警】OpenSearch磁盘空间不足10G", "category": "Database-OpenSearch", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-039", "name": "db-es-disk-10g-voice", "chinese_name": "【ES告警】OpenSearch磁盘空间不足10G (Voice)", "category": "Database-OpenSearch", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-040", "name": "db-redis-cpu-90", "chinese_name": "【Redis告警】ElastiCache CPU使用率超过90%", "category": "Database-Redis", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-041", "name": "db-redis-cpu-70-3min", "chinese_name": "【Redis告警】ElastiCache CPU使用率连续三分钟超过70%", "category": "Database-Redis", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-042", "name": "db-redis-memory-70", "chinese_name": "【Redis告警】ElastiCache 内存使用率超过70%", "category": "Database-Redis", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-043", "name": "db-redis-client-blocked", "chinese_name": "【Redis告警】ElastiCache 客户端阻塞", "category": "Database-Redis", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-044", "name": "db-redis-latency-2ms", "chinese_name": "【Redis告警】ElastiCache 延迟超过2ms", "category": "Database-Redis", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-045", "name": "db-redis-buffer-32m", "chinese_name": "【Redis告警】ElastiCache 复制缓冲区超过32MB", "category": "Database-Redis", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-046", "name": "db-redis-traffic-32mbps", "chinese_name": "【Redis告警】ElastiCache 网络流量超过32Mbps", "category": "Database-Redis", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-047", "name": "db-redis-key-eviction", "chinese_name": "【Redis告警】ElastiCache Key驱逐告警", "category": "Database-Redis", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-048", "name": "db-redis-connections-30", "chinese_name": "【Redis告警】ElastiCache 连接数超过30", "category": "Database-Redis", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-049", "name": "db-redis-collection-failed", "chinese_name": "【Redis告警】ElastiCache 数据采集失败", "category": "Database-Redis", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-050", "name": "db-exporter-abnormal", "chinese_name": "【DB告警】数据库Exporter异常", "category": "Database-Exporter", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-051", "name": "upush-sms-provider-failures-50", "chinese_name": "【UPUSH告警】SMS通道下发失败次数超过50次", "category": "SMS-UPUSH", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-052", "name": "upush-sms-return-failures-200", "chinese_name": "【UPUSH告警】SMS通道返回失败次数超过200次", "category": "SMS-UPUSH", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-053", "name": "upush-marketing-receipt-60", "chinese_name": "【UPUSH告警】营销短信回执率低于60%", "category": "SMS-UPUSH", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-054", "name": "upush-marketing-filtered-100", "chinese_name": "【UPUSH告警】营销短信被过滤次数超过100次", "category": "SMS-UPUSH", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-055", "name": "upush-industry-receipt-70", "chinese_name": "【UPUSH告警】行业短信回执率低于70%", "category": "SMS-UPUSH", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-056", "name": "upush-industry-filtered-50", "chinese_name": "【UPUSH告警】行业短信被过滤次数超过50次", "category": "SMS-UPUSH", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-057", "name": "upush-verification-volume-30", "chinese_name": "【UPUSH告警】验证码发送量低于30/分钟", "category": "SMS-UPUSH", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-058", "name": "upush-verification-receipt-70", "chinese_name": "【UPUSH告警】验证码回执率低于70%", "category": "SMS-UPUSH", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-059", "name": "upush-verification-filtered-50", "chinese_name": "【UPUSH告警】验证码被过滤次数超过50次", "category": "SMS-UPUSH", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-060", "name": "izeus-strategy1-exceptions-2", "chinese_name": "【iZeus告警】异常数量超过2个 (策略1)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-061", "name": "izeus-strategy2-exceptions-2", "chinese_name": "【iZeus告警】异常数量超过2个 (策略2)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-062", "name": "izeus-strategy3-exceptions-2", "chinese_name": "【iZeus告警】异常数量超过2个 (策略3)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-063", "name": "izeus-strategy4-exceptions-2", "chinese_name": "【iZeus告警】异常数量超过2个 (策略4)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-064", "name": "izeus-strategy5-exceptions-3", "chinese_name": "【iZeus告警】异常数量超过3个 (策略5)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-065", "name": "izeus-strategy6-exceptions-2", "chinese_name": "【iZeus告警】异常数量超过2个 (策略6)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-066", "name": "izeus-strategy7-exceptions-2", "chinese_name": "【iZeus告警】异常数量超过2个 (策略7)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-067", "name": "izeus-strategy8-exceptions-2", "chinese_name": "【iZeus告警】异常数量超过2个 (策略8)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-068", "name": "izeus-strategy9-exceptions-2", "chinese_name": "【iZeus告警】异常数量超过2个 (策略9)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-069", "name": "izeus-strategy10-jvm-cpu-20", "chinese_name": "【iZeus告警】JVM CPU使用率超过20% (策略10)", "category": "APM-iZeus-Strategy", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-070", "name": "izeus-strategy10-response-1500", "chinese_name": "【iZeus告警】响应时间超过1500ms (策略10)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-071", "name": "izeus-strategy11-endpoint-1", "chinese_name": "【iZeus告警】端点错误数超过1 (策略11)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-072", "name": "izeus-strategy12-endpoint-1", "chinese_name": "【iZeus告警】端点错误数超过1 (策略12)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-073", "name": "izeus-strategy15-exceptions-3", "chinese_name": "【iZeus告警】异常数量超过3个 (策略15)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-074", "name": "izeus-strategy16-endpoint-2", "chinese_name": "【iZeus告警】端点错误数超过2 (策略16)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-075", "name": "izeus-strategy17-endpoint-3", "chinese_name": "【iZeus告警】端点错误数超过3 (策略17)", "category": "APM-iZeus-Strategy", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-076", "name": "izeus-node-cpu-85", "chinese_name": "【iZeus告警】节点CPU使用率超过85%", "category": "APM-iZeus-Infra", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-077", "name": "izeus-node-disk-85", "chinese_name": "【iZeus告警】节点磁盘使用率超过85%", "category": "APM-iZeus-Infra", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-078", "name": "izeus-node-memory-95", "chinese_name": "【iZeus告警】节点内存使用率超过95%", "category": "APM-iZeus-Infra", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-079", "name": "izeus-oap-fgc-5", "chinese_name": "【iZeus告警】OAP Full GC次数超过5次", "category": "APM-iZeus-Infra", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-080", "name": "izeus-storage-thanos-0", "chinese_name": "【iZeus告警】Thanos存储采集为0", "category": "APM-iZeus-Infra", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-081", "name": "izeus-storage-vm-0", "chinese_name": "【iZeus告警】VictoriaMetrics存储采集为0", "category": "APM-iZeus-Infra", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-082", "name": "izeus-transfer-agent-oap-0", "chinese_name": "【iZeus告警】Agent到OAP传输为0", "category": "APM-iZeus-Infra", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-083", "name": "izeus-transfer-oap-oap-0", "chinese_name": "【iZeus告警】OAP到OAP传输为0", "category": "APM-iZeus-Infra", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-084", "name": "izeus-transfer-trace-receiver-0", "chinese_name": "【iZeus告警】Trace Receiver传输为0", "category": "APM-iZeus-Infra", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-085", "name": "default-jvm-gc", "chinese_name": "【默认策略】JVM GC告警", "category": "Default-Strategy", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-086", "name": "default-okhttp-50", "chinese_name": "【默认策略】OkHttp错误数超过50", "category": "Default-Strategy", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-087", "name": "default-exceptions-20", "chinese_name": "【默认策略】异常数量超过20个", "category": "Default-Strategy", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-088", "name": "default-exceptions-5", "chinese_name": "【默认策略】异常数量超过5个", "category": "Default-Strategy", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-089", "name": "pod-cpu-fallback-85", "chinese_name": "【Pod告警】CPU使用率超过85% (Fallback)", "category": "Pod", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-090", "name": "pod-cpu-50-10min", "chinese_name": "【Pod告警】CPU使用率持续10分钟超过50%", "category": "Pod", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-091", "name": "pod-cpu-70-3min", "chinese_name": "【Pod告警】CPU使用率持续3分钟超过70%", "category": "Pod", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-092", "name": "pod-node-heartbeat-lost", "chinese_name": "【Pod告警】Node心跳丢失", "category": "Pod", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-093", "name": "pod-restart-2min", "chinese_name": "【Pod告警】Pod在2分钟内重启", "category": "Pod", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-094", "name": "pod-memory-oom", "chinese_name": "【Pod告警】Pod内存OOM", "category": "Pod", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-095", "name": "pod-threads-3600", "chinese_name": "【Pod告警】Pod线程数超过3600", "category": "Pod", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-096", "name": "pod-io-write-50mb", "chinese_name": "【Pod告警】Pod IO写入超过50MB/s", "category": "Pod", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-097", "name": "pod-io-read-50mb", "chinese_name": "【Pod告警】Pod IO读取超过50MB/s", "category": "Pod", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-098", "name": "pod-network-ingress-30mb", "chinese_name": "【Pod告警】Pod入站流量超过30MB/s", "category": "Pod", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-099", "name": "pod-network-egress-30mb", "chinese_name": "【Pod告警】Pod出站流量超过30MB/s", "category": "Pod", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-100", "name": "vm-cpu-load-1x", "chinese_name": "【VM告警】CPU负载超过1倍核心数", "category": "VM", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-101", "name": "vm-cpu-avg-80", "chinese_name": "【VM告警】CPU平均使用率超过80%", "category": "VM", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-102", "name": "vm-cpu-iowait-80", "chinese_name": "【VM告警】CPU IOWait超过80%", "category": "VM", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-103", "name": "vm-cpu-steal-10", "chinese_name": "【VM告警】CPU Steal超过10%", "category": "VM", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-104", "name": "vm-inodes-95", "chinese_name": "【VM告警】Inode使用率超过95%", "category": "VM", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-105", "name": "vm-filesystem-readonly", "chinese_name": "【VM告警】文件系统只读", "category": "VM", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-106", "name": "vm-io-latency-90ms", "chinese_name": "【VM告警】IO延迟超过90ms", "category": "VM", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-107", "name": "vm-io-usage-70", "chinese_name": "【VM告警】IO使用率超过70%", "category": "VM", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-108", "name": "vm-tcp-retransmits-200", "chinese_name": "【VM告警】TCP重传次数超过200", "category": "VM", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-109", "name": "vm-memory-90-10min", "chinese_name": "【VM告警】内存使用率持续10分钟超过90%", "category": "VM", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-110", "name": "vm-heartbeat-lost-10min", "chinese_name": "【VM告警】心跳丢失超过10分钟", "category": "VM", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-111", "name": "vm-disk-90", "chinese_name": "【VM告警】磁盘使用率超过90%", "category": "VM", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-112", "name": "vm-network-drop-in-20", "chinese_name": "【VM告警】入站网络丢包超过20", "category": "VM", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-113", "name": "vm-network-error-in-20", "chinese_name": "【VM告警】入站网络错误超过20", "category": "VM", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-114", "name": "vm-network-drop-out-20", "chinese_name": "【VM告警】出站网络丢包超过20", "category": "VM", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-115", "name": "vm-network-error-out-20", "chinese_name": "【VM告警】出站网络错误超过20", "category": "VM", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-116", "name": "vm-nic-down", "chinese_name": "【VM告警】网卡Down", "category": "VM", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-117", "name": "business-cancelled-orders", "chinese_name": "【业务告警】取消订单数异常", "category": "Business", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-118", "name": "business-complete-orders-0", "chinese_name": "【业务告警】完成订单数为0", "category": "Business", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-119", "name": "business-order-support-0", "chinese_name": "【业务告警】订单支持数为0", "category": "Business", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-120", "name": "business-registrations-0", "chinese_name": "【业务告警】用户注册数为0", "category": "Business", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-121", "name": "business-payments-500", "chinese_name": "【业务告警】支付金额异常(超过500)", "category": "Business", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-122", "name": "risk-global-prebreak", "chinese_name": "【风控告警】全局预熔断", "category": "Risk Control", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-123", "name": "risk-global-break", "chinese_name": "【风控告警】全局熔断", "category": "Risk Control", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-124", "name": "risk-scene-prebreak", "chinese_name": "【风控告警】场景预熔断", "category": "Risk Control", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-125", "name": "risk-scene-break", "chinese_name": "【风控告警】场景熔断", "category": "Risk Control", "priority": "P0", "service_level": "L0"},
    {"id": "ALR-126", "name": "risk-order-rpc-spike", "chinese_name": "【风控告警】订单RPC调用量飙升", "category": "Risk Control", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-127", "name": "risk-payment-rpc-spike", "chinese_name": "【风控告警】支付RPC调用量飙升", "category": "Risk Control", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-128", "name": "risk-register-rpc-spike", "chinese_name": "【风控告警】注册RPC调用量飙升", "category": "Risk Control", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-129", "name": "risk-login-rpc-spike", "chinese_name": "【风控告警】登录RPC调用量飙升", "category": "Risk Control", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-130", "name": "risk-sms-rpc-spike", "chinese_name": "【风控告警】短信RPC调用量飙升", "category": "Risk Control", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-131", "name": "gateway-error-rate-15", "chinese_name": "【网关告警】错误率超过15%", "category": "Gateway", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-132", "name": "network-probe-failed-15s", "chinese_name": "【网络告警】网络探测失败超过15秒", "category": "Network", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-133", "name": "grafana-slow-query-spike", "chinese_name": "【Grafana告警】慢查询数量飙升", "category": "Grafana", "priority": "P2", "service_level": "L1"},
    {"id": "ALR-134", "name": "grafana-slow-query-critical", "chinese_name": "【Grafana告警】慢查询数量严重", "category": "Grafana", "priority": "P1", "service_level": "L0"},
    {"id": "ALR-135", "name": "grafana-slow-query-weekly", "chinese_name": "【Grafana告警】慢查询数量周报", "category": "Grafana", "priority": "P3", "service_level": "L2"},
]

def get_team_info(category):
    """Get team info based on category"""
    team_map = {
        "Priority Levels": ("DevOps", "DevOps团队"),
        "DataLink": ("DataLink", "数据链路团队"),
        "Database-RDS": ("DBA", "DBA团队"),
        "Database-MongoDB": ("DBA", "DBA团队"),
        "Database-OpenSearch": ("DBA", "DBA团队"),
        "Database-Redis": ("DBA", "DBA团队"),
        "Database-Exporter": ("DBA", "DBA团队"),
        "SMS-UPUSH": ("UPUSH", "消息推送团队"),
        "APM-iZeus-Strategy": ("APM", "APM团队"),
        "APM-iZeus-Infra": ("APM", "APM团队"),
        "Default-Strategy": ("DevOps", "DevOps团队"),
        "Pod": ("DevOps", "DevOps团队"),
        "VM": ("DevOps", "DevOps团队"),
        "Business": ("Sales", "销售业务团队"),
        "Risk Control": ("Risk", "风控团队"),
        "Gateway": ("MicroService", "微服务团队"),
        "Network": ("DevOps", "DevOps团队"),
        "Grafana": ("DevOps", "DevOps团队"),
    }
    return team_map.get(category, ("DevOps", "DevOps团队"))

def get_golden_flow_impact(category, priority):
    """Determine golden flow impact level"""
    # Categories that directly impact golden flow (customer ordering)
    critical_categories = ["Database-RDS", "Database-Redis", "Business", "Risk Control", "Gateway", "Pod"]

    if priority == "P0":
        return "high"
    elif priority == "P1" and category in critical_categories:
        return "high"
    elif priority == "P1":
        return "medium"
    else:
        return "low"

def get_diagnostic_commands(category):
    """Get category-specific diagnostic commands"""
    commands = {
        "Database-RDS": '''```bash
# 检查RDS实例状态
aws rds describe-db-instances \\
  --query 'DBInstances[?starts_with(DBInstanceIdentifier, `luckyus`)].{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Class:DBInstanceClass}'

# 检查RDS性能指标
aws cloudwatch get-metric-statistics \\
  --namespace AWS/RDS \\
  --metric-name CPUUtilization \\
  --dimensions Name=DBInstanceIdentifier,Value=[INSTANCE_ID] \\
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \\
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \\
  --period 300 \\
  --statistics Average Maximum

# 检查慢查询
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW PROCESSLIST;"
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW FULL PROCESSLIST;"

# 检查InnoDB状态
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW ENGINE INNODB STATUS\\G"
```''',
        "Database-Redis": '''```bash
# 检查ElastiCache集群状态
aws elasticache describe-cache-clusters \\
  --show-cache-node-info

# 检查Redis内存使用
redis-cli -h [REDIS_ENDPOINT] INFO memory

# 检查Redis客户端连接
redis-cli -h [REDIS_ENDPOINT] CLIENT LIST

# 检查Redis慢日志
redis-cli -h [REDIS_ENDPOINT] SLOWLOG GET 10
```''',
        "Database-MongoDB": '''```bash
# 检查DocumentDB集群状态
aws docdb describe-db-clusters

# 检查DocumentDB实例状态
aws docdb describe-db-instances

# 检查MongoDB当前操作
mongo --host [DOCDB_ENDPOINT] --eval "db.currentOp()"

# 检查MongoDB服务器状态
mongo --host [DOCDB_ENDPOINT] --eval "db.serverStatus()"
```''',
        "Database-OpenSearch": '''```bash
# 检查OpenSearch域状态
aws opensearch describe-domain --domain-name [DOMAIN_NAME]

# 检查集群健康状态
curl -X GET "https://[OPENSEARCH_ENDPOINT]/_cluster/health?pretty"

# 检查节点状态
curl -X GET "https://[OPENSEARCH_ENDPOINT]/_cat/nodes?v"

# 检查索引状态
curl -X GET "https://[OPENSEARCH_ENDPOINT]/_cat/indices?v"
```''',
        "Pod": '''```bash
# 检查Pod状态
kubectl get pods -n [NAMESPACE] -o wide

# 检查Pod日志
kubectl logs -n [NAMESPACE] [POD_NAME] --tail=100

# 检查Pod详情
kubectl describe pod -n [NAMESPACE] [POD_NAME]

# 检查Pod资源使用
kubectl top pods -n [NAMESPACE]

# 检查Node资源
kubectl top nodes
```''',
        "VM": '''```bash
# 检查CPU使用率
top -bn1 | head -20

# 检查内存使用
free -h

# 检查磁盘使用
df -h

# 检查IO状态
iostat -x 1 5

# 检查网络连接
netstat -tunlp | head -20
ss -tunlp | head -20
```''',
        "DataLink": '''```bash
# 检查DataLink任务状态
# 通过DataLink管理后台查看任务执行状态

# 检查Kafka消费者延迟
kafka-consumer-groups.sh --bootstrap-server [KAFKA_BROKER] --describe --group [GROUP_NAME]

# 检查Flink作业状态
# 通过Flink Dashboard查看作业运行状态
```''',
        "SMS-UPUSH": '''```bash
# 检查UPUSH服务状态
kubectl get pods -n upush -o wide

# 检查UPUSH服务日志
kubectl logs -n upush -l app=upush-service --tail=100

# 检查短信通道状态
# 通过UPUSH管理后台查看通道状态和发送统计
```''',
        "Business": '''```bash
# 检查订单服务状态
kubectl get pods -n sales -l app=isalesorderservice -o wide

# 检查订单服务日志
kubectl logs -n sales -l app=isalesorderservice --tail=100

# 检查业务指标
# 通过Grafana Business Metrics仪表板查看
```''',
        "Risk Control": '''```bash
# 检查风控服务状态
kubectl get pods -n risk -o wide

# 检查风控服务日志
kubectl logs -n risk -l app=risk-service --tail=100

# 检查风控熔断状态
# 通过风控管理后台查看熔断规则和触发状态
```''',
        "Gateway": '''```bash
# 检查API网关状态
kubectl get pods -n gateway -o wide

# 检查网关日志
kubectl logs -n gateway -l app=luckyapigateway --tail=100

# 检查网关错误率
# 通过Grafana API Gateway仪表板查看
```''',
    }
    return commands.get(category, '''```bash
# 检查相关服务状态
kubectl get pods -A | grep -i [SERVICE_NAME]

# 检查服务日志
kubectl logs -n [NAMESPACE] [POD_NAME] --tail=100

# 检查Grafana仪表板
# 访问相关监控仪表板查看详细指标
```''')

def get_common_causes(category):
    """Get category-specific common causes"""
    causes = {
        "Database-RDS": '''1. 复杂或未优化的SQL查询消耗过多资源
2. 缺少索引导致全表扫描
3. 并发连接数过高
4. 锁等待或死锁问题
5. 实例规格不足以支撑当前负载
6. 大量慢查询累积''',
        "Database-Redis": '''1. 内存使用接近上限
2. 大Key操作阻塞
3. 客户端连接数过多
4. 网络带宽瓶颈
5. 持久化操作影响性能
6. 热点Key导致负载不均''',
        "Database-MongoDB": '''1. 查询未使用索引
2. 内存不足导致频繁换页
3. 写入量过大
4. 连接池配置不合理
5. 复制延迟过高''',
        "Database-OpenSearch": '''1. 索引分片配置不合理
2. 查询复杂度过高
3. 磁盘空间不足
4. 内存压力过大
5. 节点故障导致集群状态异常''',
        "Pod": '''1. 应用内存泄漏
2. CPU密集型操作
3. 线程池配置不当
4. JVM参数配置不合理
5. 外部依赖响应慢导致线程阻塞
6. 容器资源限制过低''',
        "VM": '''1. 应用进程资源占用过高
2. 磁盘IO瓶颈
3. 内存泄漏或不足
4. 网络问题
5. 系统进程异常
6. 硬件故障''',
        "DataLink": '''1. 上游数据源延迟
2. 数据量突增
3. ETL任务配置问题
4. Kafka消费者延迟
5. 目标数据库性能问题
6. 网络连接问题''',
        "SMS-UPUSH": '''1. 短信通道故障
2. 运营商限流
3. 内容被过滤
4. 账户余额不足
5. 网络连接问题
6. 服务实例异常''',
        "Business": '''1. 支付通道问题
2. 库存系统异常
3. 订单服务故障
4. 数据库连接问题
5. 缓存失效
6. 外部依赖服务异常''',
        "Risk Control": '''1. 风控规则触发
2. 异常流量攻击
3. 业务逻辑异常
4. 配置变更导致
5. 上游服务异常
6. 数据一致性问题''',
        "Gateway": '''1. 后端服务异常
2. 网络连接问题
3. 配置错误
4. 证书过期
5. 限流策略触发
6. 负载不均衡''',
    }
    return causes.get(category, '''1. 服务实例异常
2. 配置变更导致
3. 资源不足
4. 网络问题
5. 依赖服务故障
6. 数据异常''')

def get_resolution_steps(category):
    """Get category-specific resolution steps"""
    steps = {
        "Database-RDS": '''### 慢查询导致

**步骤 1:** 识别消耗资源最高的查询: `SHOW PROCESSLIST`

**步骤 2:** 分析慢查询日志，找出问题SQL

**步骤 3:** 使用 `EXPLAIN` 分析查询执行计划

**步骤 4:** 添加必要索引或优化查询语句

**步骤 5:** 如需紧急处理可KILL长时间运行的查询: `KILL [process_id]`

### 连接数过高

**步骤 1:** 检查当前连接数: `SHOW STATUS LIKE 'Threads_connected'`

**步骤 2:** 识别占用连接的应用

**步骤 3:** 优化应用连接池配置

**步骤 4:** 考虑增加max_connections参数

**步骤 5:** 评估是否需要升级实例规格''',
        "Database-Redis": '''### 内存使用过高

**步骤 1:** 检查内存使用: `INFO memory`

**步骤 2:** 查找大Key: `redis-cli --bigkeys`

**步骤 3:** 分析Key过期策略是否合理

**步骤 4:** 清理过期或无用数据

**步骤 5:** 考虑扩容或数据分片

### 客户端连接问题

**步骤 1:** 检查客户端连接: `CLIENT LIST`

**步骤 2:** 识别异常连接来源

**步骤 3:** 检查应用连接池配置

**步骤 4:** 关闭空闲连接: `CLIENT KILL`''',
        "Pod": '''### CPU使用率过高

**步骤 1:** 检查Pod资源使用: `kubectl top pods`

**步骤 2:** 查看应用日志排查CPU密集操作

**步骤 3:** 分析线程堆栈: `jstack [PID]`

**步骤 4:** 优化代码或增加Pod资源限制

**步骤 5:** 考虑水平扩容增加副本数

### Pod重启

**步骤 1:** 检查重启原因: `kubectl describe pod`

**步骤 2:** 查看之前容器日志: `kubectl logs --previous`

**步骤 3:** 检查是否OOM或健康检查失败

**步骤 4:** 调整资源配置或修复应用问题''',
        "VM": '''### CPU使用率过高

**步骤 1:** 使用 `top` 或 `htop` 查看进程CPU使用

**步骤 2:** 分析高CPU进程

**步骤 3:** 检查是否有异常进程

**步骤 4:** 优化应用或增加资源

### 磁盘空间不足

**步骤 1:** 检查磁盘使用: `df -h`

**步骤 2:** 查找大文件: `du -sh /* | sort -rh | head -20`

**步骤 3:** 清理日志文件和临时文件

**步骤 4:** 考虑扩容磁盘''',
    }
    return steps.get(category, '''### 通用处理步骤

**步骤 1:** 检查服务状态和日志

**步骤 2:** 分析告警触发原因

**步骤 3:** 根据具体情况采取相应措施

**步骤 4:** 验证问题是否解决

**步骤 5:** 记录处理过程和经验''')

def get_related_alerts(category):
    """Get related alerts based on category"""
    related = {
        "Database-RDS": [
            "【DB告警】AWS-RDS CPU使用率连续三分钟大于90%",
            "【DB告警】AWS RDS 慢查询数量持续三分钟大于300个",
            "【DB告警】AWS RDS 活跃线程持续两分钟大于24",
            "【DB告警】AWS RDS 磁盘空间连续3分钟不足10G",
            "【DB告警】AWS RDS Vip 持续一分钟不通",
        ],
        "Database-Redis": [
            "【Redis告警】ElastiCache CPU使用率超过90%",
            "【Redis告警】ElastiCache 内存使用率超过70%",
            "【Redis告警】ElastiCache 延迟超过2ms",
            "【Redis告警】ElastiCache Key驱逐告警",
            "【Redis告警】ElastiCache 客户端阻塞",
        ],
        "Pod": [
            "【Pod告警】CPU使用率超过85%",
            "【Pod告警】Pod内存OOM",
            "【Pod告警】Pod在2分钟内重启",
            "【Pod告警】Node心跳丢失",
            "【Pod告警】Pod线程数超过3600",
        ],
        "VM": [
            "【VM告警】CPU平均使用率超过80%",
            "【VM告警】内存使用率持续10分钟超过90%",
            "【VM告警】磁盘使用率超过90%",
            "【VM告警】心跳丢失超过10分钟",
            "【VM告警】文件系统只读",
        ],
        "Business": [
            "【业务告警】完成订单数为0",
            "【业务告警】用户注册数为0",
            "【业务告警】取消订单数异常",
            "【业务告警】支付金额异常",
            "【风控告警】全局熔断",
        ],
    }
    return related.get(category, [
        "相关类别的其他告警",
        "依赖服务的告警",
        "资源使用相关告警",
    ])

def get_prevention_measures(category):
    """Get category-specific prevention measures"""
    measures = {
        "Database-RDS": '''- 定期审查和优化慢查询
- 设置合理的连接池参数
- 实施数据库性能监控仪表板
- 定期进行容量规划评估
- 配置自动存储扩展
- 建立索引审计机制''',
        "Database-Redis": '''- 监控内存使用趋势
- 设置合理的过期策略
- 避免大Key操作
- 配置合理的连接池
- 定期清理无用数据
- 建立容量规划机制''',
        "Pod": '''- 合理配置资源请求和限制
- 实施应用性能监控
- 定期进行容量评估
- 配置健康检查
- 建立自动扩容机制
- 优化JVM参数配置''',
        "VM": '''- 监控资源使用趋势
- 定期清理日志和临时文件
- 配置自动扩容策略
- 建立资源使用告警
- 定期进行系统维护
- 优化应用配置''',
    }
    return measures.get(category, '''- 建立完善的监控体系
- 定期进行容量规划
- 实施自动化运维
- 建立变更管理流程
- 进行定期演练
- 持续优化告警阈值''')

def generate_revised_handbook(alert):
    """Generate revised handbook content"""
    alert_id = alert["id"]
    alert_name = alert["name"]
    chinese_name = alert["chinese_name"]
    category = alert["category"]
    priority = alert["priority"]
    service_level = alert["service_level"]

    team_en, team_cn = get_team_info(category)
    golden_flow_impact = get_golden_flow_impact(category, priority)

    # Build golden flow check step
    if golden_flow_impact == "high":
        golden_flow_step = '''### 第一步: 评估黄金流程影响

**立即评估此告警是否影响黄金流程（用户下单流程）:**

```
关键检查点:
1. 用户是否可以正常打开瑞幸咖啡App
2. 用户是否可以正常浏览菜单和选择商品
3. 用户是否可以正常下单
4. 用户是否可以正常支付

如果以上任何一个环节受阻，说明黄金流程受影响!
```

**如果黄金流程受影响:**
- 这是严重事故，需要立即响应
- 通知中国团队所有相关成员（包括半夜唤醒）
- 启动紧急响应流程
- 同步升级至Team Lead

**如果黄金流程未受影响:**
- 可以按正常流程排查
- 观察告警是否自动恢复（部分告警可能是瞬时波动）
- 记录并分析是否为误报'''
    elif golden_flow_impact == "medium":
        golden_flow_step = '''### 第一步: 评估黄金流程影响

**评估此告警对黄金流程（用户下单流程）的潜在影响:**

```
检查点:
1. 相关服务是否在订单链路中
2. 当前异常是否已扩散
3. 是否有关联的P0/P1告警
```

**如果可能影响黄金流程:**
- 提高响应优先级
- 准备通知相关团队
- 密切监控告警状态变化

**如果暂不影响黄金流程:**
- 按常规流程处理
- 观察告警是否自动恢复
- 如果5-10分钟内恢复，可能是瞬时波动，记录并关注'''
    else:
        golden_flow_step = '''### 第一步: 评估告警影响

**检查此告警对业务的影响:**

```
检查点:
1. 告警是否持续存在
2. 是否有关联的高优先级告警
3. 相关服务的整体健康状态
```

**处理建议:**
- 此告警优先级较低，可以按正常流程处理
- 先观察5-10分钟，看告警是否自动恢复
- 部分此类告警可能是瞬时波动导致的误报
- 如果持续存在，再进行详细排查'''

    # Response time based on priority
    response_time_map = {
        "P0": "立即响应（< 5分钟）",
        "P1": "快速响应（< 15分钟）",
        "P2": "标准响应（< 30分钟）",
        "P3": "低优先级响应（< 2小时）"
    }
    response_time = response_time_map.get(priority, "标准响应")

    content = f'''# {chinese_name}

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | {alert_id} |
| **告警名称** | {chinese_name} |
| **优先级** | {priority} |
| **服务等级** | {service_level} |
| **类别** | {category} |
| **响应时间** | {response_time} |
| **责任团队** | {team_cn} |

---

## 告警描述

此告警属于 **{priority}** 优先级，影响 **{service_level}** 级别服务。

**责任团队:** {team_cn}负责处理此类告警。

---

## 立即响应

{golden_flow_step}

### 第二步: 初步诊断

```
1. 检查告警详细信息
2. 查看相关Grafana仪表板
3. 收集诊断信息
4. 检查最近变更记录
```

### 第三步: 深入排查

如果告警持续存在且未自动恢复，执行以下诊断命令:

---

## 诊断命令

{get_diagnostic_commands(category)}

---

## 根因分析

### 常见原因

{get_common_causes(category)}

### 排查清单

- [ ] 确认告警触发时间和频率
- [ ] 检查相关服务健康状态
- [ ] 验证数据库/缓存连接和性能
- [ ] 检查最近的部署或配置变更
- [ ] 分析相关日志是否有异常
- [ ] 检查依赖服务状态
- [ ] 验证网络连接和延迟
- [ ] 检查资源使用情况

---

## 处理步骤

{get_resolution_steps(category)}

---

## 升级标准

### 升级条件

| 条件 | 升级目标 |
|------|---------|
| 初次响应无法解决 | DevOps值班成员 |
| 问题持续恶化 | Team Lead |
| 需要外部支持 | AWS/供应商支持 |

---

## 预防措施

{get_prevention_measures(category)}

---

## 相关告警

以下告警经常与此告警同时出现或有关联关系:

'''

    for related in get_related_alerts(category):
        content += f"- `{related}`\n"

    content += '''
---

## Grafana 仪表板参考

| 仪表板 | 用途 |
|--------|------|
| RDS MySQL Overview | 数据库性能监控 |
| ElastiCache Redis | 缓存性能监控 |
| Kubernetes Pods | 容器监控 |
| Node Exporter | VM/主机监控 |
| iZeus APM | 应用性能监控 |
| DataLink Pipeline | ETL任务监控 |
| Business Metrics | 业务指标监控 |
| Risk Control | 风控监控 |
| API Gateway | 网关监控 |
'''

    return content

def main():
    """Main function to revise all handbooks"""
    handbook_dir = "/app/luckin-alerts-repo/alert-handbooks"

    # Create alert lookup by ID
    alert_lookup = {alert["id"]: alert for alert in ALERTS}

    # Get all existing handbook files
    existing_files = glob.glob(os.path.join(handbook_dir, "ALR-*.md"))

    revised_count = 0

    for filepath in existing_files:
        filename = os.path.basename(filepath)
        # Extract alert ID from filename
        match = re.match(r'(ALR-\d+)_', filename)
        if match:
            alert_id = match.group(1)
            if alert_id in alert_lookup:
                alert = alert_lookup[alert_id]

                # Generate new filename based on alert name
                new_filename = f"{alert_id}_{alert['name']}.md"
                new_filepath = os.path.join(handbook_dir, new_filename)

                # Generate revised content
                content = generate_revised_handbook(alert)

                # Remove old file if different name
                if filepath != new_filepath and os.path.exists(filepath):
                    os.remove(filepath)

                # Write revised content
                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                revised_count += 1
                print(f"Revised: {new_filename}")

    print(f"\nTotal revised: {revised_count} handbooks")

if __name__ == "__main__":
    main()
