#!/usr/bin/env python3
"""
Luckin Coffee USA - Alert Runbook Revision Script
=================================================
This script revises all alert handbooks with REAL system data discovered from:
- Grafana alert rules and dashboards
- Prometheus metrics and labels
- MySQL/Redis/PostgreSQL database configurations
- Kubernetes namespace structure

Author: DevOps Team
Date: 2026-01-14
"""

import os
import re
import json
from pathlib import Path

# =============================================================================
# REAL SYSTEM DATA - Discovered from comprehensive system analysis
# =============================================================================

# Grafana Datasources (actual UIDs)
DATASOURCES = {
    "prometheus_mysql": "ff7hkeec6c9a8e",
    "prometheus_redis": "ff6p0gjt24phce",
    "prometheus_default": "df8o21agxtkw0d",
    "mysql_ldas": "ef5ay9lchfg1sa",
    "mysql_iriskcontrol": "af8p2vx4nhp1ce",
    "mysql_luckyhealth": "af8o704xu3280a",
    "elasticsearch": "ff7ehok3sf56oa"
}

# Grafana Dashboards (actual UIDs and names)
DASHBOARDS = {
    "rds": {
        "uid": "enterprise-rds-health",
        "name": "Enterprise RDS Health Dashboard",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/enterprise-rds-health"
    },
    "mysql_overview": {
        "uid": "mysql-enterprise-monitor",
        "name": "MySQL Enterprise Monitoring Dashboard",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/mysql-enterprise-monitor"
    },
    "mysql_innodb": {
        "uid": "innodb-deep-monitor",
        "name": "InnoDB Deep Monitoring",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/innodb-deep-monitor"
    },
    "mysql_multi": {
        "uid": "mysql-multi-instance",
        "name": "MySQL Multi-Instance Monitor",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/mysql-multi-instance"
    },
    "slow_sql": {
        "uid": "na-slow-sql-governance",
        "name": "NA Weekly Slow SQL Governance",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/na-slow-sql-governance"
    },
    "db_deep_dive": {
        "uid": "na-db-instance-deep-dive",
        "name": "NA DB Instance Deep Dive",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/na-db-instance-deep-dive"
    },
    "fleet_leaderboard": {
        "uid": "na-fleet-leaderboard",
        "name": "NA Fleet Leaderboard by Database",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/na-fleet-leaderboard"
    },
    "elasticache": {
        "uid": "elasticache-redis-overview",
        "name": "ElastiCache Redis Overview",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/elasticache-redis-overview"
    },
    "redis_cluster": {
        "uid": "redis-cluster-monitor",
        "name": "Redis Cluster Monitor",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/redis-cluster-monitor"
    },
    "kubernetes": {
        "uid": "kubernetes-pods",
        "name": "Kubernetes Pods Dashboard",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/kubernetes-pods"
    },
    "node_exporter": {
        "uid": "node-exporter-full",
        "name": "Node Exporter Full",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/node-exporter-full"
    },
    "api_gateway": {
        "uid": "api-gateway-monitor",
        "name": "API Gateway Monitor",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/api-gateway-monitor"
    },
    "elasticsearch_dash": {
        "uid": "elasticsearch-monitor",
        "name": "Elasticsearch/OpenSearch Monitor",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/elasticsearch-monitor"
    },
    "business_metrics": {
        "uid": "business-metrics",
        "name": "Business Metrics Dashboard",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/business-metrics"
    },
    "risk_control": {
        "uid": "risk-control-monitor",
        "name": "Risk Control Monitor",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/risk-control-monitor"
    },
    "jvm_overview": {
        "uid": "jvm-micrometer",
        "name": "JVM Micrometer Dashboard",
        "url": "https://luckin-na-grafana.lkcoffee.com/d/jvm-micrometer"
    }
}

