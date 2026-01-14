# 【DB告警】AWS Redis CPU使用率大于90%

> **Luckin Coffee USA - DevOps/DBA Alert Response Handbook**
> **瑞幸咖啡美国 - 运维/DBA告警响应手册**

---

## 告警概览 Alert Overview

| 属性 Attribute | 值 Value |
|----------------|----------|
| **Alert ID** | ALR-040 |
| **告警名称 Alert Name** | 【DB告警】AWS Redis CPU使用率大于90% |
| **优先级 Priority** | P1 |
| **服务等级 Service Level** | L0 - Core Business Service (核心业务服务) |
| **类别 Category** | Database-Redis |
| **系统 System** | VMAlert |
| **指标类型 Metric Type** | CPU |
| **阈值/条件 Threshold** | >90% |
| **持续时间 Duration** | Instant |
| **响应时间 Response Time** | HIGH (< 15 minutes) |
| **责任团队 Owner Team** | StoragePlatform - Storage (存储平台) |

---

## 告警描述 Description

### 中文说明
此告警在 **>90%** 条件满足时触发。该告警属于 **P1** 优先级，影响 **L0** 级别服务。

**触发条件:** CPU 指标达到阈值 >90%，持续时间: Instant

**重要性:** 此告警关联 存储平台 团队负责的 Redis Cloud, LDAS 领域服务，需要在 < 15 minutes 内响应处理。

### English Description
This alert triggers when the condition **>90%** is met. This is a **P1** priority alert affecting **L0** level services.

**Trigger Condition:** CPU metric reaches threshold >90%, duration: Instant

**Importance:** This alert is associated with the Storage team's Redis Cloud, LDAS domain services and requires response within < 15 minutes.

---

## 影响范围 Impact Scope

### 关联服务 Affected Services

| 服务名称 Service | 等级 Level | 描述 Description | 团队 Team |
|-----------------|------------|------------------|-----------|
| luckyozono | L1 | 缓存云平台 Redis Cloud | StoragePlatform |
| isalesorderservice | L0 | 订单服务 Order Service (缓存) | Sales |
| isalesmarketingservice | L0 | 营销服务 Marketing Service (缓存) | Sales |

### 关联数据库 Affected Databases

- `luckyus_ozono (ElastiCache Redis)`

### 业务影响 Business Impact

**P1 - L0 级别告警的业务影响:**

- **严重程度: 关键** - 可能导致核心业务中断
- 直接影响订单、支付、会员等核心业务流程
- 可能造成直接收入损失
- 需要立即响应和处理

**Severity: CRITICAL** - May cause core business interruption
- Directly affects orders, payments, CRM core business processes
- May cause direct revenue loss
- Requires immediate response and handling

---

## 立即响应 Immediate Actions

### 第一步: 确认告警 Step 1: Acknowledge Alert
```
1. 在监控系统中确认告警 / Acknowledge alert in monitoring system
2. 记录告警时间和详情 / Record alert time and details
3. 通知相关团队成员 / Notify relevant team members
```

### 第二步: 初步评估 Step 2: Initial Assessment
```
1. 立即检查相关服务状态 / Immediately check related service status
2. 评估业务影响范围 / Assess business impact scope
3. 如有必要，启动应急响应流程 / Initiate emergency response if necessary
4. 通知值班经理 / Notify on-call manager
```

### 第三步: 收集信息 Step 3: Gather Information
```
1. 检查告警详细信息 / Check alert details
2. 查看相关Grafana仪表板 / View related Grafana dashboards
3. 收集诊断信息 / Gather diagnostic information
4. 检查最近变更记录 / Check recent change records
```

---

## 诊断命令 Diagnostic Commands

```bash
# 检查ElastiCache集群状态 Check ElastiCache cluster status
aws elasticache describe-cache-clusters \
  --query 'CacheClusters[?starts_with(CacheClusterId, `luckyus`)].{ID:CacheClusterId,Status:CacheClusterStatus}'

# 检查Redis内存信息 Check Redis memory info
redis-cli -h [REDIS_ENDPOINT] INFO memory

# 检查Redis慢日志 Check Redis slow log
redis-cli -h [REDIS_ENDPOINT] SLOWLOG GET 10

# 检查客户端连接 Check client connections
redis-cli -h [REDIS_ENDPOINT] CLIENT LIST
redis-cli -h [REDIS_ENDPOINT] INFO clients

# 检查键空间统计 Check keyspace statistics
redis-cli -h [REDIS_ENDPOINT] INFO keyspace

# 内存诊断 Memory diagnosis
redis-cli -h [REDIS_ENDPOINT] MEMORY DOCTOR
```

---

## 根因分析 Root Cause Analysis

### 常见原因 Common Causes

1. 执行高复杂度命令(KEYS, SORT等) / Executing high-complexity commands (KEYS, SORT, etc.)
2. 大量并发连接处理 / High concurrent connection handling
3. Lua脚本执行时间过长 / Lua script execution taking too long
4. 数据序列化/反序列化开销 / Data serialization/deserialization overhead
5. 单线程模型处理瓶颈 / Single-threaded model processing bottleneck

### 排查清单 Investigation Checklist

