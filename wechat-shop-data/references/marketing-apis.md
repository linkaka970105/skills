# Marketing APIs

整理赠品与限时抢购相关高频查询接口。

## 统一策略

营销场景分两类：

- 列表已足够回答问题：直接返回列表摘要
- 用户明确要单条完整字段：再补单条详情

## 获取赠品列表

- 中文名：获取赠品列表
- 英文名：`getgiftproductlist`
- 方法：`POST`
- 路径：`/channels/ec/product/gift/list/get`
- 类型：只读查询
- 用途：按状态分页获取赠品列表
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-product/gift/api_getgiftproductlist

### 返回重点

- 赠品 ID 列表
- `next_key`
- 总量信息

### 使用建议

- 这是 ID 收集或轻量列表阶段
- 不要默认把整页赠品都逐条补详情

## 获取赠品详情

- 中文名：获取赠品
- 英文名：`getgiftproduct`
- 方法：`POST`
- 路径：`/channels/ec/product/gift/get`
- 类型：只读查询
- 用途：根据赠品 ID 获取完整详情
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-product/gift/api_getgiftproduct

### 使用建议

- 单赠品查询时直接使用
- 小批量命中结果补全时使用
- 大批量赠品导出时，按固定分块并发策略执行

## 获取限时抢购任务列表

- 中文名：获取限时抢购任务列表
- 英文名：`getlimiteddiscounttasklist`
- 方法：`POST`
- 路径：`/channels/ec/product/limiteddiscounttask/list/get`
- 类型：只读查询
- 用途：分页获取限时抢购任务
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-product/limiteddiscounttask/api_getlimiteddiscounttasklist

### 使用建议

- 通常先直接消费列表结果
- 若未来接入详情接口，再纳入统一“列表 -> 明细补全”模式

## 技能落地规则

- 赠品：`list -> detail`
- 抢购任务：优先列表摘要
- 大批量任务默认先汇总，再决定是否补单条详情
