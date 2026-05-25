---
description: "对选中代码或文件进行全面 Code Review，涵盖安全性、性能、代码规范和业务逻辑"
agent: "agent"
tools: [search, codebase]
---

# Code Review

对以下代码进行全面审查，按优先级从高到低依次检查：

## 1. 安全性 (Critical)

- SQL 注入 / ORM 误用（SqlSugar 拼接）
- 未授权访问（缺少身份认证/鉴权检查）
- 敏感信息泄露（硬编码密钥、连接字符串、Token）
- SSRF / 外部输入未校验
- 文件上传路径遍历

## 2. 性能

- 循环内数据库查询 (N+1)
- 缺少分页 / 无限加载风险
- 异步方法阻塞调用 (.Result / .Wait())
- 未释放的 IDisposable / HttpClient 滥用
- 不必要的大对象分配

## 3. 代码规范

- 异步方法是否带 `Async` 后缀
- Controller 是否仅做参数接收/返回包装，逻辑是否在 Service 层
- Service 是否遵循基类继承约定
- API 返回是否使用统一响应包装类
- 配置是否通过 DI 注入而非硬编码
- 未使用的 `using` 引用

## 4. 业务逻辑

- 边界条件处理（null、空集合、超时）
- 错误处理是否充分（catch 后是否有日志/合理返回）
- 并发安全性

## 输出格式

按严重程度分类输出，每个问题包含：
- **位置**：文件名 + 行号
- **级别**：🔴 Critical / 🟠 Major / 🟡 Minor / 💡 Suggestion
- **问题描述**：简洁说明
- **修复建议**：具体代码修改方案

最后给出总体评价和改进优先级建议。
