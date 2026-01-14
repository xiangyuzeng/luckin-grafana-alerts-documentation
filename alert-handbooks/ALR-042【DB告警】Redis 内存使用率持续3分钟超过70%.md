# ALR-042【DB告警】Redis 内存使用率持续3分钟超过70%

> **⭐ 高频告警** - 此告警在生产环境中频繁出现，已有详细处理案例和最佳实践。

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-042 |
| **告警名称** | 【Redis告警】ElastiCache 内存使用率超过70% |
| **优先级** | P1 |
| **服务等级** | L0 |
| **类别** | Database-Redis |
| **响应时间** | 快速响应（< 15分钟） |

---

## 告警描述

此告警属于 **P1** 优先级，影响 **L0** 级别服务。

---

## 告警解析

### 告警含义

Redis实例内存使用率连续3分钟超过70%，接近内存上限。

### 业务影响

- **Key淘汰**: 可能触发maxmemory-policy策略淘汰Key
- **OOM风险**: 继续增长可能导致Redis OOM
- **写入失败**: 达到上限后新写入可能失败

### 受影响服务

所有使用该Redis实例的缓存服务

### PromQL表达式

```promql
avg_over_time(aws_elasticache_database_memory_usage_percentage_average[3m]) > 70
```

### 常见根因

1. **数据未过期**: TTL设置不当导致数据累积
2. **大Key**: 存在占用大量内存的Key
3. **业务增长**: 缓存数据量自然增长
4. **内存碎片**: Redis内存碎片率过高

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
# 检查ElastiCache集群状态
aws elasticache describe-cache-clusters \
  --show-cache-node-info

# 检查Redis内存使用
redis-cli -h [REDIS_ENDPOINT] INFO memory

# 检查Redis客户端连接
redis-cli -h [REDIS_ENDPOINT] CLIENT LIST

# 检查Redis慢日志
redis-cli -h [REDIS_ENDPOINT] SLOWLOG GET 10
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

**根据实际案例分析（2025-09-17 luckyus-web集群案例）：**

**触发规则（内存）：**
- FreeableMemory 持续 < 1 GiB（约等价使用率 > 70%），且一周趋势无回升 → **扩容**
- 若仅短时波动（Spike），且随即回升，可继续观察
- 如出现 **Evictions/SWAP**，优先扩容

**扩容方式（默认）：**
1. **纵向扩容（优先）**：节点规格上升一个档位，例如：`cache.t4g.medium` → `cache.t4g.large`
2. **读多写少**：可增加 Read Replica 分担读
3. **写入压力/键空间过大**：评估开启集群分片做水平扩展


### 常见原因

1. **数据未过期**: TTL设置不当导致数据累积
2. **大Key**: 存在占用大量内存的Key
3. **业务增长**: 缓存数据量自然增长
4. **内存碎片**: Redis内存碎片率过高

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

### 步骤1：确认内存与CPU状态

**登录AWS控制台：** Amazon ElastiCache → 选择 Redis 集群（如 luckyus-web）

**检查内存相关指标（CloudWatch → Metrics → ElastiCache）：**
- `FreeableMemory`（空闲可释放内存）一周趋势
- **判定标准**：若持续 < 1 GiB 且无回升趋势，判定为内存压力，需要扩容
- 同步查看 `Evictions`（是否发生驱逐）、`SwapUsage`（是否出现交换）
- `BytesUsedForCache / EngineUsedMemory`：确认已用内存接近总内存上限
- **截图**：保存一周趋势图（用于变更确认与复盘）

**检查 CPU 指标（建议）：**
- `CPUUtilization`：如持续高于 80%（或 2 核实例总CPU > ~45%），需一并评估

### 步骤2：访问集群与参数信息

**通过AWS控制台：** ElastiCache → Redis → Clusters → 点击集群名称

**查看 Nodes / Metrics / Parameter groups：**
- **参数组**：如 luckyus-ha-6（使用 LRU 驱逐策略 volatile-lru）
- **Multi-AZ 与副本**：Enabled（可降低扩容/故障切换影响）

### 步骤3：确定扩容策略

| 情况 | 处理方式 |
|------|---------|
| FreeableMemory 持续 < 1 GiB | 扩容（纵向） |
| 读多写少场景 | 增加 Read Replica |
| 写入压力/键空间过大 | 开启集群分片（水平扩展） |

### 步骤4：执行扩容操作

**截图记录（重要）：**
- 扩容前：FreeableMemory 一周趋势、Evictions/SwapUsage/CPU 指标截图
- 集群详情页（Engine、Multi-AZ、节点类型、参数组）截图

**通知方式：企业微信告警群/DBA值班**
- 说明：问题现象、阈值命中、建议动作（上调一档）、预计影响（短暂 failover/连接重试）

**控制台扩容：**
1. ElastiCache → Redis → Clusters → 选择集群 → Modify
2. Node type：从 cache.t4g.medium 调整为上一档
3. 其他项保持不变，提交变更
4. 关注状态：modifying → available

**监控恢复情况：**
- 等待 ~20 分钟（视数据量而定）
- 重新查看 FreeableMemory 是否显著回升（> 1 GiB）
- 确认告警解除、应用无持续报错

### 注意事项

⚠️ **关键提醒：**
- 扩容会触发**主从切换**，存在**短暂连接中断**；务必确认客户端具备**重连/重试**
- 若使用 **T 系列（t4g）**，避免长期高负载耗尽 CPU Credit；持续高负载建议改用 M/R 系列
- 仅当**持续性**内存紧张时扩容；瞬时峰值应结合 Evictions/Swap 判断
- 在业务低峰进行计划性扩容，降低影响面
- 变更前后务必**留痕**（截图/记录）


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

- 监控内存使用趋势
- 设置合理的过期策略
- 避免大Key操作
- 配置合理的连接池
- 定期清理无用数据
- 建立容量规划机制

---

## 相关告警

以下告警经常与此告警同时出现或有关联关系:

- `【Redis告警】ElastiCache CPU使用率超过90%`
- `【Redis告警】ElastiCache 内存使用率超过70%`
- `【Redis告警】ElastiCache 延迟超过2ms`
- `【Redis告警】ElastiCache Key驱逐告警`
- `【Redis告警】ElastiCache 客户端阻塞`
