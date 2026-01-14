# ALR-023【DB告警】AWS RDS 发生重启或者主从切换

> **⭐ 高频告警** - 此告警在生产环境中频繁出现，已有详细处理案例和最佳实践。

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-023 |
| **告警名称** | 【DB告警】AWS RDS Failover或重启 |
| **优先级** | P0 |
| **服务等级** | L0 |
| **类别** | Database-RDS |
| **响应时间** | 立即响应（< 5分钟） |

---

## 告警描述

此告警属于 **P0** 优先级，影响 **L0** 级别服务。

---

## 告警解析

### 告警含义

检测到RDS实例发生重启或主从切换，mysql_global_status_uptime计数器重置。

### 业务影响

- **短暂服务中断**: 切换期间(通常30秒-2分钟)数据库不可写
- **连接重置**: 所有现有数据库连接将被断开
- **事务回滚**: 切换时未完成的事务将被回滚

### 受影响服务

所有依赖该RDS实例的微服务需要重新建立连接

### PromQL表达式

```promql
changes(mysql_global_status_uptime[5m]) > 0
```

### 常见根因

1. **自动故障转移**: Multi-AZ实例主节点故障触发自动切换
2. **维护窗口**: AWS计划内维护导致的重启
3. **手动操作**: DBA执行的重启或切换操作
4. **资源耗尽**: 内存或存储空间耗尽导致实例重启

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

**根据实际案例分析（2025-10-24 aws-luckyus-opshop-rw案例）：**

本次重启与主从切换由**底层宿主机故障引发**，体现为"主机因网络连通性丢失不可达"，RDS 自动执行**主机替换 + 实例重启 + Multi-AZ Failover**。

**AWS 官方知识库说明：**
- 当primary host 不可达（网络连通性丢失）时会触发Multi-AZ failover 和实例重启，属于底层网络/基础设施瞬时异常场景
- 硬件问题会在 Multi-AZ 中触发failover，同时 RDS 可能进行底层宿主机替换；这是 RDS 的自动自愈行为
- Multi-AZ 的 failover 由 RDS 自动处理，常见时长**60-120秒**（受事务恢复、负载影响）
- Failover 发生时，RDS 会更新实例的 DNS 指向到新的主库，应用**必须重新建立连接**（特别注意 JVM 的 DNS 缓存 TTL）


### 常见原因

1. **自动故障转移**: Multi-AZ实例主节点故障触发自动切换
2. **维护窗口**: AWS计划内维护导致的重启
3. **手动操作**: DBA执行的重启或切换操作
4. **资源耗尽**: 内存或存储空间耗尽导致实例重启

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
