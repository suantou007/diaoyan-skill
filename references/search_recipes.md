# 搜索配方

默认使用 Tavily 做网页核验。如果本机没有 `tvly`，参考 `tavily-search` skill。

## 基本原则

- 产品事实优先在官方域名下核验
- 当产品名和公司名容易混淆时，不要混着搜
- 二手来源主要用于补充背景，不要把它当作核心产品事实的第一来源
- 始终把“视频里展示了什么”和“网页上确认了什么”分开记录

## 最低核验集合

至少要查：

1. 官方首页
2. 官方 docs / help center
3. 官方定价 / 套餐页（如果相关）
4. 官方 changelog / release notes / blog（当视频中展示了明显新功能时）

## Tavily 查询模式

### 官方站点

```bash
tvly search "\"<product name>\" official site" --max-results 5 --json
```

如果已知官方域名：

```bash
tvly search "\"<product name>\"" --include-domains <official_domain> --max-results 8 --json
```

### 文档 / 帮助中心

```bash
tvly search "\"<product name>\" docs OR help OR documentation" --include-domains <official_domain> --max-results 8 --json
```

### 定价 / 套餐

```bash
tvly search "\"<product name>\" pricing OR plans" --include-domains <official_domain> --max-results 8 --json
```

### 更新日志 / 发布说明

```bash
tvly search "\"<product name>\" changelog OR release notes OR blog" --include-domains <official_domain> --max-results 8 --json
```

### Reddit

```bash
tvly search "site:reddit.com \"<product name>\"" --max-results 8 --json
```

### ProductHunt

```bash
tvly search "site:producthunt.com \"<product name>\"" --max-results 5 --json
```

### G2

```bash
tvly search "site:g2.com \"<product name>\"" --max-results 5 --json
```

### 公司背景

```bash
tvly search "\"<company name>\" founder funding" --max-results 8 --json
```

## 哪些信息要重点确认，哪些要谨慎看待

尽量用官方来源确认：

- 产品名
- 功能名
- 定价
- 套餐限制
- 集成能力
- 平台支持
- 发布时间

以下信息如果没有多方交叉确认，就要谨慎使用：

- 总用户量
- 增长数据
- “AI-powered” 这类营销表述
- 公司自己写的对比结论
