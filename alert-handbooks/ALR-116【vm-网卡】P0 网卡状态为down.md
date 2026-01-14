# ALR-116【vm-网卡】P0 网卡状态为down

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-116 |
| **告警名称** | 【VM告警】网卡Down |
| **优先级** | P0 |
| **服务等级** | L0 |
| **类别** | VM |
| **响应时间** | 立即响应（< 5分钟） |

---

## 告警描述

此告警属于 **P0** 优先级，影响 **L0** 级别服务。

---

## 告警解析

### 告警含义

Pod CPU使用率连续3分钟超过资源限制的85%，这是一个兜底告警。

### 业务影响

- **服务限流**: 接近CPU限制，可能被K8s节流
- **响应延迟**: 服务处理能力下降
- **Pod重启风险**: 持续高负载可能触发OOM Killer

### 受影响服务

告警中指定的Pod所属服务

### PromQL表达式

```promql
avg_over_time(
  (sum(rate(container_cpu_usage_seconds_total{container!="POD",container!=""}[1m])) by (pod,namespace)
  /
  sum(kube_pod_container_resource_limits{resource="cpu"}) by (pod,namespace) * 100)[3m:]
) > 85
```

### 常见根因

1. **代码问题**: 存在CPU密集型逻辑或死循环
2. **流量突增**: 业务流量超出预期
3. **资源配置不当**: CPU limit设置过低
4. **GC问题**: JVM频繁GC消耗CPU

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
# 检查CPU使用率
top -bn1 | head -20

# 检查内存使用
free -h

# 检查磁盘使用
df -h

# 检查IO状态
iostat -x 1 5

# 检查网络连接
netstat -tunlp | head -20
ss -tunlp | head -20
```

---

## 根因分析

### 常见原因

1. **代码问题**: 存在CPU密集型逻辑或死循环
2. **流量突增**: 业务流量超出预期
3. **资源配置不当**: CPU limit设置过低
4. **GC问题**: JVM频繁GC消耗CPU

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
