# ALR-094【pod-宕机】P1 WSS内存使用率连续3分钟等于100%(OOM参考)

> **⭐ 高频告警** - 此告警在生产环境中频繁出现，已有详细处理案例和最佳实践。

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-094 |
| **告警名称** | 【Pod告警】Pod内存OOM |
| **优先级** | P0 |
| **服务等级** | L0 |
| **类别** | Pod |
| **响应时间** | 立即响应（< 5分钟） |

---

## 告警描述

此告警属于 **P0** 优先级，影响 **L0** 级别服务。

---

## 告警解析

### 告警含义

Pod WSS(Working Set Size)内存使用率连续3分钟达到100%，即将或已经OOM。

### 业务影响

- **服务崩溃**: OOM会导致Pod被杀死
- **数据丢失**: 内存中未持久化的数据将丢失
- **级联影响**: 可能导致依赖服务调用失败

### 受影响服务

OOM的Pod所属服务

### PromQL表达式

```promql
avg_over_time(
  (container_memory_working_set_bytes{container!="POD",container!=""}
  /
  kube_pod_container_resource_limits{resource="memory"} * 100)[3m:]
) >= 100
```

### 常见根因

1. **内存泄漏**: 代码存在内存泄漏
2. **JVM配置**: 堆大小超出容器限制
3. **大对象**: 处理大文件或大数据集
4. **缓存过大**: 本地缓存未设置上限

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

**根据实际案例分析（2025-09-23 hello-world案例）：**

**注意：** 容器名字叫hello-world时，很可能是测试服务。在处理此类告警时应优先确认服务性质和业务影响范围。

**OOM（内存溢出）常见原因：**
- 内存限制配置过低
- 应用存在内存泄漏
- 突发流量导致内存暴涨
- JVM堆内存配置不当


### 常见原因

1. **内存泄漏**: 代码存在内存泄漏
2. **JVM配置**: 堆大小超出容器限制
3. **大对象**: 处理大文件或大数据集
4. **缓存过大**: 本地缓存未设置上限

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
- **告警等级**：P1
- **Pod信息**：Pod名称、Pod IP、所属服务
- **当前值**：如 +Inf（表示内存使用率达到100%）

### 步骤2：初步分析

**容器名称分析：**
- 注意容器名称，如 hello-world 可能是测试环境
- 评估业务影响

**初步判断：**
- 很可能是测试环境或测试服务
- 需要确认是否影响生产业务

### 步骤3：问题调研

**联系相关团队：**
- 在告警群组中询问是否知晓问题
- 确认服务归属（如dify相关服务）

### 步骤4：检查服务状态

**容器云平台检查：**
- 登录容器云管理平台
- 找到对应服务和Pod
- 检查：
  - Pod运行状态
  - 内存使用情况
  - CPU使用率
  - 重启次数
  - 是否存在OOM Kill

### 步骤5：处理措施

**如果是测试服务：**
- 确认测试完成后可以清理
- 通知相关开发人员

**如果是正式服务出现OOM：**
- 检查内存限制配置
- 分析内存泄漏可能性
- 考虑扩容或重启操作

**容器操作（如需要）：**
- 在Pod列表中选择对应实例
- 执行重启或扩容操作
- 监控处理进度

### 步骤6：问题解决确认

- [ ] 内存使用率恢复正常
- [ ] Pod运行状态正常
- [ ] 无业务影响
- [ ] 告警解除

### 总结

**后续建议：** 建议测试环境完善资源限制配置，避免类似告警


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
