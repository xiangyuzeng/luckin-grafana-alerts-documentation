# 【VM告警】入站网络错误超过20

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-113 |
| **告警名称** | 【VM告警】入站网络错误超过20 |
| **优先级** | P2 |
| **服务等级** | L1 |
| **类别** | VM |
| **响应时间** | 标准响应（< 30分钟） |
| **责任团队** | DevOps团队 |

---

## 告警描述

此告警属于 **P2** 优先级，影响 **L1** 级别服务。

**责任团队:** DevOps团队负责处理此类告警。

---

## 立即响应

### 第一步: 评估告警影响

**检查此告警对业务的影响:**

```
检查点:
1. 告警是否持续存在
2. 是否有关联的高优先级告警
3. 相关服务的整体健康状态
```

**处理建议:**
- 此告警优先级较低，可以按正常流程处理
- 先观察5-10分钟，看告警是否自动恢复
- 部分此类告警可能是瞬时波动导致的误报
- 如果持续存在，再进行详细排查

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

1. 应用进程资源占用过高
2. 磁盘IO瓶颈
3. 内存泄漏或不足
4. 网络问题
5. 系统进程异常
6. 硬件故障

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

### CPU使用率过高

**步骤 1:** 使用 `top` 或 `htop` 查看进程CPU使用

**步骤 2:** 分析高CPU进程

**步骤 3:** 检查是否有异常进程

**步骤 4:** 优化应用或增加资源

### 磁盘空间不足

**步骤 1:** 检查磁盘使用: `df -h`

**步骤 2:** 查找大文件: `du -sh /* | sort -rh | head -20`

**步骤 3:** 清理日志文件和临时文件

**步骤 4:** 考虑扩容磁盘

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

- 监控资源使用趋势
- 定期清理日志和临时文件
- 配置自动扩容策略
- 建立资源使用告警
- 定期进行系统维护
- 优化应用配置

---

## 相关告警

以下告警经常与此告警同时出现或有关联关系:

- `【VM告警】CPU平均使用率超过80%`
- `【VM告警】内存使用率持续10分钟超过90%`
- `【VM告警】磁盘使用率超过90%`
- `【VM告警】心跳丢失超过10分钟`
- `【VM告警】文件系统只读`

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
