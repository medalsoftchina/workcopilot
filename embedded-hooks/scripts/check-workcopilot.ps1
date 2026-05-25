# check-workcopilot.ps1
# PreToolUse hook: 在 git commit/push、dotnet build/publish、docker build 前
# 检查 .workcopilot 是否已更新，未更新则阻止并提示 agent 先记录会话上下文。

$ErrorActionPreference = "SilentlyContinue"

# 读取 stdin JSON
$inputJson = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($inputJson)) { exit 0 }

$data = $inputJson | ConvertFrom-Json
if (-not $data) { exit 0 }

# 仅拦截 run_in_terminal
$toolName = $data.toolName
if ($toolName -ne "run_in_terminal") { exit 0 }

# 提取命令文本
$command = $data.toolInput.command
if ([string]::IsNullOrWhiteSpace($command)) { exit 0 }

# 匹配目标命令
$patterns = @(
    'git\s+(commit|push)',
    'dotnet\s+(build|publish)',
    'docker\s+build'
)
$matched = $false
foreach ($p in $patterns) {
    if ($command -match $p) { $matched = $true; break }
}
if (-not $matched) { exit 0 }

# 检查 .workcopilot 是否近期已更新（2 分钟内）
$workcopilotPath = Join-Path (Get-Location) ".workcopilot" "changelog.md"
if (Test-Path $workcopilotPath) {
    $lastWrite = (Get-Item $workcopilotPath).LastWriteTime
    $elapsed = (Get-Date) - $lastWrite
    if ($elapsed.TotalMinutes -le 2) {
        # 刚更新过，放行
        exit 0
    }
}

# 阻止并注入提示
$output = @{
    hookSpecificOutput = @{
        hookEventName           = "PreToolUse"
        permissionDecision      = "deny"
        permissionDecisionReason = "请先更新 .workcopilot 再执行此命令。"
    }
    systemMessage = @"
[HOOK] 检测到即将执行提交/构建/打包操作，但 .workcopilot 尚未更新。
请按照 doa-workcopilot 的「会话结束自动持久化」规则，更新以下文件：

1. .workcopilot/state.json   — updatedAt + 迭代记录
2. .workcopilot/changelog.md — 追加本次变更摘要
3. .workcopilot/decisions.md — 如有架构决策则追加
4. .workcopilot/tech-debt.md — 如有技术债变更则更新
5. docs/README.md            — 如有 Docker/版本/技术栈变更则更新

更新完成后，请重新执行原命令。
"@
}

$output | ConvertTo-Json -Depth 5 -Compress
exit 2
