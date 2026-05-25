# 测试报告 HTML 模板

生成报告时参照以下结构和样式规范。报告主色从项目品牌色提取，默认使用 `#006D75` 色系。

## 报告结构

```
┌─────────────────────────────────────────┐
│  Header（渐变背景）                       │
│  - 项目名 + 副标题                        │
│  - Meta: 执行时间、版本、浏览器、Workers、模式│
├─────────────────────────────────────────┤
│  Summary Cards（4 列网格，叠在 Header 上） │
│  [总用例数] [通过] [失败/跳过] [总耗时]      │
├─────────────────────────────────────────┤
│  Verdict Banner（全通过绿 / 有失败红）      │
├─────────────────────────────────────────┤
│  Progress Bar（通过/失败/跳过比例条）        │
├─────────────────────────────────────────┤
│  测试用例详情                              │
│  ├── Suite Card: {file}.spec.ts           │
│  │   ├── Suite Header (文件名 + 统计)      │
│  │   └── Test Rows (状态 标题 描述 耗时 位置)│
│  └── ...                                  │
├─────────────────────────────────────────┤
│  耗时分布图（水平条形图，按耗时降序）          │
├─────────────────────────────────────────┤
│  执行时间线                                │
├─────────────────────────────────────────┤
│  功能覆盖矩阵                              │
├─────────────────────────────────────────┤
│  运行环境                                  │
├─────────────────────────────────────────┤
│  Footer                                   │
└─────────────────────────────────────────┘
```

## CSS 变量（Design Tokens）

```css
:root {
  --primary: #006D75;           /* 主色 - 根据项目品牌色调整 */
  --primary-light: #E6FFFB;
  --success: #52C41A;
  --success-bg: #F6FFED;
  --error: #FF4D4F;
  --error-bg: #FFF2F0;
  --warning: #FAAD14;
  --warning-bg: #FFFBE6;
  --text: #1F1F1F;
  --text-secondary: #595959;
  --text-tertiary: #8C8C8C;
  --border: #F0F0F0;
  --bg: #FAFAFA;
  --card-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
```

## 关键组件样式要点

### Header
- `background: linear-gradient(135deg, var(--primary) 0%, darken 100%)`
- `padding: 40px 0 80px` — 底部留空给 Summary Cards 上浮
- Meta 区域水平排列，`gap: 32px`

### Summary Cards
- 4 列 `grid`，`margin-top: -48px` 上浮叠在 Header 上
- 白色卡片 + 圆角 12px + 柔和阴影
- 数值 32px 粗体，标签 13px 灰色

### Verdict Banner
- 全通过：`background: linear-gradient(135deg, #F6FFED, #D9F7BE); color: #237804; border: 1px solid #B7EB8F`
- 有失败：`background: linear-gradient(135deg, #FFF2F0, #FFCCC7); color: #A8071A; border: 1px solid #FFA39E`

### Test Row
- 5 列 grid：`32px 1fr auto auto auto`（状态图标 | 标题+描述 | Badge | 耗时 | 位置）
- 状态圆形图标：28px 圆，passed 绿色背景 / failed 红色背景
- Hover 浅灰底色

### Duration Chart
- 水平条形图，填充色 `linear-gradient(90deg, #006D75, #13C2C2)`
- 宽度百分比 = 当前耗时 / 最大耗时 × 100%
- 左侧标签 260px，右侧时间 50px

### PDF 兼容
- 使用纯 CSS，无 JavaScript 依赖
- 字体使用系统字体栈（`-apple-system, 'PingFang SC', 'Microsoft YaHei'`）
- 避免 `position: fixed`（PDF 不支持）
- 渐变和圆角在 PDF 中需要 `printBackground: true`

## 数据映射（JSON → HTML）

从 Playwright JSON Reporter 输出中提取：

```
stats.expected        → 通过数
stats.unexpected      → 失败数
stats.skipped         → 跳过数
stats.flaky           → Flaky 数
stats.duration        → 总耗时（ms）
stats.startTime       → 开始时间
config.version        → Playwright 版本
config.metadata.actualWorkers → Worker 数

suites[].title        → 测试文件名
suites[].suites[].title → describe 标题
suites[].suites[].specs[].title → 用例标题
suites[].suites[].specs[].tests[].results[].status   → passed/failed
suites[].suites[].specs[].tests[].results[].duration  → 耗时（ms）
suites[].suites[].specs[].tests[].results[].startTime → 开始时间
suites[].suites[].specs[].line   → 源码行号
```

## PDF 转换命令

```javascript
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ channel: '{{CHANNEL}}' });
  const page = await browser.newPage();
  await page.goto('file:///{{ABSOLUTE_PATH}}/detailed-report.html', {
    waitUntil: 'networkidle'
  });
  await page.pdf({
    path: '{{OUTPUT_DIR}}/E2E测试报告.pdf',
    format: 'A4',
    printBackground: true,
    margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' }
  });
  await browser.close();
})();
```
