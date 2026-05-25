# tasks.json 模板

**动态生成模式**：支持 N 个子项目，自动检测包管理器，每个子项目独立验证链。

---

## 生成逻辑

```
输入: project.subprojects[]
输出: .vscode/tasks.json

对每个子项目 sub:
  1. 根据 sub.stack 和 sub.verify_chain 生成 task 列表
  2. label 格式: "{sub.name}:{step}"
  3. 每个 task 添加 cwd: "${workspaceFolder}/{sub.path}"
  4. 生成子验证: "verify:{sub.name}" dependsOn 所有步骤

最后:
  生成 "verify" dependsOn 所有 "verify:{sub.name}"
  生成 "verify:harness" 检查 harness 文件完整性
```

## 包管理器检测

| 检测文件 | 包管理器 | 命令前缀 |
|---------|---------|---------|
| `yarn.lock` | Yarn | `yarn` |
| `pnpm-lock.yaml` | pnpm | `pnpm` |
| `package-lock.json` | npm | `npm run` |
| 都不存在 | npm（默认） | `npx` |

## 验证链映射

根据探测到的工具生成验证链，**只生成项目中实际存在的工具步骤**：

### 前端 (Node/TypeScript)

| 探测到的工具 | task label | command | problemMatcher |
|-------------|-----------|---------|---------------|
| prettier | `{sub}:prettier` | `{pm} prettier` | `[]` |
| eslint | `{sub}:lint` | `{pm} lint` 或 `{pm} eslint .` | `["$eslint-stylish"]` |
| biome | `{sub}:lint` | `{pm} biome check .` | `[]` |
| tsc (React/Node) | `{sub}:typecheck` | `{pm_x} tsc --noEmit` | `["$tsc"]` |
| vue-tsc (Vue) | `{sub}:typecheck` | `{pm_x} vue-tsc --noEmit` | `["$tsc"]` |
| build 脚本 | `{sub}:build` | `{pm} build` | `["$tsc"]` |
| vitest | `{sub}:test` | `{pm_x} vitest run` | `[]` |
| jest | `{sub}:test` | `{pm_x} jest` | `[]` |

> `{pm}` = 包管理器命令，`{pm_x}` = 包管理器的 exec 命令（yarn → yarn, npm → npx, pnpm → pnpm exec）

### 后端 (.NET)

| 步骤 | task label | command | problemMatcher |
|------|-----------|---------|---------------|
| format | `{sub}:format` | `dotnet format` | `[]` |
| build | `{sub}:build` | `dotnet build` | `["$msCompile"]` |
| test | `{sub}:test` | `dotnet test` | `[]` |

### 后端 (Python)

| 探测到的工具 | task label | command | problemMatcher |
|-------------|-----------|---------|---------------|
| ruff | `{sub}:lint` | `ruff check .` | `[]` |
| flake8 | `{sub}:lint` | `flake8 .` | `[]` |
| mypy | `{sub}:typecheck` | `mypy src/` | `[]` |
| pytest | `{sub}:test` | `pytest` | `[]` |

### 后端 (Go)

| 步骤 | task label | command | problemMatcher |
|------|-----------|---------|---------------|
| lint | `{sub}:lint` | `golangci-lint run` | `[]` |
| build | `{sub}:build` | `go build ./...` | `[]` |
| test | `{sub}:test` | `go test ./...` | `[]` |

---

## 输出骨架

```json
{
  "version": "2.0.0",
  "tasks": [
    // --- 子项目 A 的 tasks ---
    {
      "label": "{subA}:{step1}",
      "type": "shell",
      "command": "{command}",
      "options": { "cwd": "${workspaceFolder}/{subA.path}" },
      "problemMatcher": ["{matcher}"]
    },
    // ... 更多步骤

    // --- 子项目 B 的 tasks ---
    // ... 同上结构

    // --- 子验证任务 ---
    {
      "label": "verify:{subA}",
      "dependsOn": ["{subA}:{step1}", "{subA}:{step2}", "..."],
      "dependsOrder": "sequence",
      "problemMatcher": []
    },
    {
      "label": "verify:{subB}",
      "dependsOn": ["{subB}:{step1}", "{subB}:{step2}", "..."],
      "dependsOrder": "sequence",
      "problemMatcher": []
    },

    // --- 总验证任务 ---
    {
      "label": "verify",
      "dependsOn": ["verify:{subA}", "verify:{subB}"],
      "problemMatcher": []
    },

    // --- Harness 自检 ---
    {
      "label": "verify:harness",
      "type": "shell",
      "command": "echo Checking harness files... && test -f .github/copilot-instructions.md && test -f .github/AGENTS.md && test -f .vscode/tasks.json && test -d rules/ && echo 'All harness files OK' || echo 'MISSING harness files!'",
      "problemMatcher": []
    }
  ]
}
```

---

## 单项目（非 monorepo）简化

当只有一个子项目时，label 不加前缀：

```json
{
  "label": "lint",       // 而非 "frontend:lint"
  "label": "build",
  "label": "test",
  "label": "verify"
}
```

---

## 增量更新策略

**更新模式下**（`--update`）：
1. 读取已有 `tasks.json`
2. 检测新子项目 → 追加对应 task
3. 更新 `verify` 的 `dependsOn` 列表
4. 已有 task 不覆盖（用户可能调整了命令参数）
