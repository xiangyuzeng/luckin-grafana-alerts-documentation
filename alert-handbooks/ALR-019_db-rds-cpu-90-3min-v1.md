# 【DB告警】AWS-RDS CPU使用率连续三分钟大于90%

> **Luckin Coffee USA - DevOps/DBA Alert Response Handbook**
> **瑞幸咖啡美国 - 运维/DBA告警响应手册**

---

## 告警概览 Alert Overview

| 属性 Attribute | 值 Value |
|----------------|----------|
| **Alert ID** | ALR-019 |
| **告警名称 Alert Name** | 【DB告警】AWS-RDS CPU使用率连续三分钟大于90% |
| **优先级 Priority** | P1 |
| **服务等级 Service Level** | L0 - Core Business Service (核心业务服务) |
| **类别 Category** | Database-RDS |
| **系统 System** | VMAlert |
| **指标类型 Metric Type** | CPU |
| **阈值/条件 Threshold** | >90% for 3min |
| **持续时间 Duration** | 3m |
| **响应时间 Response Time** | HIGH (< 15 minutes) |
| **责任团队 Owner Team** | DBA - DBA (数据库管理) |

---

## 告警描述 Description

### 中文说明
此告警在 **>90% for 3min** 条件满足时触发。该告警属于 **P1** 优先级，影响 **L0** 级别服务。

**触发条件:** CPU 指标达到阈值 >90% for 3min，持续时间: 3m

**重要性:** 此告警关联 数据库管理 团队负责的 All Databases 领域服务，需要在 < 15 minutes 内响应处理。

### English Description
This alert triggers when the condition **>90% for 3min** is met. This is a **P1** priority alert affecting **L0** level services.

**Trigger Condition:** CPU metric reaches threshold >90% for 3min, duration: 3m

**Importance:** This alert is associated with the DBA team's All Databases domain services and requires response within < 15 minutes.

---

## 影响范围 Impact Scope

### 关联服务 Affected Services

| 服务名称 Service | 等级 Level | 描述 Description | 团队 Team |
|-----------------|------------|------------------|-----------|
| isalesorderservice | L0 | 订单服务 Order Service | Sales |
| isalespaymentservice | L0 | 支付服务 Payment Service | Sales |
| isalescrmservice | L0 | 会员服务 CRM Service | Sales |
| iopshopservice | L0 | 门店服务 Shop Service | EEOP |
| luckynacos | L1 | 注册中心 Service Registry | MicroService |
| luckyapigateway | L1 | API网关 API Gateway | MicroService |

### 关联数据库 Affected Databases

- `luckyus_sales_order`
- `luckyus_sales_payment`
- `luckyus_sales_crm`
- `luckyus_opshop`
- `luckyus_nacos`

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
# 检查RDS实例状态 Check RDS instance status
aws rds describe-db-instances \
  --query 'DBInstances[?starts_with(DBInstanceIdentifier, `luckyus`)].{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Class:DBInstanceClass}'

# 检查RDS性能指标 Check RDS performance metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=[INSTANCE_ID] \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average Maximum

# 检查慢查询 Check slow queries
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW PROCESSLIST;"
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW FULL PROCESSLIST;"

# 检查InnoDB状态 Check InnoDB status
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW ENGINE INNODB STATUS\G"

# 检查连接数 Check connections
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW STATUS LIKE 'Threads%';"
```

---

## 根因分析 Root Cause Analysis

### 常见原因 Common Causes

1. 复杂或未优化的SQL查询消耗过多CPU / Complex or unoptimized SQL queries consuming excessive CPU
2. 缺少索引导致全表扫描 / Missing indexes causing full table scans
3. 并发连接数过高 / High concurrent connection count
4. 锁等待或死锁问题 / Lock wait or deadlock issues
5. 实例规格不足以支撑当前负载 / Instance type insufficient for current load

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

### 慢查询导致 / Caused by Slow Queries

**步骤 1:** 识别消耗CPU最高的查询 / Identify queries consuming most CPU: SHOW PROCESSLIST

**步骤 2:** 分析慢查询日志 / Analyze slow query log

**步骤 3:** 检查缺失索引 / Check for missing indexes: EXPLAIN [query]

**步骤 4:** 添加必要索引或优化查询 / Add necessary indexes or optimize queries

**步骤 5:** 如需紧急处理可KILL长时间运行的查询 / Kill long-running queries if urgent: KILL [process_id]

### 连接数过高 / Caused by High Connections

**步骤 1:** 检查当前连接数 / Check current connections: SHOW STATUS LIKE 'Threads_connected'

**步骤 2:** 识别占用连接的应用 / Identify applications holding connections

**步骤 3:** 优化应用连接池配置 / Optimize application connection pool settings

**步骤 4:** 考虑增加max_connections参数 / Consider increasing max_connections parameter

**步骤 5:** 评估是否需要升级实例规格 / Evaluate if instance upgrade is needed


---

## 升级标准 Escalation Criteria

### 升级条件 When to Escalate

| 条件 Condition | 时间要求 Time Requirement | 升级目标 Escalation Target |
|---------------|--------------------------|---------------------------|
| 初次响应无法解决 / Initial response cannot resolve | 3m | L2 Support |
| 问题持续恶化 / Issue continues to worsen | +10分钟 / +10 minutes | Team Lead |
| 影响扩大到其他服务 / Impact spreads to other services | 立即 / Immediately | SRE On-Call |
| 需要外部支持 / External support needed | 根据情况 / As needed | Vendor/AWS Support |

### 升级联系方式 Escalation Contacts

| 角色 Role | 联系方式 Contact |
|-----------|-----------------|
| **主要负责团队 Primary Team** | DBA (数据库管理) |
| **On-Call** | dba-oncall@luckin.com |
| **Slack Channel** | #dba-alerts |
| **升级邮件 Escalation Email** | escalation@luckin.com |
| **紧急热线 Emergency Hotline** | +1-XXX-XXX-XXXX |

### 升级时需提供信息 Information Required for Escalation

```
1. 告警名称和ID / Alert name and ID: 【DB告警】AWS-RDS CPU使用率连续三分钟大于90% (ALR-019)
2. 告警触发时间 / Alert trigger time
3. 当前状态 / Current status
4. 已采取的措施 / Actions taken
5. 影响范围评估 / Impact assessment
6. 相关日志和指标截图 / Related logs and metric screenshots
7. 诊断命令输出 / Diagnostic command output
```

---

## 预防措施 Prevention Measures

- 定期审查和优化慢查询 / Regularly review and optimize slow queries
- 设置合理的连接池参数 / Configure appropriate connection pool parameters
- 实施数据库性能监控仪表板 / Implement database performance monitoring dashboard
- 定期进行容量规划评估 / Conduct regular capacity planning assessments
- 配置自动存储扩展 / Configure automatic storage scaling
- 建立索引审计机制 / Establish index audit mechanism

---

## 相关告警 Related Alerts

以下告警经常与此告警同时出现或有关联关系:

The following alerts often appear together or are related to this alert:

- `【DB告警】AWS RDS CPU使用率连续三分钟大于90%`
- `【DB告警】AWS RDS 慢查询数量持续三分钟大于300个`
- `【DB告警】AWS RDS 活跃线程持续两分钟大于24`
- `【DB告警】AWS RDS 磁盘空间连续3分钟不足10G`
- `【DB告警】AWS RDS Vip 持续一分钟不通`

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
