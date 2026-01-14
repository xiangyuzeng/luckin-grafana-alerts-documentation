# ALR-093【pod-全局】P0 Pod 2m内发生重启请关注

> **⭐ 高频告警** - 此告警在生产环境中频繁出现，已有详细处理案例和最佳实践。

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-093 |
| **告警名称** | 【Pod告警】Pod在2分钟内重启 |
| **优先级** | P1 |
| **服务等级** | L0 |
| **类别** | Pod |
| **响应时间** | 快速响应（< 15分钟） |

---

## 告警描述

此告警属于 **P1** 优先级，影响 **L0** 级别服务。

---

## 告警解析

### 告警含义

Pod在最近2分钟内发生了重启，可能是异常退出或健康检查失败。

### 业务影响

- **服务中断**: 重启期间服务不可用
- **请求失败**: 正在处理的请求将失败
- **流量切换**: K8s会将流量切走，可能造成其他Pod压力增加

### 受影响服务

重启的Pod所属服务及其依赖服务

### PromQL表达式

```promql
increase(kube_pod_container_status_restarts_total[2m]) > 0
```

### 常见根因

1. **OOM Kill**: 内存超限被系统杀死
2. **健康检查失败**: Liveness Probe失败
3. **应用崩溃**: 未捕获异常导致进程退出
4. **资源不足**: 节点资源不足触发驱逐

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
# 检查Pod状态
kubectl get pods -n [NAMESPACE] -o wide

# 检查Pod日志
kubectl logs -n [NAMESPACE] [POD_NAME] --tail=100

# 检查Pod详情
kubectl describe pod -n [NAMESPACE] [POD_NAME]

# 检查Pod资源使用
kubectl top pods -n [NAMESPACE]

# 检查Node资源
kubectl top nodes
```

---

## 根因分析

**根据实际案例分析（2025-09-16 iluckysentrybot-pd案例）：**

Pod重启可能由多种原因引起：
- 内存溢出（OOM）
- 健康检查失败
- 应用崩溃
- 资源限制触发
- Kubernetes调度变更

**服务等级说明：**
- L2（普通业务服务）：可按正常流程处理
- L0/L1（核心服务）：需要立即响应


### 常见原因

1. **OOM Kill**: 内存超限被系统杀死
2. **健康检查失败**: Liveness Probe失败
3. **应用崩溃**: 未捕获异常导致进程退出
4. **资源不足**: 节点资源不足触发驱逐

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

检查告警详情，确认：
- **告警等级**：P0/P1/P2
- **服务等级**：L0/L1/L2
- **Pod名称**
- **所属服务**

**打开Grafana链接查看告警详情**

### 步骤2：检查服务状态

**容器云平台检查：**
1. 登录容器云管理平台
2. 找到对应服务
3. 检查Pod状态：
   - Pod名称
   - 运行状态
   - 重启次数
   - CPU/内存使用率

### 步骤3：联系负责人

**通过服务树找到负责人信息：**
- 在LSOP → 服务树 → 基础信息中查找
- 在告警群组中询问是否知晓问题

### 步骤4：处理措施

**重启服务（如需要）：**

**方式一：持续交付平台操作：**
- 路径：PROD > LUCKY > WEB > [服务名]
- 选择受影响的Pod
- 执行滚动重启

**方式二：容器云平台操作：**
- 在Pod列表中选择对应实例
- 点击"重启"按钮
- 监控重启进度

**重启后验证：**
- 确认所有Pod恢复Running状态
- 检查健康检查endpoint响应正常
- 验证Grafana指标恢复正常

### 步骤5：问题解决确认

- [ ] 错误率恢复正常
- [ ] 响应时间符合预期
- [ ] 所有Pod运行正常
- [ ] 健康检查通过


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