# Critical MySQL Databases (discovered from system)
MYSQL_DATABASES = {
    "golden_flow": [
        "aws-luckyus-salesorder-rw",
        "aws-luckyus-salespayment-rw",
        "aws-luckyus-salescrm-rw",
        "aws-luckyus-salescommodity-rw",
        "aws-luckyus-salesmarket-rw",
        "aws-luckyus-salesmember-rw"
    ],
    "risk_control": [
        "aws-luckyus-iriskcontrolservice-rw",
        "aws-luckyus-iriskcontrol-rw"
    ],
    "auth": [
        "aws-luckyus-unionauth-rw",
        "aws-luckyus-authservice-rw"
    ],
    "finance": [
        "aws-luckyus-ifiaccounting-rw",
        "aws-luckyus-ifichargecontrol-rw",
        "aws-luckyus-ifitax-rw",
        "aws-luckyus-billcenterservice-rw"
    ],
    "supply_chain": [
        "aws-luckyus-scm-asset-rw",
        "aws-luckyus-scm-commodity-rw",
        "aws-luckyus-scm-ordering-rw",
        "aws-luckyus-scm-purchase-rw",
        "aws-luckyus-scm-shopstock-rw"
    ],
    "data_platform": [
        "aws-luckyus-ldas-rw",
        "aws-luckyus-bigdata-rw",
        "aws-luckyus-datamarket-rw"
    ]
}

# Critical Redis Clusters (discovered from system - 74+ instances)
REDIS_CLUSTERS = {
    "golden_flow": [
        "luckyus-isales-order",
        "luckyus-isales-session",
        "luckyus-isales-commodity",
        "luckyus-isales-crm",
        "luckyus-isales-market",
        "luckyus-isales-member"
    ],
    "auth": [
        "luckyus-unionauth",
        "luckyus-aapi-unionauth",
        "luckyus-sapi-unionauth",
        "luckyus-open-unionauth",
        "luckyus-auth",
        "luckyus-authservice"
    ],
    "risk_control": [
        "luckyus-iriskcontrol"
    ],
    "api_gateway": [
        "luckyus-apigateway"
    ],
    "messaging": [
        "luckyus-ipushnet",
        "luckyus-iupush",
        "luckyus-imessageflow"
    ]
}

# Kubernetes Namespaces (discovered from system)
K8S_NAMESPACES = {
    "sales": "rd-sales",
    "finance": "rd-finance",
    "supply_chain": "rd-supplychains",
    "frontend": "rd-frontend",
    "iot": "rd-iot",
    "public": "rd-pub",
    "risk_control": "baseservices-riskcontrol",
    "cloud": "baseservices-cloud",
    "devops": "baseservices-devops",
    "api_gateway": "api-gateway",
    "monitoring": "monitor",
    "ingress": "ingress-nginx"
}

# Real PromQL Expressions (discovered from Grafana alert rules)
PROMQL_EXPRESSIONS = {
    # MySQL Metrics
    "mysql_slow_queries_rate": "sum(rate(mysql_global_status_slow_queries[5m])) by (instance)",
    "mysql_slow_queries_weekly": "sum(increase(mysql_global_status_slow_queries[7d])) by (instance)",
    "mysql_threads_connected": "mysql_global_status_threads_connected",
    "mysql_threads_running": "mysql_global_status_threads_running",
    "mysql_connections": "mysql_global_status_connections",
    "mysql_innodb_buffer_pool": "mysql_global_status_innodb_buffer_pool_bytes_data",
    "mysql_innodb_row_lock_waits": "mysql_global_status_innodb_row_lock_waits",
    "mysql_vip_check": "mysql_check_vip",

    # Redis Metrics
    "redis_connected_clients": "redis_connected_clients",
    "redis_blocked_clients": "redis_blocked_clients",
    "redis_memory_used": "redis_memory_used_bytes",
    "redis_memory_max": "redis_memory_max_bytes",
    "redis_cpu_usage": "rate(redis_cpu_user_seconds_total[5m]) + rate(redis_cpu_sys_seconds_total[5m])",
    "redis_commands_total": "rate(redis_commands_total[5m])",
    "redis_keyspace_hits": "rate(redis_keyspace_hits_total[5m])",
    "redis_keyspace_misses": "rate(redis_keyspace_misses_total[5m])",
    "redis_slowlog_length": "redis_slowlog_length",
    "redis_connected_slaves": "redis_connected_slaves",

    # AWS RDS CloudWatch Metrics
    "aws_rds_cpu": "aws_rds_cpuutilization_average",
    "aws_rds_connections": "aws_rds_database_connections_average",
    "aws_rds_free_storage": "aws_rds_free_storage_space_average",
    "aws_rds_read_iops": "aws_rds_read_iops_average",
    "aws_rds_write_iops": "aws_rds_write_iops_average",
    "aws_rds_read_latency": "aws_rds_read_latency_average",
    "aws_rds_write_latency": "aws_rds_write_latency_average",

    # AWS ElastiCache CloudWatch Metrics
    "aws_elasticache_cpu": "aws_elasticache_cpuutilization_average",
    "aws_elasticache_memory": "aws_elasticache_database_memory_usage_percentage_average",
    "aws_elasticache_connections": "aws_elasticache_curr_connections_average",
    "aws_elasticache_evictions": "aws_elasticache_evictions_average",

    # Container Metrics
    "container_cpu_usage": "sum(rate(container_cpu_usage_seconds_total{namespace=~\"rd-.*|baseservices-.*\"}[5m])) by (namespace, pod)",
    "container_memory_usage": "sum(container_memory_working_set_bytes{namespace=~\"rd-.*|baseservices-.*\"}) by (namespace, pod)",
    "container_restarts": "sum(increase(kube_pod_container_status_restarts_total[1h])) by (namespace, pod)",
    "container_oom_events": "sum(increase(container_oom_events_total[1h])) by (namespace, pod)",

    # Node Metrics
    "node_cpu_usage": "100 - (avg by(instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
    "node_memory_usage": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
    "node_disk_usage": "(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100",
    "node_network_receive": "rate(node_network_receive_bytes_total[5m])",
    "node_network_transmit": "rate(node_network_transmit_bytes_total[5m])",

    # JVM Metrics
    "jvm_gc_pause": "rate(jvm_gc_pause_seconds_sum[5m])",
    "jvm_memory_used": "jvm_memory_used_bytes",
    "jvm_threads_live": "jvm_threads_live_threads",
    "jvm_threads_daemon": "jvm_threads_daemon_threads",

    # Kubernetes Metrics
    "kube_pod_status_phase": "kube_pod_status_phase",
    "kube_deployment_replicas": "kube_deployment_spec_replicas",
    "kube_deployment_available": "kube_deployment_status_replicas_available",
    "kube_node_status": "kube_node_status_condition{condition=\"Ready\",status=\"true\"}"
}

