# 【默认策略】服务器每分钟异常数大于20

> **Luckin Coffee USA - DevOps/DBA Alert Response Handbook**
> **瑞幸咖啡美国 - 运维/DBA告警响应手册**

---

## 告警概览 Alert Overview

| 属性 Attribute | 值 Value |
|----------------|----------|
| **Alert ID** | ALR-087 |
| **告警名称 Alert Name** | 【默认策略】服务器每分钟异常数大于20 |
| **优先级 Priority** | P1 |
| **服务等级 Service Level** | L1 - Important Business/Infrastructure (重要业务服务/重要基础服务) |
| **类别 Category** | APM-Default |
| **系统 System** | VMAlert |
| **指标类型 Metric Type** | Errors |
| **阈值/条件 Threshold** | >20 exceptions/min |
| **持续时间 Duration** | 1m |
| **响应时间 Response Time** | HIGH (< 15 minutes) |
| **责任团队 Owner Team** | DevOps - DevOps (运维开发) |

---

## 告警描述 Description

### 中文说明
此告警在 **>20 exceptions/min** 条件满足时触发。该告警属于 **P1** 优先级，影响 **L1** 级别服务。

**触发条件:** Errors 指标达到阈值 >20 exceptions/min，持续时间: 1m

**重要性:** 此告警关联 运维开发 团队负责的 Auth, CI/CD, Monitoring 领域服务，需要在 < 15 minutes 内响应处理。

### English Description
This alert triggers when the condition **>20 exceptions/min** is met. This is a **P1** priority alert affecting **L1** level services.

**Trigger Condition:** Errors metric reaches threshold >20 exceptions/min, duration: 1m

**Importance:** This alert is associated with the DevOps team's Auth, CI/CD, Monitoring domain services and requires response within < 15 minutes.

---

## 影响范围 Impact Scope

### 关联服务 Affected Services

| 服务名称 Service | 等级 Level | 描述 Description | 团队 Team |
|-----------------|------------|------------------|-----------|
| All Spring Boot Services | L0-L2 | 所有Spring Boot服务 | DevOps |

### 关联数据库 Affected Databases

- `N/A - Infrastructure Alert`

### 业务影响 Business Impact

**P1 - L1 级别告警的业务影响:**

- **严重程度: 高** - 重要业务功能受影响
- 影响重要业务或基础设施服务
- 可能导致部分功能降级
- 需要尽快响应处理

**Severity: HIGH** - Important business functions affected
- Affects important business or infrastructure services
- May cause partial service degradation
- Requires prompt response and handling

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
# 检查服务状态 Check service status
kubectl get pods -A | grep -E "(Error|CrashLoopBackOff|Pending)"

# 检查节点状态 Check node status
kubectl get nodes -o wide
kubectl top nodes

# 检查系统日志 Check system logs
kubectl get events -A --sort-by='.lastTimestamp' | head -50

# 检查Prometheus指标 Check Prometheus metrics
# 通过Grafana Dashboard查看 View via Grafana Dashboard
```

---

## 根因分析 Root Cause Analysis

### 常见原因 Common Causes

1. 系统资源不足 / Insufficient system resources
2. 配置错误 / Configuration error
3. 网络连接问题 / Network connection issues
4. 依赖服务异常 / Dependent service abnormal
5. 代码或应用程序问题 / Code or application issues

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
| 初次响应无法解决 / Initial response cannot resolve | 1m | L2 Support |
| 问题持续恶化 / Issue continues to worsen | +10分钟 / +10 minutes | Team Lead |
| 影响扩大到其他服务 / Impact spreads to other services | 立即 / Immediately | SRE On-Call |
| 需要外部支持 / External support needed | 根据情况 / As needed | Vendor/AWS Support |

### 升级联系方式 Escalation Contacts

| 角色 Role | 联系方式 Contact |
|-----------|-----------------|
| **主要负责团队 Primary Team** | DevOps (运维开发) |
| **On-Call** | devops-oncall@luckin.com |
| **Slack Channel** | #devops-alerts |
| **升级邮件 Escalation Email** | escalation@luckin.com |
| **紧急热线 Emergency Hotline** | +1-XXX-XXX-XXXX |

### 升级时需提供信息 Information Required for Escalation

```
1. 告警名称和ID / Alert name and ID: 【默认策略】服务器每分钟异常数大于20 (ALR-087)
2. 告警触发时间 / Alert trigger time
3. 当前状态 / Current status
4. 已采取的措施 / Actions taken
5. 影响范围评估 / Impact assessment
6. 相关日志和指标截图 / Related logs and metric screenshots
7. 诊断命令输出 / Diagnostic command output
```

---

## 预防措施 Prevention Measures

- 实施主动监控和告警 / Implement proactive monitoring and alerting
- 建立定期系统健康检查 / Establish regular system health checks
- 实施变更管理流程 / Implement change management process
- 进行容量规划和资源优化 / Conduct capacity planning and resource optimization
- 建立事件响应和复盘机制 / Establish incident response and post-mortem process

---

## 相关告警 Related Alerts

以下告警经常与此告警同时出现或有关联关系:

The following alerts often appear together or are related to this alert:

- `[LCP-Prod-P0]`
- `[LCP-Prod-P1]`
- `[LCP-Prod-P2]`

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
