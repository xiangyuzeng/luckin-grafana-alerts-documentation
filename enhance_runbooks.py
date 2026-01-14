#!/usr/bin/env python3
"""
Enhanced Runbook Generator for Luckin Coffee USA DevOps
This script enhances alert handbooks with:
1. A new "告警解析" section explaining alert meaning and impact
2. Specific access instructions in 诊断命令 section
3. Actual server names, AWS accounts, and endpoints
4. Comprehensive root causes specific to the system
"""

import re
from pathlib import Path

# System Configuration
AWS_CONFIG = {
    "account_id": "257394478466",
    "region": "us-east-1",
    "rds_endpoint_suffix": ".cxwu08m2qypw.us-east-1.rds.amazonaws.com",
}

# Key RDS Instances by Category
RDS_INSTANCES = {
    "sales": [
        {"id": "aws-luckyus-salesorder-rw", "desc": "订单主库", "services": ["isales-order", "订单服务"]},
        {"id": "aws-luckyus-salespayment-rw", "desc": "支付主库", "services": ["salespayment", "支付服务"]},
        {"id": "aws-luckyus-salescrm-rw", "desc": "CRM主库", "services": ["isales-crm", "CRM服务"]},
        {"id": "aws-luckyus-salesmarketing-rw", "desc": "营销主库", "services": ["isales-market", "营销服务"]},
    ],
    "auth": [
        {"id": "aws-luckyus-iluckyauthapi-rw", "desc": "认证主库", "services": ["unionauth", "认证服务"]},
    ],
    "risk": [
        {"id": "aws-luckyus-iriskcontrolservice-rw", "desc": "风控主库", "services": ["iriskcontrol", "风控服务"]},
    ],
    "framework": [
        {"id": "aws-luckyus-framework01-rw", "desc": "框架库01", "services": ["framework", "基础框架"]},
        {"id": "aws-luckyus-framework02-rw", "desc": "框架库02", "services": ["framework", "基础框架"]},
    ],
    "scm": [
        {"id": "aws-luckyus-scm-ordering-rw", "desc": "供应链订货", "services": ["scm-ordering", "供应链"]},
        {"id": "aws-luckyus-scm-shopstock-rw", "desc": "门店库存", "services": ["scm-shopstock", "库存管理"]},
    ],
    "upush": [
        {"id": "aws-luckyus-upush-rw", "desc": "推送服务库", "services": ["upush", "消息推送"]},
    ],
}

# Key Redis Clusters
REDIS_CLUSTERS = {
    "sales": ["luckyus-isales-order", "luckyus-isales-session", "luckyus-isales-tradecapi"],
    "auth": ["luckyus-unionauth", "luckyus-auth", "luckyus-authservice", "luckyus-session"],
    "risk": ["luckyus-iriskcontrol"],
    "api": ["luckyus-apigateway", "luckyus-web"],
}

# VMAlert Configuration
VMALERT_CONFIG = {
    "apm_instances": [
        {"ip": "10.238.3.137", "port": "8880", "job": "us_izeus_apm_vm_alert"},
        {"ip": "10.238.3.143", "port": "8880", "job": "us_izeus_apm_vm_alert"},
        {"ip": "10.238.3.52", "port": "8880", "job": "us_izeus_apm_vm_alert"},
    ],
    "basic_instance": {"ip": "10.238.3.153", "port": "8880", "job": "us_izeus_basic_vm_alert"},
}

# Grafana Datasources
DATASOURCES = {
    "prometheus_mysql": {"uid": "ff7hkeec6c9a8e", "name": "prometheus", "desc": "MySQL指标"},
    "prometheus_redis": {"uid": "ff6p0gjt24phce", "name": "prometheus_redis", "desc": "Redis指标"},
    "prometheus_main": {"uid": "df8o21agxtkw0d", "name": "UMBQuerier-Luckin", "desc": "主Prometheus"},
    "elasticsearch": {"uid": "ff7ehok3sf56oa", "name": "elasticsearch", "desc": "日志搜索"},
}

