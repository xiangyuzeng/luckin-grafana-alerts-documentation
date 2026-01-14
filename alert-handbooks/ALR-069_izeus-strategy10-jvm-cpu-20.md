# 【iZeus告警】JVM CPU使用率超过20% (策略10)

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-069 |
| **告警名称** | 【iZeus告警】JVM CPU使用率超过20% (策略10) |
| **优先级** | P2 |
| **服务等级** | L1 |
| **类别** | APM-iZeus-Strategy |
| **响应时间** | 标准响应（< 30分钟） |
| **责任团队** | APM团队 |

---

## 告警描述

此告警属于 **P2** 优先级，影响 **L1** 级别服务。

**责任团队:** APM团队负责处理此类告警。

**系统上下文:** 此告警涉及 Kubernetes 命名空间: rd-sales, rd-finance。

**系统上下文:** 此告警涉及 Kubernetes 命名空间: rd-sales, rd-finance。

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

### Prometheus 指标查询 (Grafana Explore)
```promql
# GC 暂停时间
rate(jvm_gc_pause_seconds_sum[5m])

# JVM 内存使用
jvm_memory_used_bytes

# 活跃线程数
jvm_threads_live_threads

# 守护线程数
jvm_threads_daemon_threads

# 堆内存使用率
jvm_memory_used_bytes{area="heap"} / jvm_memory_max_bytes{area="heap"} * 100
```

### JVM 诊断命令
```bash
# 获取堆转储 (在容器内)
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- jmap -dump:format=b,file=/tmp/heapdump.hprof [PID]

# 查看线程转储
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- jstack [PID]

# 查看 GC 日志
kubectl logs [POD_NAME] -n [NAMESPACE] | grep -i "gc"

# 查看 JVM 参数
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- java -XX:+PrintFlagsFinal -version
```

---

## 诊断命令

### Prometheus 指标查询 (Grafana Explore)
```promql
# GC 暂停时间
rate(jvm_gc_pause_seconds_sum[5m])

# JVM 内存使用
jvm_memory_used_bytes

# 活跃线程数
jvm_threads_live_threads

# 守护线程数
jvm_threads_daemon_threads

# 堆内存使用率
jvm_memory_used_bytes{area="heap"} / jvm_memory_max_bytes{area="heap"} * 100
```

### JVM 诊断命令
```bash
# 获取堆转储 (在容器内)
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- jmap -dump:format=b,file=/tmp/heapdump.hprof [PID]

# 查看线程转储
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- jstack [PID]

# 查看 GC 日志
kubectl logs [POD_NAME] -n [NAMESPACE] | grep -i "gc"

# 查看 JVM 参数
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- java -XX:+PrintFlagsFinal -version
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
| [JVM Micrometer Dashboard](https://luckin-na-grafana.lkcoffee.com/d/jvm-micrometer) | Jvm Overview 监控 |
| [Kubernetes Pods Dashboard](https://luckin-na-grafana.lkcoffee.com/d/kubernetes-pods) | Kubernetes 监控 |

**Grafana 访问地址:** https://luckin-na-grafana.lkcoffee.com

**Prometheus 数据源:**
- MySQL 指标: `ff7hkeec6c9a8e`
- Redis 指标: `ff6p0gjt24phce`
- 默认指标: `df8o21agxtkw0d`
