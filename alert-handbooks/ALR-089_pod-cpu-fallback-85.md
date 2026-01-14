# 【Pod告警】CPU使用率超过85% (Fallback)

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-089 |
| **告警名称** | 【Pod告警】CPU使用率超过85% (Fallback) |
| **优先级** | P1 |
| **服务等级** | L0 |
| **类别** | Pod |
| **响应时间** | 快速响应（< 15分钟） |
| **责任团队** | DevOps团队 |

---

## 告警描述

此告警属于 **P1** 优先级，影响 **L0** 级别服务。

**责任团队:** DevOps团队负责处理此类告警。

**系统上下文:** 此告警涉及 Kubernetes 命名空间: rd-sales, rd-finance, rd-supplychains。

**系统上下文:** 此告警涉及 Kubernetes 命名空间: rd-sales, rd-finance, rd-supplychains。

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

### kubectl 诊断命令
```bash
# 查看所有命名空间的 Pod 状态
kubectl get pods -A | grep -E "(rd-|baseservices-)"

# 查看特定命名空间的 Pod 详情
kubectl get pods -n rd-sales -o wide
kubectl get pods -n rd-finance -o wide

# 查看 Pod 事件
kubectl describe pod [POD_NAME] -n [NAMESPACE]

# 查看 Pod 日志
kubectl logs [POD_NAME] -n [NAMESPACE] --tail=100

# 查看资源使用情况
kubectl top pods -n [NAMESPACE]
kubectl top nodes
```

### Prometheus 指标查询 (Grafana Explore)
```promql
# 容器 CPU 使用率
sum(rate(container_cpu_usage_seconds_total{namespace=~"rd-.*|baseservices-.*"}[5m])) by (namespace, pod)

# 容器内存使用量
sum(container_memory_working_set_bytes{namespace=~"rd-.*|baseservices-.*"}) by (namespace, pod)

# 容器重启次数 (过去1小时)
sum(increase(kube_pod_container_status_restarts_total[1h])) by (namespace, pod)

# OOM 事件
sum(increase(container_oom_events_total[1h])) by (namespace, pod)

# Pod 状态
kube_pod_status_phase

# Deployment 可用副本
kube_deployment_status_replicas_available
```

### 关键命名空间
**业务服务:**
- 销售: `rd-sales`
- 财务: `rd-finance`
- 供应链: `rd-supplychains`

**基础服务:**
- 风控: `baseservices-riskcontrol`
- API网关: `api-gateway`
- 监控: `monitor`

---

## 诊断命令

### kubectl 诊断命令
```bash
# 查看所有命名空间的 Pod 状态
kubectl get pods -A | grep -E "(rd-|baseservices-)"

# 查看特定命名空间的 Pod 详情
kubectl get pods -n rd-sales -o wide
kubectl get pods -n rd-finance -o wide

# 查看 Pod 事件
kubectl describe pod [POD_NAME] -n [NAMESPACE]

# 查看 Pod 日志
kubectl logs [POD_NAME] -n [NAMESPACE] --tail=100

# 查看资源使用情况
kubectl top pods -n [NAMESPACE]
kubectl top nodes
```

### Prometheus 指标查询 (Grafana Explore)
```promql
# 容器 CPU 使用率
sum(rate(container_cpu_usage_seconds_total{namespace=~"rd-.*|baseservices-.*"}[5m])) by (namespace, pod)

# 容器内存使用量
sum(container_memory_working_set_bytes{namespace=~"rd-.*|baseservices-.*"}) by (namespace, pod)

# 容器重启次数 (过去1小时)
sum(increase(kube_pod_container_status_restarts_total[1h])) by (namespace, pod)

# OOM 事件
sum(increase(container_oom_events_total[1h])) by (namespace, pod)

# Pod 状态
kube_pod_status_phase

# Deployment 可用副本
kube_deployment_status_replicas_available
```

### 关键命名空间
**业务服务:**
- 销售: `rd-sales`
- 财务: `rd-finance`
- 供应链: `rd-supplychains`

**基础服务:**
- 风控: `baseservices-riskcontrol`
- API网关: `api-gateway`
- 监控: `monitor`


---

## 根因分析

### 常见原因

1. 应用内存泄漏
2. CPU密集型操作
3. 线程池配置不当
4. JVM参数配置不合理
5. 外部依赖响应慢导致线程阻塞
6. 容器资源限制过低

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

**步骤 1:** 检查Pod资源使用: `kubectl top pods`

**步骤 2:** 查看应用日志排查CPU密集操作

**步骤 3:** 分析线程堆栈: `jstack [PID]`

**步骤 4:** 优化代码或增加Pod资源限制

**步骤 5:** 考虑水平扩容增加副本数

### Pod重启

**步骤 1:** 检查重启原因: `kubectl describe pod`

**步骤 2:** 查看之前容器日志: `kubectl logs --previous`

**步骤 3:** 检查是否OOM或健康检查失败

**步骤 4:** 调整资源配置或修复应用问题

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

- 合理配置资源请求和限制
- 实施应用性能监控
- 定期进行容量评估
- 配置健康检查
- 建立自动扩容机制
- 优化JVM参数配置

---

## 相关告警

以下告警经常与此告警同时出现或有关联关系:

- `【Pod告警】CPU使用率超过85%`
- `【Pod告警】Pod内存OOM`
- `【Pod告警】Pod在2分钟内重启`
- `【Pod告警】Node心跳丢失`
- `【Pod告警】Pod线程数超过3600`

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
