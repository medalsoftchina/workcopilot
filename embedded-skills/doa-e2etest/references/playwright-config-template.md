# Playwright 配置模板

根据项目实际情况填充以下模板。

## 模板

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  // 测试目录
  testDir: './e2e',

  // 超时配置
  timeout: 30000,

  // 失败重试次数（CI 中建议设为 1-2）
  retries: 0,

  // 浏览器配置
  use: {
    // 前端开发服务器地址
    baseURL: '{{BASE_URL}}',   // 如 'http://localhost:5173'

    // 浏览器通道
    // 优先 'chromium'，网络受限时用 'msedge'（Windows）或 'chrome'（macOS）
    channel: '{{CHANNEL}}',

    // 无头模式
    headless: true,

    // 仅失败时截图
    screenshot: 'only-on-failure',
  },

  // 自动启动前端服务（可选）
  webServer: {
    command: '{{DEV_COMMAND}}',  // 如 'npm run dev'
    port: {{PORT}},              // 如 5173
    reuseExistingServer: true,   // 已有服务时复用
  },
});
```

## 占位符说明

| 占位符 | 说明 | 常见值 |
|-------|------|-------|
| `{{BASE_URL}}` | 前端服务地址 | `http://localhost:5173`（Vite）、`http://localhost:3000`（CRA/Next.js） |
| `{{CHANNEL}}` | 浏览器通道 | `chromium`、`msedge`、`chrome` |
| `{{DEV_COMMAND}}` | 启动命令 | `npm run dev`、`npm start`、`npx next dev` |
| `{{PORT}}` | 端口号 | `5173`、`3000`、`3001`、`8080` |

## 浏览器选择决策

```
可以下载 Chromium？
  ├── 是 → channel: 不设置（默认 chromium）
  └── 否 → Windows？
        ├── 是 → channel: 'msedge'
        └── 否 → channel: 'chrome'
```
