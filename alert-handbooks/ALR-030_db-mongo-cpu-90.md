# 【MongoDB告警】AWS DocumentDB CPU使用率超过90%

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-030 |
| **告警名称** | 【MongoDB告警】AWS DocumentDB CPU使用率超过90% |
| **优先级** | P1 |
| **服务等级** | L0 |
| **类别** | Database-MongoDB |
| **响应时间** | 快速响应（< 15分钟） |
| **责任团队** | DBA团队 |

---

## 告警描述

此告警属于 **P1** 优先级，影响 **L0** 级别服务。

**责任团队:** DBA团队负责处理此类告警。

**系统上下文:** 此告警涉及 6 个关键 MySQL 数据库实例。

---

## 立即响应

### 第一步: 评估黄金流程影响

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
- 如果5-10分钟内恢复，可能是瞬时波动，记录并关注

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

### AWS RDS 状态检查
```bash
# 检查所有 Luckin US RDS 实例状态
aws rds describe-db-instances \
  --query 'DBInstances[?starts_with(DBInstanceIdentifier, `luckyus`)].{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Class:DBInstanceClass,Engine:Engine,Storage:AllocatedStorage}' \
  --output table

# 检查特定实例的性能指标 (替换 INSTANCE_ID)
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=[INSTANCE_ID] \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average Maximum
```

### Prometheus 指标查询 (Grafana Explore)
```promql
# 慢查询速率 (每秒)
sum(rate(mysql_global_status_slow_queries[5m])) by (instance)

# 活跃连接数
mysql_global_status_threads_connected

# 运行中线程数
mysql_global_status_threads_running

# VIP 健康检查
mysql_check_vip
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
- aws-luckyus-salesorder-rw
- aws-luckyus-salespayment-rw
- aws-luckyus-salescrm-rw
- aws-luckyus-salescommodity-rw
- aws-luckyus-salesmarket-rw
- aws-luckyus-salesmember-rw

**风控相关:**
- aws-luckyus-iriskcontrolservice-rw
- aws-luckyus-iriskcontrol-rw

---

## 根因分析

### 常见原因

1. 查询未使用索引
2. 内存不足导致频繁换页
3. 写入量过大
4. 连接池配置不合理
5. 复制延迟过高

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

### 通用处理步骤

**步骤 1:** 检查服务状态和日志

**步骤 2:** 分析告警触发原因

**步骤 3:** 根据具体情况采取相应措施

**步骤 4:** 验证问题是否解决

**步骤 5:** 记录处理过程和经验

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

- 建立完善的监控体系
- 定期进行容量规划
- 实施自动化运维
- 建立变更管理流程
- 进行定期演练
- 持续优化告警阈值

---

## 相关告警

以下告警经常与此告警同时出现或有关联关系:

- `相关类别的其他告警`
- `依赖服务的告警`
- `资源使用相关告警`

---

## Grafana 仪表板参考

| 仪表板 | 用途 |
|--------|------|
| [Enterprise RDS Health Dashboard](https://luckin-na-grafana.lkcoffee.com/d/enterprise-rds-health) | Rds 监控 |
| [MySQL Enterprise Monitoring Dashboard](https://luckin-na-grafana.lkcoffee.com/d/mysql-enterprise-monitor) | Mysql Overview 监控 |
| [InnoDB Deep Monitoring](https://luckin-na-grafana.lkcoffee.com/d/innodb-deep-monitor) | Mysql Innodb 监控 |
| [NA Weekly Slow SQL Governance](https://luckin-na-grafana.lkcoffee.com/d/na-slow-sql-governance) | Slow Sql 监控 |
| [NA DB Instance Deep Dive](https://luckin-na-grafana.lkcoffee.com/d/na-db-instance-deep-dive) | Db Deep Dive 监控 |
| [Kubernetes Pods Dashboard](https://luckin-na-grafana.lkcoffee.com/d/kubernetes-pods) | 容器监控 |

**Grafana 访问地址:** https://luckin-na-grafana.lkcoffee.com

**Prometheus 数据源:**
- MySQL 指标: `ff7hkeec6c9a8e`
- Redis 指标: `ff6p0gjt24phce`
- 默认指标: `df8o21agxtkw0d`