# Alert Analysis Templates
ALERT_ANALYSIS = {
    # Database RDS Alerts
    "db-rds-cpu-90": {
        "meaning": "AWS RDS MySQL实例的CPU使用率连续3分钟超过90%，表明数据库负载过高。",
        "impact": """- **黄金流程影响**: 如果是salesorder-rw或salespayment-rw实例，将直接影响用户下单和支付
- **服务降级**: 数据库响应延迟增加，可能导致API超时
- **级联效应**: 连接池可能耗尽，导致其他服务无法获取数据库连接""",
        "affected_services": "订单服务、支付服务、会员服务、营销服务等依赖该数据库的所有微服务",
        "root_causes": """1. **慢查询累积**: 未优化的SQL语句导致全表扫描
2. **索引缺失**: 关键查询字段缺少索引
3. **连接数暴增**: 应用侧连接池配置不当或流量突增
4. **锁竞争**: 大事务或死锁导致资源等待
5. **实例规格不足**: 业务增长超出当前实例容量
6. **批量任务冲击**: 定时任务或数据同步任务在业务高峰期执行""",
        "promql": "aws_rds_cpuutilization_average offset 3m >= 90\navg_over_time(aws_rds_cpuutilization_average[3m]) >= 90",
    },
    "db-rds-vip-unreachable": {
        "meaning": "RDS VIP(虚拟IP)连续1分钟无法访问，表明数据库实例可能不可达。",
        "impact": """- **严重中断**: 依赖该数据库的所有服务将无法执行读写操作
- **黄金流程中断**: 如果是核心订单/支付库，用户将无法下单和支付
- **紧急程度**: P0级别，需要立即响应""",
        "affected_services": "所有依赖该RDS实例的微服务",
        "root_causes": """1. **网络问题**: VPC网络配置异常或安全组规则变更
2. **RDS故障**: 实例重启、主从切换进行中
3. **DNS解析失败**: 内部DNS服务异常
4. **监控探测异常**: mysql_exporter自身故障导致误报""",
        "promql": "min_over_time(mysql_check_vip{}[1m]) == 0",
    },
    "db-rds-failover-restart": {
        "meaning": "检测到RDS实例发生重启或主从切换，mysql_global_status_uptime计数器重置。",
        "impact": """- **短暂服务中断**: 切换期间(通常30秒-2分钟)数据库不可写
- **连接重置**: 所有现有数据库连接将被断开
- **事务回滚**: 切换时未完成的事务将被回滚""",
        "affected_services": "所有依赖该RDS实例的微服务需要重新建立连接",
        "root_causes": """1. **自动故障转移**: Multi-AZ实例主节点故障触发自动切换
2. **维护窗口**: AWS计划内维护导致的重启
3. **手动操作**: DBA执行的重启或切换操作
4. **资源耗尽**: 内存或存储空间耗尽导致实例重启""",
        "promql": "changes(mysql_global_status_uptime[5m]) > 0",
    },
    "db-rds-slow-queries-300": {
        "meaning": "RDS实例慢查询数量连续3分钟超过300个，表明存在大量执行缓慢的SQL。",
        "impact": """- **性能下降**: 服务响应时间明显增加
- **资源消耗**: CPU和IO资源被慢查询占用
- **用户体验**: 页面加载缓慢，可能出现超时""",
        "affected_services": "依赖该数据库的所有服务，特别是读取密集型服务",
        "root_causes": """1. **索引问题**: 查询字段缺少索引或索引失效
2. **数据量增长**: 表数据量增加导致查询变慢
3. **复杂查询**: 未优化的JOIN或子查询
4. **锁等待**: 大量事务等待锁释放
5. **参数配置**: slow_query_log阈值设置(long_query_time)""",
        "promql": "avg_over_time(mysql_global_status_slow_queries[3m]) > 300\nrate(mysql_global_status_slow_queries[3m]) * 180 > 300",
    },
    "db-rds-active-threads-24": {
        "meaning": "RDS实例活跃线程数连续2分钟超过24个，表明数据库并发压力过大。",
        "impact": """- **连接排队**: 新的数据库请求可能需要等待
- **响应延迟**: 服务端到端延迟增加
- **资源竞争**: CPU和内存资源竞争加剧""",
        "affected_services": "所有并发访问该数据库的服务",
        "root_causes": """1. **流量突增**: 促销活动或异常流量导致并发增加
2. **慢查询阻塞**: 长时间运行的查询占用线程
3. **锁等待**: 事务锁导致线程等待
4. **连接池泄露**: 应用连接未正确释放""",
        "promql": "avg_over_time(mysql_global_status_threads_running[2m]) > 24\nmin_over_time(mysql_global_status_threads_running[2m]) > 24",
    },
    "db-rds-disk-low-10g": {
        "meaning": "RDS实例可用磁盘空间连续3分钟低于10GB，存储空间即将耗尽。",
        "impact": """- **写入失败**: 空间耗尽后数据库将无法写入
- **服务中断**: 依赖写操作的服务将完全失败
- **数据完整性**: 事务可能无法完成""",
        "affected_services": "所有需要写入该数据库的服务",
        "root_causes": """1. **日志文件膨胀**: binlog或慢查询日志占用大量空间
2. **数据增长**: 业务数据自然增长
3. **大表操作**: DDL操作产生临时文件
4. **未清理历史数据**: 归档策略未执行""",
        "promql": "avg_over_time(aws_rds_freestoragespace_average[3m]) / 1024 / 1024 / 1024 < 10",
    },
    # Redis Alerts
    "db-redis-cpu-90": {
        "meaning": "AWS ElastiCache Redis实例CPU使用率达到90%以上。",
        "impact": """- **缓存延迟**: Redis命令响应时间增加
- **会话问题**: 依赖Redis存储会话的服务可能出现登录异常
- **限流失效**: 如果Redis用于限流，可能导致限流机制失效""",
        "affected_services": "会话管理、缓存服务、限流服务、消息队列等",
        "root_causes": """1. **热点Key**: 某个Key访问过于频繁
2. **大Key操作**: 对大List/Set/Hash的操作
3. **Lua脚本**: 复杂Lua脚本消耗CPU
4. **持久化**: RDB/AOF持久化过程中的CPU消耗
5. **实例规格不足**: 需要升级实例""",
        "promql": "aws_elasticache_cpuutilization_average >= 90",
    },
    "db-redis-memory-70": {
        "meaning": "Redis实例内存使用率连续3分钟超过70%，接近内存上限。",
        "impact": """- **Key淘汰**: 可能触发maxmemory-policy策略淘汰Key
- **OOM风险**: 继续增长可能导致Redis OOM
- **写入失败**: 达到上限后新写入可能失败""",
        "affected_services": "所有使用该Redis实例的缓存服务",
        "root_causes": """1. **数据未过期**: TTL设置不当导致数据累积
2. **大Key**: 存在占用大量内存的Key
3. **业务增长**: 缓存数据量自然增长
4. **内存碎片**: Redis内存碎片率过高""",
        "promql": "avg_over_time(aws_elasticache_database_memory_usage_percentage_average[3m]) > 70",
    },
    "db-redis-client-blocked": {
        "meaning": "检测到Redis有客户端处于阻塞状态，通常由BLPOP/BRPOP等阻塞命令引起。",
        "impact": """- **连接占用**: 阻塞连接占用连接池资源
- **潜在死锁**: 可能导致业务逻辑等待""",
        "affected_services": "使用阻塞命令的消息队列类服务",
        "root_causes": """1. **消息队列空**: 阻塞等待消息的客户端
2. **生产者故障**: 消息生产者停止发送消息
3. **超时设置**: 阻塞命令超时时间设置过长""",
        "promql": "redis_blocked_clients > 0",
    },
    "db-redis-key-eviction": {
        "meaning": "Redis触发了Key淘汰机制，表明内存已达到maxmemory限制。",
        "impact": """- **缓存穿透**: 被淘汰的热点Key可能导致大量请求打到数据库
- **数据丢失**: 重要缓存数据被淘汰
- **业务异常**: 依赖缓存数据的业务逻辑异常""",
        "affected_services": "所有依赖缓存数据的服务",
        "root_causes": """1. **内存不足**: 实例内存配置不足
2. **数据膨胀**: 缓存数据量超出预期
3. **TTL问题**: 未设置合理的过期时间
4. **maxmemory-policy**: 淘汰策略配置""",
        "promql": "increase(redis_evicted_keys_total[1m]) > 0",
    },
    # Pod/Container Alerts
    "pod-cpu-fallback-85": {
        "meaning": "Pod CPU使用率连续3分钟超过资源限制的85%，这是一个兜底告警。",
        "impact": """- **服务限流**: 接近CPU限制，可能被K8s节流
- **响应延迟**: 服务处理能力下降
- **Pod重启风险**: 持续高负载可能触发OOM Killer""",
        "affected_services": "告警中指定的Pod所属服务",
        "root_causes": """1. **代码问题**: 存在CPU密集型逻辑或死循环
2. **流量突增**: 业务流量超出预期
3. **资源配置不当**: CPU limit设置过低
4. **GC问题**: JVM频繁GC消耗CPU""",
        "promql": """avg_over_time(
  (sum(rate(container_cpu_usage_seconds_total{container!="POD",container!=""}[1m])) by (pod,namespace)
  /
  sum(kube_pod_container_resource_limits{resource="cpu"}) by (pod,namespace) * 100)[3m:]
) > 85""",
    },
    "pod-restart-2min": {
        "meaning": "Pod在最近2分钟内发生了重启，可能是异常退出或健康检查失败。",
        "impact": """- **服务中断**: 重启期间服务不可用
- **请求失败**: 正在处理的请求将失败
- **流量切换**: K8s会将流量切走，可能造成其他Pod压力增加""",
        "affected_services": "重启的Pod所属服务及其依赖服务",
        "root_causes": """1. **OOM Kill**: 内存超限被系统杀死
2. **健康检查失败**: Liveness Probe失败
3. **应用崩溃**: 未捕获异常导致进程退出
4. **资源不足**: 节点资源不足触发驱逐""",
        "promql": "increase(kube_pod_container_status_restarts_total[2m]) > 0",
    },
    "pod-memory-oom": {
        "meaning": "Pod WSS(Working Set Size)内存使用率连续3分钟达到100%，即将或已经OOM。",
        "impact": """- **服务崩溃**: OOM会导致Pod被杀死
- **数据丢失**: 内存中未持久化的数据将丢失
- **级联影响**: 可能导致依赖服务调用失败""",
        "affected_services": "OOM的Pod所属服务",
        "root_causes": """1. **内存泄漏**: 代码存在内存泄漏
2. **JVM配置**: 堆大小超出容器限制
3. **大对象**: 处理大文件或大数据集
4. **缓存过大**: 本地缓存未设置上限""",
        "promql": """avg_over_time(
  (container_memory_working_set_bytes{container!="POD",container!=""}
  /
  kube_pod_container_resource_limits{resource="memory"} * 100)[3m:]
) >= 100""",
    },
    # VM/Host Alerts
    "vm-cpu-80": {
        "meaning": "VM主机整体CPU平均使用率超过80%，服务器负载过高。",
        "impact": """- **性能下降**: 所有运行在该主机上的服务性能下降
- **调度影响**: K8s可能无法在该节点调度新Pod""",
        "affected_services": "运行在该主机上的所有服务和Pod",
        "root_causes": """1. **负载不均**: Pod分布不均匀
2. **资源争抢**: 多个高负载Pod同时运行
3. **系统进程**: 系统级进程占用过多CPU
4. **节点容量**: 节点资源规划不足""",
        "promql": "100 - (avg by(instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[1m])) * 100) > 80",
    },
    "vm-disk-90": {
        "meaning": "VM主机磁盘分区使用率超过90%，存储空间紧张。",
        "impact": """- **服务异常**: 日志写入失败，服务可能崩溃
- **数据丢失**: 新数据无法写入""",
        "affected_services": "运行在该主机上的所有服务",
        "root_causes": """1. **日志堆积**: 应用日志未及时清理
2. **容器镜像**: 过多的容器镜像占用空间
3. **临时文件**: 临时文件未清理
4. **数据增长**: 应用数据文件增长""",
        "promql": "(1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 > 90",
    },
    # Business Alerts
    "business-orders-low": {
        "meaning": "新建-付款-完成订单链路持续10分钟少于1单，核心交易链路可能中断。",
        "impact": """- **黄金流程中断**: 这是最严重的业务告警
- **收入损失**: 直接影响业务营收
- **用户体验**: 用户无法正常下单购买""",
        "affected_services": "订单服务、支付服务、商品服务、库存服务、会员服务",
        "root_causes": """1. **订单服务故障**: isales-order服务异常
2. **支付服务故障**: salespayment服务异常
3. **数据库故障**: salesorder-rw或salespayment-rw数据库异常
4. **Redis故障**: isales-order或session Redis故障
5. **上游依赖**: 认证服务、商品服务等上游服务异常
6. **外部支付通道**: 支付渠道(如Stripe)异常""",
        "promql": "sum_over_time(business_completed_orders_total[10m]) < 1",
    },
    "business-registrations-zero": {
        "meaning": "过去10分钟新用户注册数为0，用户获取链路可能中断。",
        "impact": """- **用户增长停滞**: 无法获取新用户
- **营销失效**: 推广活动无法转化""",
        "affected_services": "会员服务、认证服务、短信服务",
        "root_causes": """1. **认证服务故障**: unionauth服务异常
2. **短信服务故障**: 验证码无法发送
3. **App故障**: 客户端注册页面异常
4. **Redis故障**: session Redis异常""",
        "promql": "sum_over_time(business_registration_count[10m]) == 0",
    },
    # Risk Control Alerts
    "risk-circuit-breaker": {
        "meaning": "风控系统全局熔断器触发，所有风控策略将暂停执行。",
        "impact": """- **风险敞口**: 风控失效可能导致欺诈交易通过
- **业务保护**: 熔断可能是保护系统的措施
- **需要评估**: 需要判断是策略问题还是系统问题""",
        "affected_services": "所有需要风控校验的服务(下单、支付、注册、登录)",
        "root_causes": """1. **风控服务故障**: iriskcontrol服务异常
2. **规则引擎故障**: 风控规则执行失败
3. **上游依赖**: 风控依赖的数据服务异常
4. **阈值误触发**: 风控阈值设置过于敏感""",
        "promql": "risk_control_global_circuit_breaker_triggered == 1",
    },
    # Gateway Alerts
    "gateway-error-rate": {
        "meaning": "API网关错误率超过15%，大量请求返回5xx错误。",
        "impact": """- **服务降级**: 大量用户请求失败
- **用户体验**: App功能不可用
- **级联故障**: 可能是后端服务问题的表现""",
        "affected_services": "通过网关的所有API服务",
        "root_causes": """1. **后端服务故障**: 上游服务不可用
2. **网关配置**: 路由配置错误
3. **容量问题**: 网关实例资源不足
4. **网络问题**: 网关到后端服务网络异常""",
        "promql": "(sum(rate(gateway_requests_total{status=~\"5..\"}[1m])) / sum(rate(gateway_requests_total[1m]))) * 100 > 15",
    },
    # SMS/UPUSH Alerts
    "upush-sms-failures": {
        "meaning": "五分钟内短信供应商调用失败次数超过阈值，短信发送可能受影响。",
        "impact": """- **验证码发送**: 用户无法收到验证码
- **营销短信**: 营销活动短信无法发送
- **通知服务**: 系统通知无法送达""",
        "affected_services": "短信服务、验证码服务、营销服务",
        "root_causes": """1. **供应商故障**: 短信供应商服务异常
2. **API限流**: 超过供应商API调用限制
3. **配置问题**: API密钥或配置错误
4. **网络问题**: 到供应商网络不通""",
        "promql": "sum_over_time(sms_provider_call_failures_total[5m]) > 50",
    },
    # Slow Query Grafana Alerts
    "slow-query-spike": {
        "meaning": "Grafana原生告警: MySQL慢查询速率5分钟内超过阈值(>1或>2/秒)。",
        "impact": """- **数据库性能**: 慢查询累积影响整体数据库性能
- **服务延迟**: 依赖数据库的服务响应变慢
- **资源消耗**: CPU和IO资源被大量消耗""",
        "affected_services": "所有依赖MySQL的服务",
        "root_causes": """1. **索引缺失**: 查询未命中索引
2. **表锁竞争**: InnoDB行锁或表锁等待
3. **复杂查询**: JOIN过多或子查询嵌套
4. **数据量增长**: 表数据量增长导致查询变慢""",
        "promql": "sum(rate(mysql_global_status_slow_queries[5m])) by (instance) > 1",
    },
}

