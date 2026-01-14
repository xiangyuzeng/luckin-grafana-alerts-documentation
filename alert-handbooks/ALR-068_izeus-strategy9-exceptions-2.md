# 【iZeus告警】异常数量超过2个 (策略9)

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-068 |
| **告警名称** | 【iZeus告警】异常数量超过2个 (策略9) |
| **优先级** | P1 |
| **服务等级** | L0 |
| **类别** | APM-iZeus-Strategy |
| **响应时间** | 快速响应（< 15分钟） |
| **责任团队** | APM团队 |

---

## 告警描述

此告警属于 **P1** 优先级，影响 **L0** 级别服务。

**责任团队:** APM团队负责处理此类告警。

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

### 通用 Prometheus 指标查询
```promql
# 节点 CPU 使用率
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 节点内存使用率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# 节点磁盘使用率
(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100
```

### 通用诊断命令
```bash
# 检查服务健康状态
curl -s http://[SERVICE_ENDPOINT]/health

# 检查网络连通性
ping [TARGET_HOST]
telnet [TARGET_HOST] [PORT]

# 检查日志
kubectl logs [POD_NAME] -n [NAMESPACE] --tail=100
```

---

## 诊断命令

### 通用 Prometheus 指标查询
```promql
# 节点 CPU 使用率
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 节点内存使用率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# 节点磁盘使用率
(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100
```

### 通用诊断命令
```bash
# 检查服务健康状态
curl -s http://[SERVICE_ENDPOINT]/health

# 检查网络连通性
ping [TARGET_HOST]
telnet [TARGET_HOST] [PORT]

# 检查日志
kubectl logs [POD_NAME] -n [NAMESPACE] --tail=100
```


---

## 根因分析

### 常见原因

1. 服务实例异常
2. 配置变更导致
3. 资源不足
4. 网络问题
5. 依赖服务故障
6. 数据异常

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
| [Kubernetes Pods Dashboard](https://luckin-na-grafana.lkcoffee.com/d/kubernetes-pods) | Kubernetes 监控 |
| [Node Exporter Full](https://luckin-na-grafana.lkcoffee.com/d/node-exporter-full) | Node Exporter 监控 |

**Grafana 访问地址:** https://luckin-na-grafana.lkcoffee.com

**Prometheus 数据源:**
- MySQL 指标: `ff7hkeec6c9a8e`
- Redis 指标: `ff6p0gjt24phce`
- 默认指标: `df8o21agxtkw0d`
