# 【DB告警】AWS RDS Failover或重启 (Voice)

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-024 |
| **告警名称** | 【DB告警】AWS RDS Failover或重启 (Voice) |
| **优先级** | P0 |
| **服务等级** | L0 |
| **类别** | Database-RDS |
| **响应时间** | 立即响应（< 5分钟） |
| **责任团队** | DBA团队 |

---

## 告警描述

此告警属于 **P0** 优先级，影响 **L0** 级别服务。

**责任团队:** DBA团队负责处理此类告警。

**系统上下文:** 此告警涉及 6 个关键 MySQL 数据库实例。

---

## 立即响应

### 第一步: 评估黄金流程影响

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
- 记录并分析是否为误报

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

1. 复杂或未优化的SQL查询消耗过多资源
2. 缺少索引导致全表扫描
3. 并发连接数过高
4. 锁等待或死锁问题
5. 实例规格不足以支撑当前负载
6. 大量慢查询累积

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

### 慢查询导致

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

**步骤 5:** 评估是否需要升级实例规格

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

- 定期审查和优化慢查询
- 设置合理的连接池参数
- 实施数据库性能监控仪表板
- 定期进行容量规划评估
- 配置自动存储扩展
- 建立索引审计机制

---

## 相关告警

以下告警经常与此告警同时出现或有关联关系:

- `【DB告警】AWS-RDS CPU使用率连续三分钟大于90%`
- `【DB告警】AWS RDS 慢查询数量持续三分钟大于300个`
- `【DB告警】AWS RDS 活跃线程持续两分钟大于24`
- `【DB告警】AWS RDS 磁盘空间连续3分钟不足10G`
- `【DB告警】AWS RDS Vip 持续一分钟不通`

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
