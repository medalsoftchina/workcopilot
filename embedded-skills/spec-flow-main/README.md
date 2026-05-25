# Spec-Flow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue.svg)](https://github.com/anthropics/claude-code)

**A Claude Code skill for structured, spec-driven development**

Spec-Flow is an interactive skill for [Claude Code](https://github.com/anthropics/claude-code) that transforms complex feature development into a guided, phase-by-phase workflow with living documentation. Perfect for teams that want systematic planning and clear implementation paths.

## 🌟 Features

- **Phase-by-Phase Workflow**: Breaks down feature development into 4 clear phases (Proposal → Requirements → Design → Tasks)
- **Interactive Confirmation**: Each phase waits for your approval before proceeding
- **Living Documentation**: Creates `.spec-flow/` directory with Markdown documents that guide implementation
- **EARS Requirements**: Uses industry-standard Easy Approach to Requirements Syntax
- **Flexible Execution**: Supports Step, Batch, and Phase execution modes
- **Team Collaboration**: Git-friendly structure for sharing specs across teams

## 📦 Installation

### For Claude Code (Recommended)

This is a **Claude Code skill** that extends Claude's capabilities with structured development workflows.

```bash
# Clone to your Claude Code skills directory
cd ~/.claude/skills
git clone https://github.com/echoVic/spec-flow.git

# Verify installation
ls ~/.claude/skills/spec-flow
```

Once installed, the skill is automatically available in Claude Code. Just say "spec-flow" to activate it!

### For Other Compatible Agents

This skill also works with other AI agents that support the Skills format (Blade, etc.). Install to the appropriate skills directory for your agent.

## 🚀 Quick Start

### 1. Trigger the Workflow

Use any of these phrases to start:
- "spec-flow"
- "spec mode"
- "need a plan"
- "structured development"

### 2. Four-Phase Development

```
┌──────────┐    ┌──────────────┐    ┌────────┐    ┌───────┐
│ Proposal │ -> │ Requirements │ -> │ Design │ -> │ Tasks │
└──────────┘    └──────────────┘    └────────┘    └───────┘
    WHY             WHAT               HOW        EXECUTE
```

#### Phase 1: Proposal
Defines **WHY** this change is needed
- Background and motivation
- Goals and non-goals
- Scope boundaries
- Risk assessment

#### Phase 2: Requirements
Defines **WHAT** the system should do
- Functional requirements (EARS format)
- Non-functional requirements (performance, security, reliability)
- Acceptance criteria

#### Phase 3: Design
Defines **HOW** to implement
- Architecture overview (with Mermaid diagrams)
- Component design and interfaces
- API specifications
- Data models

#### Phase 4: Tasks
Breaks down into **EXECUTABLE** steps
- Granular tasks (1-2 tool calls each)
- Dependency tracking
- Progress monitoring (⏳ Pending → 🔄 In Progress → ✅ Done)

### 3. Implementation

Choose your execution mode:

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Step** (Default) | "start implementation" | Execute one task, wait for confirmation |
| **Batch** | "execute all tasks" | Execute all tasks consecutively |
| **Phase** | "execute setup phase" | Execute all tasks in one phase |

## 📁 Directory Structure

```
your-project/
└── .spec-flow/
    ├── steering/              # Optional: Global project context
    │   ├── constitution.md    # Governance principles
    │   ├── product.md         # Product vision
    │   ├── tech.md            # Tech stack constraints
    │   └── structure.md       # Code organization
    ├── active/                # Work in progress
    │   └── user-auth/
    │       ├── proposal.md
    │       ├── requirements.md
    │       ├── design.md
    │       └── tasks.md
    └── archive/               # Completed features
        └── oauth-login/
            └── ...
```

## 💡 Example Usage

```
User: I need to add user authentication to my app

AI: I'll help you design this feature using spec-flow. Let me start by creating a proposal.

[Creates .spec-flow/active/user-auth/proposal.md]

📋 **Proposal Complete**

Created `.spec-flow/active/user-auth/proposal.md` containing:
- Background: Why we need authentication
- Goals: Security, user management, session handling
- Risks: Security vulnerabilities, performance impact

**Please review**:
1. Is the scope reasonable?
2. Are there any missing risks?

✅ Say "continue" to proceed to Requirements phase
✏️ Tell me what to modify if needed

User: continue

AI: [Creates requirements.md with EARS-formatted requirements]

...
```

## 🌐 Language Support

- **Workflow Instructions**: English (this README, SKILL.md)
- **Generated Documents**: Chinese (中文) - proposal.md, requirements.md, design.md, tasks.md

This is configurable in the skill if you need documents in other languages.

## 📚 Documentation

- **Main Skill File**: [`SKILL.md`](SKILL.md) - Complete workflow guide
- **References**:
  - [`references/ears-format.md`](references/ears-format.md) - EARS requirement syntax
  - [`references/task-decomposition.md`](references/task-decomposition.md) - Task breakdown patterns
  - [`references/workflow.md`](references/workflow.md) - Detailed workflow guide
  - [`references/examples/`](references/examples/) - Real-world examples
- **Templates**: [`templates/`](templates/) - All document templates

## 🛠️ Utilities

### Initialize Spec Directory
```bash
./scripts/init-spec-flow.sh <feature-name>
```

### Validate Spec Completeness
```bash
python3 scripts/validate-spec-flow.py
```

### Execute Task
```bash
./scripts/execute-task.sh <task-id>
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by industry best practices in software specification and requirements engineering
- EARS (Easy Approach to Requirements Syntax) methodology
- Claude Code community

## 📧 Contact

- GitHub: [@echoVic](https://github.com/echoVic)
- Issues: [GitHub Issues](https://github.com/echoVic/spec-flow/issues)

## 🔗 Related Projects

- [Claude Code](https://github.com/anthropics/claude-code) - Official Claude CLI tool
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk) - Build custom Claude agents

---

**Made with ❤️ for better software development workflows**