# Access Instructions Template
ACCESS_INSTRUCTIONS = """
## 系统访问方式

### AWS控制台访问

**AWS账号信息:**
- **Account ID**: 257394478466
- **Region**: us-east-1 (美东)
- **控制台URL**: https://257394478466.signin.aws.amazon.com/console

### AWS CLI访问

**配置AWS CLI:**
```bash
# 确认当前AWS身份
aws sts get-caller-identity

# 确认区域配置
aws configure get region
# 应返回: us-east-1
```

### 数据库访问

**RDS MySQL连接方式:**

1. **通过JumpServer跳板机** (推荐):
   - JumpServer地址: 联系DBA团队获取
   - 使用SSH隧道或Web终端连接

2. **通过MySQL客户端**:
```bash
# 连接示例 (需要在内网或VPN环境)
mysql -h <RDS_ENDPOINT> -u <USERNAME> -p

# 常用RDS端点:
# 订单库: aws-luckyus-salesorder-rw.cxwu08m2qypw.us-east-1.rds.amazonaws.com
# 支付库: aws-luckyus-salespayment-rw.cxwu08m2qypw.us-east-1.rds.amazonaws.com
# 风控库: aws-luckyus-iriskcontrolservice-rw.cxwu08m2qypw.us-east-1.rds.amazonaws.com
```

### Redis访问

**ElastiCache Redis连接方式:**

```bash
# 通过redis-cli连接 (需要在内网)
redis-cli -h <REDIS_ENDPOINT> -p 6379

# 常用Redis集群:
# 订单缓存: luckyus-isales-order.xxxxx.use1.cache.amazonaws.com
# 会话缓存: luckyus-session.xxxxx.use1.cache.amazonaws.com
# 认证缓存: luckyus-unionauth.xxxxx.use1.cache.amazonaws.com
```

### Kubernetes访问

**EKS集群访问:**
```bash
# 更新kubeconfig
aws eks update-kubeconfig --name <CLUSTER_NAME> --region us-east-1

# 查看Pod状态
kubectl get pods -n <NAMESPACE>

# 查看Pod日志
kubectl logs -f <POD_NAME> -n <NAMESPACE>
```

### 监控系统访问

**Grafana:**
- 地址: 联系DevOps团队获取Grafana URL
- 主要Datasource UID:
  - MySQL指标: ff7hkeec6c9a8e
  - Redis指标: ff6p0gjt24phce
  - 主Prometheus: df8o21agxtkw0d

**VMAlert配置:**
- APM实例: 10.238.3.137:8880, 10.238.3.143:8880, 10.238.3.52:8880
- Basic实例: 10.238.3.153:8880
- 配置文件: `/etc/rules/alert_rules.json`
"""


