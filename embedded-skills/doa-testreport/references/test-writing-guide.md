# E2E 测试编写指南

## 文件组织

```
e2e/
├── login.spec.ts        # 登录认证
├── navigation.spec.ts   # 路由导航
├── dashboard.spec.ts    # 仪表板功能
├── {module}.spec.ts     # 按业务模块
└── helpers/
    └── auth.ts          # 登录辅助函数（可选）
```

## 命名规范

- 文件名：`{功能模块}.spec.ts`（小写 kebab-case）
- `describe` 标题：中文功能模块名（如 `'登录页面'`）
- `test` 标题：中文行为描述（如 `'应显示登录表单'`、`'空表单提交应显示验证提示'`）

## 定位器优先级

按优先级从高到低选择定位器：

1. **`getByRole`** — 按钮、链接、标题等
2. **`getByText`** — 可见文本
3. **`getByPlaceholder`** — 输入框
4. **`getByLabel`** — 表单标签
5. **`page.locator('.class')`** — CSS 选择器（最后手段）

## 登录辅助函数模板

```typescript
async function login(page: import('@playwright/test').Page) {
  await page.goto('/login');
  await page.waitForLoadState('networkidle');
  await page.getByPlaceholder('用户名').fill('{{USERNAME}}');
  await page.getByPlaceholder('密码').fill('{{PASSWORD}}');
  await page.getByRole('button', { name: /登\s*录/ }).click();
  await page.waitForURL('**/dashboard', { timeout: 15000 });
}
```

## 测试用例模板

```typescript
import { test, expect } from '@playwright/test';

test.describe('功能模块名', () => {
  test.beforeEach(async ({ page }) => {
    // 前置条件：导航、登录等
    await page.goto('/target-page');
    await page.waitForLoadState('networkidle');
  });

  test('正向场景描述', async ({ page }) => {
    // Arrange: 准备
    // Act: 操作
    // Assert: 断言
    await expect(page.getByRole('heading', { name: /标题/ })).toBeVisible();
  });

  test('异常场景描述', async ({ page }) => {
    // 错误输入 → 验证提示信息
  });
});
```

## Ant Design 组件选择器速查

| 组件 | 选择器 | 备注 |
|------|--------|------|
| Button | `getByRole('button', { name: /按\s*钮/ })` | 注意文字间可能有空格 |
| Input | `getByPlaceholder('占位文本')` | |
| Message | `page.locator('.ant-message')` | 全局提示 |
| Modal | `page.locator('.ant-modal')` | 弹窗 |
| Table | `page.locator('.ant-table')` | 表格 |
| Result | `page.locator('.ant-result-title')` | 结果页标题 |
| Menu Item | `getByText('菜单文本')` | 侧边栏菜单 |
| Form Error | `getByText('验证提示文案')` | 表单校验 |

## 常见陷阱与解决方案

### 1. Ant Design 按钮文本有空格
```typescript
// ❌ 会失败：实际渲染为 "登 录"
page.getByRole('button', { name: '登录' })

// ✅ 用正则匹配
page.getByRole('button', { name: /登\s*录/ })
```

### 2. 401 拦截器干扰登录测试
如果 axios 全局拦截器对 401 做了重定向，登录接口的 401（密码错误）也会被拦截。
需要在拦截器中排除登录接口：
```typescript
if (originalRequest.url?.includes('/auth/login')) {
  return Promise.reject(error.response?.data || error.message);
}
```

### 3. Strict Mode 多元素匹配
```typescript
// ❌ 可能匹配多个元素
page.getByText('404')

// ✅ 缩小范围到具体组件
page.locator('.ant-result-title').toHaveText('404')
```

### 4. 页面未完全加载
```typescript
// 在 beforeEach 中等待网络空闲
await page.waitForLoadState('networkidle');
```

### 5. 异步路由跳转
```typescript
// 等待 URL 变化，设置合理超时
await page.waitForURL('**/dashboard', { timeout: 15000 });
```
