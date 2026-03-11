# Order APIs

整理微信小店高频订单查询接口。

## 统一策略

订单查询默认分成两个阶段：

1. 列表或搜索阶段：先拿到 `order_id`
2. 明细补全阶段：按需调用详情接口

不要把“查一个月全部订单”写成普通对话里的串行逐条补全。大任务必须进入批处理模式。

## 获取订单列表

- 中文名：获取订单列表
- 英文名：`getorderlist`
- 方法：`POST`
- 路径：`/channels/ec/order/list/get`
- 类型：只读查询
- 用途：按创建时间、更新时间、订单状态、买家 `openid` 查询订单列表
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-order/api_getorderlist

### 请求参数

#### Query

- `access_token`: string，必填

#### Body

- `create_time_range.start_time`: number，必填，秒级时间戳
- `create_time_range.end_time`: number，必填，秒级时间戳，和开始时间间隔不能超过 7 天
- `update_time_range`: object，可选
- `status`: number，可选
- `openid`: string，可选
- `page_size`: number，可选，不超过 100
- `next_key`: string，可选，翻页上下文

### 返回字段

- `order_id_list`
- `next_key`
- `has_more`

### 使用建议

- 适合批量拉取订单 ID
- 适合后续进入详情补全
- 不适合直接回答“完整订单字段导出”

### 批处理建议

- 月度查询必须按 7 天切片
- 每个时间窗都要翻完 `next_key`
- 汇总后去重 `order_id`
- 命中量大时进入批处理详情模式
- 大批量详情补全前，建议先对 50 到 100 个订单做并发压测，在 20 / 50 / 100 等档位中选最优值；若没有历史数据，首次建议从 50 开始试

## 获取订单详情

- 中文名：获取订单详情
- 英文名：`getorder`
- 方法：`POST`
- 路径：`/channels/ec/order/get`
- 类型：只读查询
- 用途：根据 `order_id` 获取单个订单完整详情
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-order/api_getorder

### 请求参数

#### Query

- `access_token`: string，必填

#### Body

- `order_id`: string，必填

### 返回重点

- 订单基础信息
- 商品明细
- 实收与优惠信息
- 收货与物流信息
- 订单状态
- 售后相关字段

### 使用建议

- 适合查询单笔订单
- 适合对小集合订单做限定补全
- 大批量导出时，应通过分块并发执行，而不是普通串行调用

## 订单搜索

- 中文名：订单搜索
- 英文名：`searchorder`
- 方法：`POST`
- 路径：`/channels/ec/order/search`
- 类型：只读查询
- 用途：按更灵活的条件搜索订单
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-order/api_searchorder

### 请求参数

#### Query

- `access_token`: string，必填

#### Body

- `search_condition`: object，至少包含一个过滤条件
- `on_aftersale_order_exist`: number，可选
- `status`: number，可选
- `page_size`: number，必填，不超过 100
- `next_key`: string，可选

### 使用建议

- 适合模糊条件、售后条件、状态组合筛选
- 搜索结果仍然应视为“ID 收集阶段”或“轻量列表阶段”
- 若用户要完整字段，继续进入 `getorder` 详情补全

## 技能落地规则

- `summary_only`：只返回命中数量、订单 ID、状态、分页
- `detail_on_demand`：仅对小集合订单补详情
- `full_export`：固定走“切片 -> 分页 -> 去重 -> 分块并发详情”