- [ ] 确认告警触发时间和频率 / Confirm alert trigger time and frequency
- [ ] 检查相关服务健康状态 / Check related service health status
- [ ] 验证数据库连接和性能 / Verify database connectivity and performance
- [ ] 检查最近的部署或配置变更 / Check recent deployments or configuration changes
- [ ] 分析相关日志是否有异常 / Analyze related logs for anomalies
- [ ] 检查依赖服务状态 / Check dependent service status
- [ ] 验证网络连接和延迟 / Verify network connectivity and latency
- [ ] 检查资源使用情况(CPU/内存/磁盘) / Check resource usage (CPU/Memory/Disk)

---

## 处理步骤 Resolution Steps

### 通用排查流程 / General Troubleshooting

**步骤 1:** 确认告警详情和影响范围 / Confirm alert details and impact scope

**步骤 2:** 检查相关服务和依赖状态 / Check related services and dependency status

**步骤 3:** 查看最近的变更记录 / Review recent change records

**步骤 4:** 分析相关日志和指标 / Analyze related logs and metrics

**步骤 5:** 根据根因实施修复措施 / Implement fix based on root cause


---

## 升级标准 Escalation Criteria

### 升级条件 When to Escalate

| 条件 Condition | 时间要求 Time Requirement | 升级目标 Escalation Target |
|---------------|--------------------------|---------------------------|
| 初次响应无法解决 / Initial response cannot resolve | 5分钟内 | L2 Support |
| 问题持续恶化 / Issue continues to worsen | +10分钟 / +10 minutes | Team Lead |
| 影响扩大到其他服务 / Impact spreads to other services | 立即 / Immediately | SRE On-Call |
| 需要外部支持 / External support needed | 根据情况 / As needed | Vendor/AWS Support |

### 升级联系方式 Escalation Contacts

| 角色 Role | 联系方式 Contact |
|-----------|-----------------|
| **主要负责团队 Primary Team** | Storage (存储平台) |
| **On-Call** | storage-oncall@luckin.com |
| **Slack Channel** | #storage-alerts |
| **升级邮件 Escalation Email** | escalation@luckin.com |
| **紧急热线 Emergency Hotline** | +1-XXX-XXX-XXXX |

### 升级时需提供信息 Information Required for Escalation

```
1. 告警名称和ID / Alert name and ID: 【DB告警】AWS Redis CPU使用率大于90% (ALR-040)
2. 告警触发时间 / Alert trigger time
3. 当前状态 / Current status
4. 已采取的措施 / Actions taken
5. 影响范围评估 / Impact assessment
6. 相关日志和指标截图 / Related logs and metric screenshots
7. 诊断命令输出 / Diagnostic command output
```

---

## 预防措施 Prevention Measures

- 设置合理的内存淘汰策略 / Set appropriate memory eviction policy
- 定期清理过期键 / Regularly clean expired keys
- 监控大键并进行优化 / Monitor and optimize large keys
- 实施Redis集群高可用架构 / Implement Redis cluster high availability
- 配置合理的连接池参数 / Configure appropriate connection pool parameters

---

## 相关告警 Related Alerts

以下告警经常与此告警同时出现或有关联关系:

The following alerts often appear together or are related to this alert:

- `【DB告警】AWS Redis CPU使用率大于90%`
- `【DB告警】Redis 内存使用率持续3分钟超过70%`
- `【DB告警】Redis 发生客户端堵塞`
- `【DB告警】Redis 实例采集失败请检查是否存活`
- `【DB告警】Redis 实例触发key淘汰`

---

## Grafana 仪表板参考 Grafana Dashboard Reference

| 仪表板 Dashboard | 用途 Purpose | 关联告警类型 Related Alert Types |
|-----------------|--------------|--------------------------------|
| RDS MySQL Overview | 数据库性能监控 | Database-RDS |
| ElastiCache Redis | 缓存性能监控 | Database-Redis |
| Kubernetes Pods | 容器监控 | Pod |
| Node Exporter | VM/主机监控 | VM |
| iZeus APM | 应用性能监控 | APM-iZeus |
| DataLink Pipeline | ETL任务监控 | DataLink |
| Business Metrics | 业务指标监控 | Business |
| Risk Control | 风控监控 | Risk Control |
| API Gateway | 网关监控 | Gateway |

---

## 文档信息 Document Information

| 属性 Attribute | 值 Value |
|----------------|----------|
| **版本 Version** | 1.0 |
| **创建日期 Created** | 2026-01-14 |
| **最后更新 Last Updated** | 2026-01-14 |
| **文档负责人 Owner** | DevOps Team |
| **审核状态 Review Status** | Approved |

---

## 修订历史 Revision History

| 版本 Version | 日期 Date | 作者 Author | 变更说明 Changes |
|-------------|-----------|-------------|-----------------|
| 1.0 | 2026-01-14 | DevOps Team | 初始版本 Initial version |

---

> **备注 Note:** 本手册为标准操作程序(SOP)文档，请根据实际情况灵活处理。如有疑问，请联系相关团队负责人。
>
> This handbook is a Standard Operating Procedure (SOP) document. Please handle flexibly according to actual situations. If you have any questions, please contact the relevant team leader.
