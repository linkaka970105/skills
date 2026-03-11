# Product APIs

整理微信小店高频商品查询接口。

## 统一策略

商品场景默认分成两个阶段：

1. 列表阶段：先拿 `product_id`
2. 明细阶段：按需调用 `getproduct`

不要把商品列表查询默认写成全量逐条详情补拉。

## 获取商品列表

- 中文名：获取商品列表
- 英文名：`getproductlist`
- 方法：`POST`
- 路径：`/channels/ec/product/list/get`
- 类型：只读查询
- 用途：按状态分页获取商品 ID 列表
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-product/shop/api_getproductlist

### 请求参数

#### Query

- `access_token`: string，必填

#### Body

- `status`: number，可选
- `page_size`: number，必填，不超过 30
- `next_key`: string，可选

### 返回字段

- `product_ids`
- `next_key`
- `total_num`

### 使用建议

- 适合分页拿商品 ID
- 适合盘点商品池、在售商品、指定状态商品
- 不适合直接回答完整商品详情问题

## 获取商品详情

- 中文名：获取商品
- 英文名：`getproduct`
- 方法：`POST`
- 路径：`/channels/ec/product/get`
- 类型：只读查询
- 用途：根据 `product_id` 获取单个商品详情
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-product/shop/api_getproduct

### 请求参数

#### Query

- `access_token`: string，必填

#### Body

- `product_id`: string，必填
- `data_type`: number，可选，默认 `1`

### 返回重点

- 商品标题
- 图片
- 类目
- 属性
- SKU 信息
- 线上与草稿数据

### 使用建议

- 单商品查看时直接使用
- 小批量命中结果补全时使用
- 大规模商品导出时，走固定分块并发策略

## 技能落地规则

- `summary_only`：返回商品 ID、数量、状态、分页
- `detail_on_demand`：对小集合 `product_id` 补详情
- `full_export`：先收集全部 `product_id`，再分块补详情
