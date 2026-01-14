# 【DB告警】AWS RDS 磁盘空间连续3分钟不足10G

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-029 |
| **告警名称** | 【DB告警】AWS RDS 磁盘空间连续3分钟不足10G |
| **优先级** | P1 |
| **服务等级** | L0 |
| **类别** | Database-RDS |
| **响应时间** | 快速响应（< 15分钟） |
| **责任团队** | DBA团队 |

---

## 告警描述

此告警属于 **P1** 优先级，影响 **L0** 级别服务。

---

## 告警解析

### 告警含义

RDS实例可用磁盘空间连续3分钟低于10GB，存储空间即将耗尽。

### 业务影响

- **写入失败**: 空间耗尽后数据库将无法写入
- **服务中断**: 依赖写操作的服务将完全失败
- **数据完整性**: 事务可能无法完成

### 受影响服务

所有需要写入该数据库的服务

### PromQL表达式

```promql
avg_over_time(aws_rds_freestoragespace_average[3m]) / 1024 / 1024 / 1024 < 10
```

### 常见根因

1. **日志文件膨胀**: binlog或慢查询日志占用大量空间
2. **数据增长**: 业务数据自然增长
3. **大表操作**: DDL操作产生临时文件
4. **未清理历史数据**: 归档策略未执行

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

---

## 诊断命令

```bash
# 检查RDS实例状态
aws rds describe-db-instances \
  --query 'DBInstances[?starts_with(DBInstanceIdentifier, `luckyus`)].{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Class:DBInstanceClass}'

# 检查RDS性能指标
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=[INSTANCE_ID] \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average Maximum

# 检查慢查询
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW PROCESSLIST;"
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW FULL PROCESSLIST;"

# 检查InnoDB状态
mysql -h [RDS_ENDPOINT] -u admin -p -e "SHOW ENGINE INNODB STATUS\G"
```

---

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
aws rds describe-db-instances \
  --query 'DBInstances[?starts_with(DBInstanceIdentifier, `aws-luckyus`)].{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Class:DBInstanceClass,CPU:toString(EngineVersion)}' \
  --output table
```

**查看特定实例的CPU指标:**
```bash
# 替换 INSTANCE_ID 为实际的实例ID
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=aws-luckyus-salesorder-rw \
  --start-time $(date -u -d '30 minutes ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics Average Maximum
```

**查看数据库连接数:**
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name DatabaseConnections \
  --dimensions Name=DBInstanceIdentifier,Value=aws-luckyus-salesorder-rw \
  --start-time $(date -u -d '30 minutes ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics Average Maximum
```

## 根因分析

### 常见原因

1. **日志文件膨胀**: binlog或慢查询日志占用大量空间
2. **数据增长**: 业务数据自然增长
3. **大表操作**: DDL操作产生临时文件
4. **未清理历史数据**: 归档策略未执行

#### Luckin系统特定原因

根据系统架构，以下是可能的特定原因:

1. **核心服务影响**: 检查salesorder-rw、salespayment-rw等核心数据库
2. **缓存层问题**: 检查luckyus-isales-order、luckyus-session等Redis集群
3. **认证链路**: 检查unionauth相关服务和Redis
4. **风控链路**: 检查iriskcontrol服务状态

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