def get_alert_type(filename):
    """Extract alert type from filename."""
    name = filename.stem.lower()

    # Map filename patterns to alert types
    mappings = [
        ("db-rds-cpu-90", "db-rds-cpu-90"),
        ("db-rds-vip-unreachable", "db-rds-vip-unreachable"),
        ("db-rds-failover-restart", "db-rds-failover-restart"),
        ("db-rds-slow-queries", "db-rds-slow-queries-300"),
        ("db-rds-active-threads", "db-rds-active-threads-24"),
        ("db-rds-disk", "db-rds-disk-low-10g"),
        ("db-redis-cpu-90", "db-redis-cpu-90"),
        ("db-redis-cpu-70", "db-redis-cpu-90"),
        ("db-redis-memory", "db-redis-memory-70"),
        ("db-redis-client-blocked", "db-redis-client-blocked"),
        ("db-redis-key-eviction", "db-redis-key-eviction"),
        ("db-redis-latency", "db-redis-client-blocked"),
        ("db-redis-buffer", "db-redis-memory-70"),
        ("db-redis-traffic", "db-redis-cpu-90"),
        ("db-redis-connections", "db-redis-memory-70"),
        ("db-redis-collection", "db-redis-client-blocked"),
        ("db-mongo", "db-rds-cpu-90"),
        ("db-es-cpu", "db-rds-cpu-90"),
        ("db-es-cluster", "db-rds-vip-unreachable"),
        ("db-es-disk", "db-rds-disk-low-10g"),
        ("db-exporter", "db-redis-client-blocked"),
        ("pod-cpu-fallback", "pod-cpu-fallback-85"),
        ("pod-cpu-50", "pod-cpu-fallback-85"),
        ("pod-cpu-70", "pod-cpu-fallback-85"),
        ("pod-restart", "pod-restart-2min"),
        ("pod-memory", "pod-memory-oom"),
        ("pod-node-heartbeat", "pod-restart-2min"),
        ("pod-threads", "pod-cpu-fallback-85"),
        ("pod-io", "pod-cpu-fallback-85"),
        ("pod-network", "pod-cpu-fallback-85"),
        ("vm-cpu", "vm-cpu-80"),
        ("vm-disk", "vm-disk-90"),
        ("vm-memory", "vm-cpu-80"),
        ("vm-filesystem", "vm-disk-90"),
        ("vm-io", "vm-disk-90"),
        ("vm-tcp", "vm-cpu-80"),
        ("vm-network", "vm-cpu-80"),
        ("business-cancelled", "business-orders-low"),
        ("business-completed", "business-orders-low"),
        ("business-order", "business-orders-low"),
        ("business-registration", "business-registrations-zero"),
        ("business-payment", "business-orders-low"),
        ("risk-global-circuit", "risk-circuit-breaker"),
        ("risk-scene-circuit", "risk-circuit-breaker"),
        ("risk-rpc", "risk-circuit-breaker"),
        ("upush-sms-provider", "upush-sms-failures"),
        ("upush-sms-return", "upush-sms-failures"),
        ("upush-marketing", "upush-sms-failures"),
        ("upush-industry", "upush-sms-failures"),
        ("upush-verification", "upush-sms-failures"),
        ("izeus-strategy", "pod-cpu-fallback-85"),
        ("izeus-node", "vm-cpu-80"),
        ("izeus-oap", "pod-cpu-fallback-85"),
        ("izeus-storage", "pod-restart-2min"),
        ("izeus-transfer", "pod-restart-2min"),
        ("default-jvm", "pod-cpu-fallback-85"),
        ("default-okhttp", "pod-cpu-fallback-85"),
        ("default-exceptions", "pod-cpu-fallback-85"),
        ("datalink", "business-orders-low"),
        ("gateway-error", "gateway-error-rate"),
        ("network", "vm-cpu-80"),
        ("slow-query-spike", "slow-query-spike"),
        ("slow-query-critical", "slow-query-spike"),
        ("slow-query-weekly", "slow-query-spike"),
        ("lcp-prod", "business-orders-low"),
    ]

    for pattern, alert_type in mappings:
        if pattern in name:
            return alert_type

    return "pod-cpu-fallback-85"  # Default fallback