# Alert category to dashboard/metric mapping
ALERT_CATEGORY_MAP = {
    "DB": {
        "dashboards": ["rds", "mysql_overview", "mysql_innodb", "slow_sql", "db_deep_dive"],
        "metrics": ["mysql_slow_queries_rate", "mysql_threads_connected", "mysql_connections", "aws_rds_cpu"],
        "databases": "golden_flow"
    },
    "Redis": {
        "dashboards": ["elasticache", "redis_cluster"],
        "metrics": ["redis_connected_clients", "redis_memory_used", "redis_cpu_usage", "aws_elasticache_cpu"],
        "databases": "golden_flow"
    },
    "K8S": {
        "dashboards": ["kubernetes", "node_exporter"],
        "metrics": ["container_cpu_usage", "container_memory_usage", "container_restarts", "kube_pod_status_phase"],
        "namespaces": ["sales", "finance", "supply_chain"]
    },
    "JVM": {
        "dashboards": ["jvm_overview", "kubernetes"],
        "metrics": ["jvm_gc_pause", "jvm_memory_used", "jvm_threads_live"],
        "namespaces": ["sales", "finance"]
    },
    "ES": {
        "dashboards": ["elasticsearch_dash"],
        "metrics": ["aws_es_cluster_status", "aws_es_jvmmemory_pressure"],
        "service": "OpenSearch"
    },
    "Gateway": {
        "dashboards": ["api_gateway"],
        "metrics": ["gateway_request_rate", "gateway_error_rate"],
        "namespaces": ["api_gateway"]
    },
    "Risk": {
        "dashboards": ["risk_control"],
        "metrics": ["iriskcontrol_tenant_scene_result_pv"],
        "namespaces": ["risk_control"],
        "databases": "risk_control"
    },
    "MQ": {
        "dashboards": ["business_metrics"],
        "metrics": ["rabbitmq_queue_messages", "kafka_consumer_lag"],
        "service": "Message Queue"
    }
}

# =============================================================================
# RUNBOOK REVISION FUNCTIONS
# =============================================================================

