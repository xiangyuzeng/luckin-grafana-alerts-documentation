# 【iZeus告警】节点CPU使用率超过85%

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-076 |
| **告警名称** | 【iZeus告警】节点CPU使用率超过85% |
| **优先级** | P1 |
| **服务等级** | L0 |
| **类别** | APM-iZeus-Infra |
| **响应时间** | 快速响应（< 15分钟） |
| **责任团队** | APM团队 |

---

## 告警描述

此告警属于 **P1** 优先级，影响 **L0** 级别服务。

---

## 告警解析

### 告警含义

VM主机整体CPU平均使用率超过80%，服务器负载过高。

### 业务影响

- **性能下降**: 所有运行在该主机上的服务性能下降
- **调度影响**: K8s可能无法在该节点调度新Pod

### 受影响服务

运行在该主机上的所有服务和Pod

### PromQL表达式

```promql
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100) > 80
```

### 常见根因

1. **负载不均**: Pod分布不均匀
2. **资源争抢**: 多个高负载Pod同时运行
3. **系统进程**: 系统级进程占用过多CPU
4. **节点容量**: 节点资源规划不足

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
# 检查相关服务状态
kubectl get pods -A | grep -i [SERVICE_NAME]

# 检查服务日志
kubectl logs -n [NAMESPACE] [POD_NAME] --tail=100

# 检查Grafana仪表板
# 访问相关监控仪表板查看详细指标
```

---

## 根因分析

### 常见原因

1. **负载不均**: Pod分布不均匀
2. **资源争抢**: 多个高负载Pod同时运行
3. **系统进程**: 系统级进程占用过多CPU
4. **节点容量**: 节点资源规划不足

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
