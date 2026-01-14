# ALR-038【DB告警】AWS-ES磁盘空间不足10G

> **⭐ 高频告警** - 此告警在生产环境中频繁出现，已有详细处理案例和最佳实践。

> **瑞幸咖啡美国运维告警响应参考手册**
>
> 本手册为参考文档，请根据实际情况灵活处理。

---

## 告警概览

| 属性 | 值 |
|------|-----|
| **告警ID** | ALR-038 |
| **告警名称** | 【ES告警】OpenSearch磁盘空间不足10G |
| **优先级** | P1 |
| **服务等级** | L0 |
| **类别** | Database-OpenSearch |
| **响应时间** | 快速响应（< 15分钟） |

---

## 告警描述

此告警属于 **P1** 优先级，影响 **L0** 级别服务。

---

## 告警解析

### 告警含义

RDS实例可用磁盘空间连续3分钟低于10GB，存储空间即将耗尽。

### 业务影响

- **写入失败**: 空间耗尽后数据库将无法写入
- **服务中断**: 依赖写操作的服务将完全失败
- **数据完整性**: 事务可能无法完成

### 受影响服务

所有需要写入该数据库的服务

### PromQL表达式

```promql
avg_over_time(aws_rds_freestoragespace_average[3m]) / 1024 / 1024 / 1024 < 10
```

### 常见根因

1. **日志文件膨胀**: binlog或慢查询日志占用大量空间
2. **数据增长**: 业务数据自然增长
3. **大表操作**: DDL操作产生临时文件
4. **未清理历史数据**: 归档策略未执行

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
# 检查OpenSearch域状态
aws opensearch describe-domain --domain-name [DOMAIN_NAME]

# 检查集群健康状态
curl -X GET "https://[OPENSEARCH_ENDPOINT]/_cluster/health?pretty"

# 检查节点状态
curl -X GET "https://[OPENSEARCH_ENDPOINT]/_cat/nodes?v"

# 检查索引状态
curl -X GET "https://[OPENSEARCH_ENDPOINT]/_cat/indices?v"
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

**根据实际案例分析（2025-09-13案例）：**

**日志保留规则（重要）：**

| 日志类型 | 保留策略 | 索引命名示例 |
|---------|---------|------------|
| 按月生成日志 | 保留 3-6 个月 | logs-2024.09 |
| 按日生成日志 | 保留 7 天 | logs-2024.09.13 |
| LFE集群 (luckylfe-log) | 保留 30 天 | - |
| urlog集群 (luckyur-log) | 保留 15 天 | - |
| dify集群 | 暂不处理 | - |

**清理优先级（默认）：**
1. **优先删除**：按日生成的过期日志（超过保留期限）
2. **次要删除**：大容量索引（> 1GB）中的过期数据
3. **谨慎删除**：按月生成的日志（除非确实超过 3-6 个月）
4. **不删除**：当前活跃索引、系统索引（.开头）、dify集群数据


### 常见原因

1. **日志文件膨胀**: binlog或慢查询日志占用大量空间
2. **数据增长**: 业务数据自然增长
3. **大表操作**: DDL操作产生临时文件
4. **未清理历史数据**: 归档策略未执行

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

### 步骤1：确认磁盘空间与集群状态

**登录AWS控制台：** Amazon OpenSearch Service → 选择告警集群

**检查磁盘空间相关指标（CloudWatch → Metrics → OpenSearch）：**
- `FreeStorageSpace`（剩余可用空间）一周趋势
- **判定标准**：若持续 < 10 GiB 且呈下降趋势，判定为磁盘压力，需要立即清理
- 同步查看 `ClusterIndexWritesBlocked`（是否发生写入阻塞）、`JVMMemoryPressure`（内存压力）

**ClusterHealthStatus 确认：**
- **Red**：立即处理，可能已影响服务
- **Yellow**：需要关注，副本可能受影响
- **Green**：正常状态

### 步骤2：访问索引管理

**通过KBX（https://ikbx.luckincoffee.us/）或AWS Kibana：**
1. 左侧菜单选择 "Index Management" > "Indices"
2. 按 **Size** 降序排序，快速定位占用空间大的索引
3. 查看索引命名规则，区分按日/按月生成的索引

### 步骤3：确定清理策略

**触发规则（磁盘空间）：**
- FreeStorageSpace 持续 < 10 GiB（约等价使用率 > 85%），且一周趋势持续下降 → **立即清理**
- 若仅短时波动，可继续观察
- 如出现 `ClusterIndexWritesBlocked`，优先清理

### 步骤4：执行清理操作

**截图记录（重要）：**
- 清理前：FreeStorageSpace 一周趋势、ClusterHealthStatus 截图
- 索引列表截图（包含名称、大小、文档数）
- 记录要删除的具体索引名称列表

**通知方式：企业微信告警群/DBA值班**

**KBX清理操作：**
1. Stack Management → Index Management → Indices
2. 按 Size 排序，识别大容量索引
3. 核对索引日期，确认符合删除条件
4. 选中待删除索引，点击 Manage indices → Delete indices
5. **二次确认**：输入索引名称确认删除
6. **批量操作建议**：每次删除 5-10 个索引，观察集群响应

**监控恢复情况：**
- 等待 ~5-10 分钟
- 重新查看 FreeStorageSpace 是否显著回升（> 10 GiB）
- 确认 ClusterHealthStatus 保持 Green/Yellow
- 验证 ClusterIndexWritesBlocked 解除

### 注意事项

⚠️ **关键提醒：**
- 删除操作**不可恢复**，务必：二次确认索引名称和日期、确保符合保留策略、保存删除前截图
- **按月生成**的日志谨慎删除（通常是重要汇总数据）
- 优先在**业务低峰期（美国时间晚上）**执行
- 保持与团队沟通，避免重复操作


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