def get_alert_category(alert_name):
    """Determine the category of an alert based on its name."""
    name_lower = alert_name.lower()

    if "db" in name_lower or "rds" in name_lower or "mysql" in name_lower or "sql" in name_lower:
        return "DB"
    elif "redis" in name_lower or "elasticache" in name_lower or "缓存" in alert_name:
        return "Redis"
    elif "k8s" in name_lower or "pod" in name_lower or "容器" in alert_name or "kubernetes" in name_lower:
        return "K8S"
    elif "jvm" in name_lower or "gc" in name_lower or "heap" in name_lower:
        return "JVM"
    elif "es" in name_lower or "elasticsearch" in name_lower or "opensearch" in name_lower:
        return "ES"
    elif "gateway" in name_lower or "网关" in alert_name or "api" in name_lower:
        return "Gateway"
    elif "risk" in name_lower or "风控" in alert_name:
        return "Risk"
    elif "mq" in name_lower or "rabbitmq" in name_lower or "kafka" in name_lower or "消息" in alert_name:
        return "MQ"
    else:
        return "General"

def generate_diagnostic_section(category, alert_name):
    """Generate enhanced diagnostic commands based on alert category."""

    if category == "DB":
        return f"""## 诊断命令

### AWS RDS 状态检查
```bash
# 检查所有 Luckin US RDS 实例状态
aws rds describe-db-instances \\
  --query 'DBInstances[?starts_with(DBInstanceIdentifier, `luckyus`)].{{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Class:DBInstanceClass,Engine:Engine,Storage:AllocatedStorage}}' \\
  --output table

# 检查特定实例的性能指标 (替换 INSTANCE_ID)
aws cloudwatch get-metric-statistics \\
  --namespace AWS/RDS \\
  --metric-name CPUUtilization \\
  --dimensions Name=DBInstanceIdentifier,Value=[INSTANCE_ID] \\
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \\
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \\
  --period 300 \\
  --statistics Average Maximum
```

### Prometheus 指标查询 (Grafana Explore)
```promql
# 慢查询速率 (每秒)
{PROMQL_EXPRESSIONS['mysql_slow_queries_rate']}

# 活跃连接数
{PROMQL_EXPRESSIONS['mysql_threads_connected']}

# 运行中线程数
{PROMQL_EXPRESSIONS['mysql_threads_running']}

# VIP 健康检查
{PROMQL_EXPRESSIONS['mysql_vip_check']}
```

### MySQL 诊断命令
```sql
-- 查看当前进程列表
SHOW PROCESSLIST;

-- 查看完整进程列表 (包含完整SQL)
SHOW FULL PROCESSLIST;

-- 检查InnoDB状态
SHOW ENGINE INNODB STATUS;

-- 检查慢查询日志状态
SHOW VARIABLES LIKE 'slow_query%';

-- 查看连接状态
SHOW STATUS LIKE 'Threads_%';
SHOW STATUS LIKE 'Connections';

-- 检查锁等待
SELECT * FROM information_schema.innodb_lock_waits;
```

### 关键数据库实例
**黄金流程相关:**
{chr(10).join(['- ' + db for db in MYSQL_DATABASES['golden_flow']])}

**风控相关:**
{chr(10).join(['- ' + db for db in MYSQL_DATABASES['risk_control']])}
"""

    elif category == "Redis":
        return f"""## 诊断命令

### AWS ElastiCache 状态检查
```bash
# 检查所有 Luckin US ElastiCache 集群
aws elasticache describe-cache-clusters \\
  --query 'CacheClusters[?starts_with(CacheClusterId, `luckyus`)].{{ID:CacheClusterId,Status:CacheClusterStatus,Engine:Engine,NodeType:CacheNodeType}}' \\
  --output table

# 检查复制组状态
aws elasticache describe-replication-groups \\
  --query 'ReplicationGroups[?starts_with(ReplicationGroupId, `luckyus`)].{{ID:ReplicationGroupId,Status:Status,NodeType:CacheNodeType}}' \\
  --output table
```

### Prometheus 指标查询 (Grafana Explore)
```promql
# 连接客户端数
{PROMQL_EXPRESSIONS['redis_connected_clients']}

# 阻塞客户端数
{PROMQL_EXPRESSIONS['redis_blocked_clients']}

# 内存使用量
{PROMQL_EXPRESSIONS['redis_memory_used']}

# CPU 使用率
{PROMQL_EXPRESSIONS['redis_cpu_usage']}

# 命令处理速率
{PROMQL_EXPRESSIONS['redis_commands_total']}

# 慢日志长度
{PROMQL_EXPRESSIONS['redis_slowlog_length']}

# 命中率计算
{PROMQL_EXPRESSIONS['redis_keyspace_hits']} / ({PROMQL_EXPRESSIONS['redis_keyspace_hits']} + {PROMQL_EXPRESSIONS['redis_keyspace_misses']})
```

### Redis CLI 诊断命令
```bash
# 连接到 Redis (使用正确的端点)
redis-cli -h [REDIS_ENDPOINT] -p 6379 --tls

# 查看实时统计
INFO

# 查看内存使用
INFO memory

# 查看客户端连接
CLIENT LIST

# 查看慢日志
SLOWLOG GET 10

# 查看键空间统计
INFO keyspace
```

### 关键 Redis 集群
**黄金流程相关:**
{chr(10).join(['- ' + cluster for cluster in REDIS_CLUSTERS['golden_flow']])}

**认证相关:**
{chr(10).join(['- ' + cluster for cluster in REDIS_CLUSTERS['auth']])}
"""

    elif category == "K8S":
        return f"""## 诊断命令

### kubectl 诊断命令
```bash
# 查看所有命名空间的 Pod 状态
kubectl get pods -A | grep -E "(rd-|baseservices-)"

# 查看特定命名空间的 Pod 详情
kubectl get pods -n {K8S_NAMESPACES['sales']} -o wide
kubectl get pods -n {K8S_NAMESPACES['finance']} -o wide

# 查看 Pod 事件
kubectl describe pod [POD_NAME] -n [NAMESPACE]

# 查看 Pod 日志
kubectl logs [POD_NAME] -n [NAMESPACE] --tail=100

# 查看资源使用情况
kubectl top pods -n [NAMESPACE]
kubectl top nodes
```

### Prometheus 指标查询 (Grafana Explore)
```promql
# 容器 CPU 使用率
{PROMQL_EXPRESSIONS['container_cpu_usage']}

# 容器内存使用量
{PROMQL_EXPRESSIONS['container_memory_usage']}

# 容器重启次数 (过去1小时)
{PROMQL_EXPRESSIONS['container_restarts']}

# OOM 事件
{PROMQL_EXPRESSIONS['container_oom_events']}

# Pod 状态
{PROMQL_EXPRESSIONS['kube_pod_status_phase']}

# Deployment 可用副本
{PROMQL_EXPRESSIONS['kube_deployment_available']}
```

### 关键命名空间
**业务服务:**
- 销售: `{K8S_NAMESPACES['sales']}`
- 财务: `{K8S_NAMESPACES['finance']}`
- 供应链: `{K8S_NAMESPACES['supply_chain']}`

**基础服务:**
- 风控: `{K8S_NAMESPACES['risk_control']}`
- API网关: `{K8S_NAMESPACES['api_gateway']}`
- 监控: `{K8S_NAMESPACES['monitoring']}`
"""

    elif category == "JVM":
        return f"""## 诊断命令

### Prometheus 指标查询 (Grafana Explore)
```promql
# GC 暂停时间
{PROMQL_EXPRESSIONS['jvm_gc_pause']}

# JVM 内存使用
{PROMQL_EXPRESSIONS['jvm_memory_used']}

# 活跃线程数
{PROMQL_EXPRESSIONS['jvm_threads_live']}

# 守护线程数
{PROMQL_EXPRESSIONS['jvm_threads_daemon']}

# 堆内存使用率
jvm_memory_used_bytes{{area="heap"}} / jvm_memory_max_bytes{{area="heap"}} * 100
```

### JVM 诊断命令
```bash
# 获取堆转储 (在容器内)
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- jmap -dump:format=b,file=/tmp/heapdump.hprof [PID]

# 查看线程转储
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- jstack [PID]

# 查看 GC 日志
kubectl logs [POD_NAME] -n [NAMESPACE] | grep -i "gc"

# 查看 JVM 参数
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- java -XX:+PrintFlagsFinal -version
```
"""

    else:
        return f"""## 诊断命令

### 通用 Prometheus 指标查询
```promql
# 节点 CPU 使用率
{PROMQL_EXPRESSIONS['node_cpu_usage']}

# 节点内存使用率
{PROMQL_EXPRESSIONS['node_memory_usage']}

# 节点磁盘使用率
{PROMQL_EXPRESSIONS['node_disk_usage']}
```

### 通用诊断命令
```bash
# 检查服务健康状态
curl -s http://[SERVICE_ENDPOINT]/health

# 检查网络连通性
ping [TARGET_HOST]
telnet [TARGET_HOST] [PORT]

# 检查日志
kubectl logs [POD_NAME] -n [NAMESPACE] --tail=100
```
"""

