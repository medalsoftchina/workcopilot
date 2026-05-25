# DOA WorkCopilot — 团队部署脚本
# 将 skill 完整部署到团队成员的环境中
# 用法: 在 PowerShell 中执行此脚本

param(
    [string]$SkillSourcePath,  # 本 skill 目录路径（留空则自动检测）
    [switch]$SkipAgents,       # 跳过用户级 Agent 安装
    [switch]$SkipSkills        # 跳过用户级附属 Skill 安装
)

$ErrorActionPreference = "Stop"

# ─── 1. 定位 skill 源目录 ───
if (-not $SkillSourcePath) {
    $SkillSourcePath = Split-Path -Parent $PSScriptRoot
}

if (-not (Test-Path "$SkillSourcePath\SKILL.md")) {
    Write-Host "❌ 未找到 SKILL.md，请确认路径: $SkillSourcePath" -ForegroundColor Red
    exit 1
}

Write-Host "📦 DOA WorkCopilot 团队部署" -ForegroundColor Cyan
Write-Host "   源目录: $SkillSourcePath" -ForegroundColor Gray
Write-Host ""

# ─── 2. 确定目标目录 ───
$UserHome = $env:USERPROFILE
$ClaudeDir = Join-Path $UserHome ".claude"
$SkillsDir = Join-Path $ClaudeDir "skills"
$AgentsDir = Join-Path $ClaudeDir "agents"
$TargetSkillDir = Join-Path $SkillsDir "doa-workcopilot"

# ─── 3. 安装主 Skill: doa-workcopilot ───
Write-Host "📋 安装主 Skill: doa-workcopilot" -ForegroundColor Yellow

if (Test-Path $TargetSkillDir) {
    Write-Host "   ⚠️ 已存在，将更新..." -ForegroundColor DarkYellow
    Remove-Item -Recurse -Force $TargetSkillDir
}

New-Item -ItemType Directory -Path $TargetSkillDir -Force | Out-Null
Copy-Item -Recurse -Force "$SkillSourcePath\*" $TargetSkillDir

Write-Host "   ✅ Skill 已安装到: $TargetSkillDir" -ForegroundColor Green

# ─── 4. 安装用户级 Agents（从 embedded-agents 复制完整文件） ───
if (-not $SkipAgents) {
    Write-Host ""
    Write-Host "🤖 安装用户级 Agents (6个)" -ForegroundColor Yellow

    if (-not (Test-Path $AgentsDir)) {
        New-Item -ItemType Directory -Path $AgentsDir -Force | Out-Null
    }

    $EmbeddedAgentsDir = Join-Path $SkillSourcePath "embedded-agents"
    if (Test-Path $EmbeddedAgentsDir) {
        Get-ChildItem "$EmbeddedAgentsDir\*.md" | ForEach-Object {
            $targetFile = Join-Path $AgentsDir $_.Name
            if (Test-Path $targetFile) {
                Write-Host "   ⏭️ $($_.BaseName) — 已存在，跳过" -ForegroundColor DarkGray
            } else {
                Copy-Item $_.FullName $targetFile
                Write-Host "   ✅ $($_.BaseName) — 已安装" -ForegroundColor Green
            }
        }
    } else {
        Write-Host "   ⚠️ 未找到 embedded-agents 目录，跳过" -ForegroundColor DarkYellow
    }
}

# ─── 5. 安装用户级附属 Skills（从 embedded-skills 复制） ───
if (-not $SkipSkills) {
    Write-Host ""
    Write-Host "📦 安装用户级附属 Skills (12个)" -ForegroundColor Yellow

    $EmbeddedSkillsDir = Join-Path $SkillSourcePath "embedded-skills"
    if (Test-Path $EmbeddedSkillsDir) {
        Get-ChildItem $EmbeddedSkillsDir -Directory | ForEach-Object {
            $targetSkill = Join-Path $SkillsDir $_.Name
            if (Test-Path $targetSkill) {
                Write-Host "   ⏭️ $($_.Name) — 已存在，跳过" -ForegroundColor DarkGray
            } else {
                Copy-Item -Recurse $_.FullName $targetSkill
                Write-Host "   ✅ $($_.Name) — 已安装" -ForegroundColor Green
            }
        }
    } else {
        Write-Host "   ⚠️ 未找到 embedded-skills 目录，跳过" -ForegroundColor DarkYellow
    }
}

# ─── 6. 提示 Prompts 信息（项目初始化时自动注入） ───
Write-Host ""
Write-Host "📝 Prompts (2个)" -ForegroundColor Yellow

$EmbeddedPromptsDir = Join-Path $SkillSourcePath "embedded-prompts"
if (Test-Path $EmbeddedPromptsDir) {
    $promptFiles = Get-ChildItem "$EmbeddedPromptsDir\*.prompt.md"
    $promptFiles | ForEach-Object {
        Write-Host "   📄 $($_.Name)" -ForegroundColor Gray
    }
    Write-Host "   ℹ️ Prompts 在项目初始化时自动注入到 .github/prompts/" -ForegroundColor DarkGray
} else {
    Write-Host "   ⚠️ 未找到 embedded-prompts 目录" -ForegroundColor DarkYellow
}

# ─── 7. 输出结果 ───
Write-Host ""
Write-Host "─────────────────────────────────────────" -ForegroundColor Cyan
Write-Host "✅ 部署完成！" -ForegroundColor Green
Write-Host ""
Write-Host "已安装:" -ForegroundColor White
Write-Host "  📋 主 Skill:    $TargetSkillDir" -ForegroundColor Gray
if (-not $SkipAgents) {
    Write-Host "  🤖 Agents:      $AgentsDir (6个)" -ForegroundColor Gray
}
if (-not $SkipSkills) {
    Write-Host "  📦 附属 Skills: $SkillsDir (12个)" -ForegroundColor Gray
}
Write-Host "  🔒 Hooks:       embedded-hooks/ (项目初始化时自动注入)" -ForegroundColor Gray
Write-Host "  📝 Prompts:     embedded-prompts/ (项目初始化时注入到 .github/prompts/)" -ForegroundColor Gray
Write-Host ""
Write-Host "使用方式:" -ForegroundColor White
Write-Host '  在 VS Code Copilot Chat 中输入: "workcopilot" 或 "开始新项目"' -ForegroundColor Gray
Write-Host ""
Write-Host "提示:" -ForegroundColor White
Write-Host '  初始化项目时，Agent、Skill、Hook 和 Prompt 会自动注入到项目目录' -ForegroundColor Gray
Write-Host '  项目级 > 用户级，团队可对项目版本做定制化修改' -ForegroundColor Gray
