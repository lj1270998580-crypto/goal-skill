# goal-skill 🎯

**从想法到结果的通用目标执行框架**

**Universal Goal Execution Framework — from idea to result**

---

告别"看起来可以"就交付。goal-skill 为 Claude Code、Codex、Kimi CLI 等 AI 工具提供了一套结构化、可审计、可进化的 **7 阶段任务流程**，确保每个交付物都经过完整质量控制。

Say goodbye to "looks fine" delivery. goal-skill provides a structured, auditable, and evolvable **7-phase framework** for Claude Code, Codex, Kimi CLI, and beyond.

---

## 🚀 核心特性 / Core Features

- **7 阶段流程** — 理解 → 规划 → 设计 → 执行 → 验证 → 交付 → 反思
- **强制质量检查点** — 每个阶段检查清单，未通过绝不进入下一阶段
- **自动上报机制** — 遇到无法解决的阻塞，3 次重试后自动上报用户
- **进化循环** — 交付后自动从 6 维度评估，最多 6 轮自我优化
- **内置开发标准** — UI/UX 设计、架构模式、代码质量、安全、性能
- **跨工具兼容** — Claude Code /goal、Codex、Kimi CLI 通用

---

## 📋 流程图 / Workflow

```
User Goal
  │
  ▼
[Stage 1] 理解目标 → 检查点 → ✅ 通过
  │
  ▼
[Stage 2] 规划方案 → 检查点 → ✅ 通过
  │
  ▼
[Stage 3] 设计方案 → 检查点 → ✅ 通过
  │
  ▼
[Stage 4] 执行实现 → 检查点 → ✅ 通过
  │
  ▼
[Stage 5] 验证质量 → 检查点 → ✅ 通过
  │
  ▼
[Stage 6] 交付结果 → 检查点 → ✅ 通过
  │
  ▼
[Stage 7] 反思评估 → 评分 + 改进清单
  │
  ├─ 无改进点 → 结束
  └─ 有改进点 → 进化循环 → 回到阶段 3/4（最多 6 轮）
```

---

## 📁 文件结构 / File Structure

```
goal-skill/
├── SKILL.md                              # 核心框架（7 阶段流程 + 检查点 + 上报机制）
├── README.md                             # 本文件
├── references/
│   ├── goal-execution-protocol.md        # 启动协议、状态跟踪、环境探测、用户确认、回溯
│   ├── tool-adaptation.md                 # 跨工具链适配（Claude Code / Kimi / Codex / OpenClaw）
│   ├── phase-operators.md                # 每个阶段的具体操作步骤
│   ├── development-standards.md           # UI/UX、架构、代码、安全、性能标准
│   ├── evolution-loop.md                  # 反思方法论、6维评估、进化循环
│   ├── quality-checklist.md              # 7 类目标的质量检查清单
│   ├── error-handling.md                 # 错误分类、上报模板、恢复策略
│   └── goal-types.md                      # 目标类型识别 + 技能映射表
└── scripts/
    ├── goal_state.py                      # 状态文件管理（纯 Python，无依赖）
    └── checkpoint_validator.py            # 检查点自动验证（纯 Python，无依赖）
```

---

## 🛠️ 使用方法 / Usage

### 1. 安装 / Installation

将 `goal-skill` 目录复制到你的技能目录：

```bash
# Claude Code
mkdir -p ~/.claude/skills
cp -r goal-skill ~/.claude/skills/

# Kimi CLI
mkdir -p ~/.kimi/skills
cp -r goal-skill ~/.kimi/skills/

# Codex
mkdir -p ~/.codex/skills
cp -r goal-skill ~/.codex/skills/
```

### 2. 触发 / Trigger

描述一个目标，skill 自动触发：

```
/goal 帮我开发一个待办应用
```

或自然语言：

```
> 帮我做一个AI行业研究报告
```

### 3. 进化循环 / Evolution Loop

交付后，goal-skill 自动进入反思阶段：

- **6 维度评估**：功能、Bug、体验、架构、性能、安全
- **评分**：每维度 1-5 分，总分 30 分
- **决策**：
  - ≥ 25/30 且改进点 ≤ 2 → 结束
  - 有改进点且轮次 < 6 → 进入第 N+1 轮优化
  - 轮次 == 6 仍有改进点 → 上报用户决策

---

## 🏗️ 内置开发标准 / Built-in Standards

| 标准 | 覆盖内容 |
|------|----------|
| **UI/UX** | 10 条可用性原则、网格系统、色彩、字体、响应式、组件规范、Logo 设计 |
| **架构** | 架构选择决策树、MVC/MVVM/Flux/Clean Architecture、项目结构、API 设计、数据库标准 |
| **代码质量** | 命名规范、函数设计、测试金字塔、Git 提交规范（Conventional Commits） |
| **安全** | 输入验证、认证授权、数据加密、常见漏洞清单（SQL 注入/XSS/CSRF 等） |
| **性能** | 前端指标（LCP/TBT/CLS）、后端指标（API/DB 响应时间）、性能预算 |

---

## 🔧 工具兼容 / Tool Compatibility

| 工具 | 触发方式 | 支持级别 |
|------|----------|----------|
| Claude Code | `/goal` 命令 | ✅ 完全支持 |
| Kimi CLI | 自然语言 | ✅ 完全支持 |
| Codex | `/goal` 或自然语言 | ✅ 完全支持 |
| OpenClaw | 自然语言 | ✅ 完全支持 |

---

## 📊 质量检查点 / Checkpoint Gates

每个阶段结束时，必须完成以下检查：

| 阶段 | 检查项数 | 失败处理 |
|------|----------|----------|
| 1. 理解 | 6 项 | 提问澄清 |
| 2. 规划 | 6 项 | 重规划 |
| 3. 设计 | 5 项 | 重设计 |
| 4. 执行 | 5 项 | 重试（最多 3 次） |
| 5. 验证 | 通用 5 + 领域专项 | 修复重验（最多 3 轮） |
| 6. 交付 | 4 项 | 补充完善 |

---

## 🔄 进化循环 / Evolution Loop

```
Round 1: 用户原始目标 → 交付 → 反思
Round 2: 自动优化（修复反思发现的问题）→ 交付 → 反思
Round 3: 自动优化 → 交付 → 反思
...
Round 6: 最终轮 → 交付 → 反思 → 如有改进点，上报用户
```

**结束条件**：
- 评分 ≥ 25/30 且改进点 ≤ 2
- 完成 6 轮
- 用户明确停止
- 连续 2 轮改进点相同（收益递减）

---

## 📜 许可证 / License

MIT License — 自由使用、修改和分发。

---

**🎯 让 AI 不再"看起来可以"，而是真正可靠。**

**Stop "looks fine" delivery. Make AI truly reliable.**