def generate_dashboard_section(category):
    """Generate Grafana dashboard references based on category."""

    category_info = ALERT_CATEGORY_MAP.get(category, {})
    dashboard_keys = category_info.get("dashboards", ["kubernetes", "node_exporter"])

    dashboard_rows = []
    for key in dashboard_keys:
        if key in DASHBOARDS:
            dash = DASHBOARDS[key]
            dashboard_rows.append(f"| [{dash['name']}]({dash['url']}) | {key.replace('_', ' ').title()} 监控 |")

    # Add common dashboards
    if "kubernetes" not in dashboard_keys:
        dash = DASHBOARDS["kubernetes"]
        dashboard_rows.append(f"| [{dash['name']}]({dash['url']}) | 容器监控 |")

    return f"""## Grafana 仪表板参考

| 仪表板 | 用途 |
|--------|------|
{chr(10).join(dashboard_rows)}

**Grafana 访问地址:** https://luckin-na-grafana.lkcoffee.com

**Prometheus 数据源:**
- MySQL 指标: `{DATASOURCES['prometheus_mysql']}`
- Redis 指标: `{DATASOURCES['prometheus_redis']}`
- 默认指标: `{DATASOURCES['prometheus_default']}`
"""

def revise_handbook(filepath):
    """Revise a single handbook file with real system data."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract alert name from content
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if not title_match:
        return content

    alert_name = title_match.group(1)
    category = get_alert_category(alert_name)

    # Replace generic diagnostic section with real data
    diagnostic_section = generate_diagnostic_section(category, alert_name)

    # Find and replace the diagnostic commands section
    # Use lambda to avoid backslash interpretation issues in replacement
    pattern = r'## 诊断命令\n\n```bash\n.*?```'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, lambda m: diagnostic_section.strip(), content, flags=re.DOTALL)
    else:
        # Insert diagnostic section before root cause analysis if not found
        pattern = r'(---\n\n## 根因分析)'
        if re.search(pattern, content):
            replacement = f'---\n\n{diagnostic_section}\n\n---\n\n## 根因分析'
            content = re.sub(pattern, lambda m: replacement, content)

    # Replace generic dashboard section with real data
    dashboard_section = generate_dashboard_section(category)

    pattern = r'## Grafana 仪表板参考\n\n\| 仪表板.*?\| 网关监控 \|'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, lambda m: dashboard_section.strip(), content, flags=re.DOTALL)

    # Add real system context to the alert description
    if category in ALERT_CATEGORY_MAP:
        category_info = ALERT_CATEGORY_MAP[category]

        # Add service context
        context_addition = f"\n\n**系统上下文:** 此告警涉及 "
        if "databases" in category_info:
            db_type = category_info["databases"]
            if db_type in MYSQL_DATABASES:
                context_addition += f"{len(MYSQL_DATABASES[db_type])} 个关键 MySQL 数据库实例。"
        if "namespaces" in category_info:
            ns_list = [K8S_NAMESPACES.get(ns, ns) for ns in category_info["namespaces"]]
            context_addition += f"Kubernetes 命名空间: {', '.join(ns_list)}。"

        # Insert after alert description
        pattern = r'(此告警属于 \*\*P\d+\*\* 优先级.*?负责处理此类告警。)'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, lambda m: m.group(1) + context_addition, content, flags=re.DOTALL)

    return content

def main():
    """Main function to revise all runbooks."""

    handbook_dir = Path("/app/luckin-alerts-repo/alert-handbooks")
    revised_count = 0

    print("=" * 60)
    print("Luckin Coffee USA - Alert Runbook Revision")
    print("=" * 60)
    print(f"\nSource directory: {handbook_dir}")
    print(f"Total dashboards mapped: {len(DASHBOARDS)}")
    print(f"Total MySQL databases: {sum(len(v) for v in MYSQL_DATABASES.values())}")
    print(f"Total Redis clusters: {sum(len(v) for v in REDIS_CLUSTERS.values())}")
    print(f"Total K8S namespaces: {len(K8S_NAMESPACES)}")
    print(f"Total PromQL expressions: {len(PROMQL_EXPRESSIONS)}")
    print("\n" + "-" * 60)

    for filepath in sorted(handbook_dir.glob("*.md")):
        print(f"Revising: {filepath.name}")

        try:
            revised_content = revise_handbook(filepath)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(revised_content)

            revised_count += 1
        except Exception as e:
            print(f"  ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"Revision complete! {revised_count} handbooks updated.")
    print("=" * 60)

if __name__ == "__main__":
    main()
