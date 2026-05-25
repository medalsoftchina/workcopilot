---
description: "为选中代码生成 xUnit + Moq 单元测试，覆盖正常流程、边界条件和异常场景"
agent: "agent"
argument-hint: "选中要测试的类或方法"
tools: [search, codebase]
---

# 生成单元测试

为提供的代码生成全面的单元测试。

## 技术栈

- 框架：xUnit
- Mock：Moq
- 断言：FluentAssertions（如项目已引用）或 xUnit Assert
- .NET 8 / C# 12

## 测试策略

### 必须覆盖

1. **正常路径 (Happy Path)**：标准输入产生预期输出
2. **边界条件**：null 参数、空集合、最大/最小值、空字符串
3. **异常场景**：外部依赖失败（HTTP 超时、数据库异常）、权限不足
4. **业务规则**：关键业务逻辑的各种分支

### Mock 原则

- Mock 所有外部依赖：`ISqlSugarClient`、`IHttpClientFactory`、`ILogger<T>`、`IOptions<T>`
- 使用 `MockHttpMessageHandler` 模拟 HTTP 调用
- 对于基类依赖，通过构造函数注入 Mock

## 命名规范

```
方法名_场景描述_期望结果
```

示例：`GetAccessTokenAsync_WhenApiReturnsSuccess_ReturnsAccessToken`

## 输出格式

```csharp
using Moq;
using Xunit;
using FluentAssertions;

namespace MyProject.Tests.模块名;

public class 类名Tests
{
    private readonly Mock<依赖> _mock依赖;
    private readonly 被测类 _sut;

    public 类名Tests()
    {
        // Arrange: 初始化 Mock 和 SUT
    }

    [Fact]
    public async Task 方法名_场景_期望()
    {
        // Arrange
        // Act
        // Assert
    }

    [Theory]
    [InlineData(...)]
    public async Task 方法名_多组输入_期望(参数)
    {
        // 参数化测试
    }
}
```

## 注意事项

- 每个测试方法只验证一个行为
- 避免测试实现细节，测试行为和结果
- 对异步方法使用 `async Task` 而非 `async void`
- 测试类放在与源码对应的命名空间下（`MyProject.Tests.模块名`）
