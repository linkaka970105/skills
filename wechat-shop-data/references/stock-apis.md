# Stock APIs

整理微信小店库存相关高频查询接口。

## 统一策略

库存场景优先批量接口，不要默认进入“每个 SKU 调一次单条库存查询”的低效模式。

## 获取库存

- 中文名：获取库存
- 英文名：`getstock`
- 方法：`POST`
- 路径：`/channels/ec/product/stock/get`
- 类型：只读查询
- 用途：查询单个商品单个 SKU 当前库存
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-product/stock/api_getstock

### 适用场景

- 单个 SKU 库存查询
- 精确排查某个商品某个 SKU

## 批量获取库存信息

- 中文名：批量获取库存信息
- 英文名：`batchgetstock`
- 方法：`POST`
- 路径：`/channels/ec/product/stock/batchget`
- 类型：只读查询
- 用途：根据商品 ID 批量获取每个商品下所有 SKU 的库存
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-product/stock/api_batchgetstock

### 请求参数

#### Query

- `access_token`: string，必填

#### Body

- `product_id`: array，必填，上限 50

### 使用建议

- 多商品库存盘点时默认优先使用
- 商品列表场景如果要补库存，不要逐条循环 `getstock`
- 先收集商品 ID，再按最多 50 个商品一批调用

## 获取库存流水

- 中文名：获取库存流水
- 英文名：`getstockflow`
- 方法：`POST`
- 路径：`/channels/ec/product/stock/getflow`
- 类型：只读查询
- 用途：查询指定商品 SKU 在时间范围内的库存流水
- 官方文档：https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-product/stock/api_getstockflow

### 使用建议

- 适合异常排查和库存变动分析
- 时间范围较大时应按时间窗分段拉取
- 这是流水查询，不是静态库存批量查询

## 技能落地规则

- 单 SKU：`getstock`
- 多商品库存：`batchgetstock`
- 库存变动分析：`getstockflow`

如果用户要“一个商品列表对应的库存”，推荐流程是：

1. 先收集商品 ID
2. 再按 50 个商品一批使用 `batchgetstock`

不要推荐对每个商品或每个 SKU 单独重复调用 `getstock`。