def generate_alert_analysis_section(alert_type):
    """Generate the alert analysis section content."""
    analysis = ALERT_ANALYSIS.get(alert_type, ALERT_ANALYSIS["pod-cpu-fallback-85"])

    section = f"""
## 告警解析

### 告警含义

{analysis['meaning']}

### 业务影响

{analysis['impact']}

### 受影响服务

{analysis['affected_services']}

### PromQL表达式

```promql
{analysis['promql']}
```

### 常见根因

{analysis['root_causes']}

---
"""
    return section


def enhance_diagnostic_commands(content, alert_type):
    """Enhance the diagnostic commands section with specific access info."""
    # Find where to insert the access information
    if "## 诊断命令" in content:
        # Add access instructions before diagnostic commands
        enhanced_content = content.replace(
            "## 诊断命令",
            ACCESS_INSTRUCTIONS + "\n---\n\n## 诊断命令"
        )
        return enhanced_content
    return content


def add_rds_specific_commands(content, alert_type):
    """Add RDS-specific diagnostic commands for database alerts."""
    if "db-rds" not in alert_type and "db-redis" not in alert_type:
        return content

    rds_commands = """
### 实时数据库诊断

**关键RDS实例列表:**
```
aws-luckyus-salesorder-rw     - 订单主库 (L0核心)
aws-luckyus-salespayment-rw   - 支付主库 (L0核心)
aws-luckyus-iriskcontrolservice-rw - 风控主库
aws-luckyus-framework01-rw    - 框架库01
aws-luckyus-framework02-rw    - 框架库02
```

**查看所有RDS实例状态:**
```bash
aws rds describe-db-instances \\
  --query 'DBInstances[?starts_with(DBInstanceIdentifier, `aws-luckyus`)].{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Class:DBInstanceClass,CPU:toString(EngineVersion)}' \\
  --output table
```

**查看特定实例的CPU指标:**
```bash
# 替换 INSTANCE_ID 为实际的实例ID
aws cloudwatch get-metric-statistics \\
  --namespace AWS/RDS \\
  --metric-name CPUUtilization \\
  --dimensions Name=DBInstanceIdentifier,Value=aws-luckyus-salesorder-rw \\
  --start-time $(date -u -d '30 minutes ago' +%Y-%m-%dT%H:%M:%SZ) \\
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \\
  --period 60 \\
  --statistics Average Maximum
```

**查看数据库连接数:**
```bash
aws cloudwatch get-metric-statistics \\
  --namespace AWS/RDS \\
  --metric-name DatabaseConnections \\
  --dimensions Name=DBInstanceIdentifier,Value=aws-luckyus-salesorder-rw \\
  --start-time $(date -u -d '30 minutes ago' +%Y-%m-%dT%H:%M:%SZ) \\
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \\
  --period 60 \\
  --statistics Average Maximum
```
"""

    # Insert after the diagnostic commands header
    if "## 诊断命令" in content:
        parts = content.split("## 诊断命令")
        if len(parts) >= 2:
            # Find the end of the diagnostic section (next ##)
            rest = parts[1]
            next_section = rest.find("\n## ")
            if next_section > 0:
                content = parts[0] + "## 诊断命令" + rest[:next_section] + rds_commands + rest[next_section:]
            else:
                content = parts[0] + "## 诊断命令" + rest + rds_commands

    return content


