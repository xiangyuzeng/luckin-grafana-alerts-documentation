# 【Redis告警】ElastiCache 客户端阻塞

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-043 |
| **告警名称** | 【Redis告警】ElastiCache 客户端阻塞 |
| **优先级** | P1 |
| **服务等级** | L0 |
| **类别** | Database-Redis |
| **响应时间** | 快速响应（< 15分钟） |
| **责任团队** | DBA团队 |

---

## 告警描述

此告警属于 **P1** 优先级，影响 **L0** 级别服务。

**责任团队:** DBA团队负责处理此类告警。

**系统上下文:** 此告警涉及 6 个关键 MySQL 数据库实例。

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

### AWS ElastiCache 状态检查
```bash
# 检查所有 Luckin US ElastiCache 集群
aws elasticache describe-cache-clusters \
  --query 'CacheClusters[?starts_with(CacheClusterId, `luckyus`)].{ID:CacheClusterId,Status:CacheClusterStatus,Engine:Engine,NodeType:CacheNodeType}' \
  --output table

# 检查复制组状态
aws elasticache describe-replication-groups \
  --query 'ReplicationGroups[?starts_with(ReplicationGroupId, `luckyus`)].{ID:ReplicationGroupId,Status:Status,NodeType:CacheNodeType}' \
  --output table
```

### Prometheus 指标查询 (Grafana Explore)
```promql
# 连接客户端数
redis_connected_clients

# 阻塞客户端数
redis_blocked_clients

# 内存使用量
redis_memory_used_bytes

# CPU 使用率
rate(redis_cpu_user_seconds_total[5m]) + rate(redis_cpu_sys_seconds_total[5m])

# 命令处理速率
rate(redis_commands_total[5m])

# 慢日志长度
redis_slowlog_length

# 命中率计算
rate(redis_keyspace_hits_total[5m]) / (rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m]))
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
- luckyus-isales-order
- luckyus-isales-session
- luckyus-isales-commodity
- luckyus-isales-crm
- luckyus-isales-market
- luckyus-isales-member

**认证相关:**
- luckyus-unionauth
- luckyus-aapi-unionauth
- luckyus-sapi-unionauth
- luckyus-open-unionauth
- luckyus-auth
- luckyus-authservice

---

## 诊断命令

### AWS ElastiCache 状态检查
```bash
# 检查所有 Luckin US ElastiCache 集群
aws elasticache describe-cache-clusters \
  --query 'CacheClusters[?starts_with(CacheClusterId, `luckyus`)].{ID:CacheClusterId,Status:CacheClusterStatus,Engine:Engine,NodeType:CacheNodeType}' \
  --output table

# 检查复制组状态
aws elasticache describe-replication-groups \
  --query 'ReplicationGroups[?starts_with(ReplicationGroupId, `luckyus`)].{ID:ReplicationGroupId,Status:Status,NodeType:CacheNodeType}' \
  --output table
```

### Prometheus 指标查询 (Grafana Explore)
```promql
# 连接客户端数
redis_connected_clients

# 阻塞客户端数
redis_blocked_clients

# 内存使用量
redis_memory_used_bytes

# CPU 使用率
rate(redis_cpu_user_seconds_total[5m]) + rate(redis_cpu_sys_seconds_total[5m])

# 命令处理速率
rate(redis_commands_total[5m])

# 慢日志长度
redis_slowlog_length

# 命中率计算
rate(redis_keyspace_hits_total[5m]) / (rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m]))
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
- luckyus-isales-order
- luckyus-isales-session
- luckyus-isales-commodity
- luckyus-isales-crm
- luckyus-isales-market
- luckyus-isales-member

**认证相关:**
- luckyus-unionauth
- luckyus-aapi-unionauth
- luckyus-sapi-unionauth
- luckyus-open-unionauth
- luckyus-auth
- luckyus-authservice


---

## 根因分析

### 常见原因

1. 内存使用接近上限
2. 大Key操作阻塞
3. 客户端连接数过多
4. 网络带宽瓶颈
5. 持久化操作影响性能
6. 热点Key导致负载不均

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

### 内存使用过高

**步骤 1:** 检查内存使用: `INFO memory`

**步骤 2:** 查找大Key: `redis-cli --bigkeys`

**步骤 3:** 分析Key过期策略是否合理

**步骤 4:** 清理过期或无用数据

**步骤 5:** 考虑扩容或数据分片

### 客户端连接问题

**步骤 1:** 检查客户端连接: `CLIENT LIST`

**步骤 2:** 识别异常连接来源

**步骤 3:** 检查应用连接池配置

**步骤 4:** 关闭空闲连接: `CLIENT KILL`

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

---

## Grafana 仪表板参考

| 仪表板 | 用途 |
|--------|------|
| [ElastiCache Redis Overview](https://luckin-na-grafana.lkcoffee.com/d/elasticache-redis-overview) | Elasticache 监控 |
| [Redis Cluster Monitor](https://luckin-na-grafana.lkcoffee.com/d/redis-cluster-monitor) | Redis Cluster 监控 |
| [Kubernetes Pods Dashboard](https://luckin-na-grafana.lkcoffee.com/d/kubernetes-pods) | 容器监控 |

**Grafana 访问地址:** https://luckin-na-grafana.lkcoffee.com

**Prometheus 数据源:**
- MySQL 指标: `ff7hkeec6c9a8e`
- Redis 指标: `ff6p0gjt24phce`
- 默认指标: `df8o21agxtkw0d`