def enhance_root_causes(content, alert_type):
    """Enhance root cause section with more specific information."""
    analysis = ALERT_ANALYSIS.get(alert_type, ALERT_ANALYSIS["pod-cpu-fallback-85"])

    # Find and enhance the root cause section
    if "### 常见原因" in content:
        # Add more specific root causes
        enhanced_causes = f"""### 常见原因

{analysis['root_causes']}

#### Luckin系统特定原因

根据系统架构，以下是可能的特定原因:

1. **核心服务影响**: 检查salesorder-rw、salespayment-rw等核心数据库
2. **缓存层问题**: 检查luckyus-isales-order、luckyus-session等Redis集群
3. **认证链路**: 检查unionauth相关服务和Redis
4. **风控链路**: 检查iriskcontrol服务状态
"""

        # Replace the section
        pattern = r'### 常见原因\n\n.*?(?=\n### |\n## |\n---|\Z)'
        content = re.sub(pattern, enhanced_causes, content, flags=re.DOTALL)

    return content


def enhance_handbook(filepath):
    """Enhance a single handbook file with all improvements."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    alert_type = get_alert_type(filepath)

    # 1. Add alert analysis section after 告警描述
    if "## 告警解析" not in content:
        analysis_section = generate_alert_analysis_section(alert_type)

        # Insert after 告警描述 section
        if "## 告警描述" in content:
            parts = content.split("## 告警描述")
            if len(parts) >= 2:
                # Find the next section
                rest = parts[1]
                next_section = rest.find("\n## ")
                if next_section > 0:
                    content = parts[0] + "## 告警描述" + rest[:next_section] + analysis_section + rest[next_section:]
                else:
                    content = parts[0] + "## 告警描述" + rest + analysis_section
        elif "## 立即响应" in content:
            # Insert before 立即响应 if 告警描述 not found
            content = content.replace("## 立即响应", analysis_section + "## 立即响应")

    # 2. Enhance diagnostic commands with access info
    content = enhance_diagnostic_commands(content, alert_type)

    # 3. Add RDS-specific commands for database alerts
    content = add_rds_specific_commands(content, alert_type)

    # 4. Enhance root causes
    content = enhance_root_causes(content, alert_type)

    # Clean up formatting
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    content = content.rstrip() + '\n'

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    handbook_dir = Path("/app/luckin-alerts-repo/alert-handbooks")
    modified_count = 0

    print("=" * 60)
    print("Luckin Coffee USA - Enhanced Runbook Generator")
    print("=" * 60)
    print(f"\nAWS Account: {AWS_CONFIG['account_id']}")
    print(f"Region: {AWS_CONFIG['region']}")
    print(f"RDS Instances: {len([db for cat in RDS_INSTANCES.values() for db in cat])}")
    print(f"Redis Clusters: {len([r for cat in REDIS_CLUSTERS.values() for r in cat])}")
    print("\n" + "-" * 60)
    print("Processing handbooks...")
    print("-" * 60 + "\n")

    for filepath in sorted(handbook_dir.glob("ALR-*.md")):
        try:
            if enhance_handbook(filepath):
                print(f"✓ Enhanced: {filepath.name}")
                modified_count += 1
            else:
                print(f"- Skipped (no changes): {filepath.name}")
        except Exception as e:
            print(f"✗ Error processing {filepath.name}: {e}")

    print("\n" + "-" * 60)
    print(f"Summary: Enhanced {modified_count} files")
    print("-" * 60)


if __name__ == "__main__":
    main()
