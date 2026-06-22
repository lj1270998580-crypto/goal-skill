# Tool Chain Adaptation — 跨工具链适配指南

加载此文件在 **环境探测阶段**（启动协议 1.1），用于识别当前运行的工具链并调整执行策略。

---

## 1. 支持的执行环境

此 skill 设计为兼容以下工具链：

| 工具链 | 触发方式 | Agent 模型 | 上下文特性 | 特殊能力 |
|--------|----------|-----------|------------|----------|
| **Claude Code** | `/goal` 命令或自然语言 | 单 Agent（Claude） | 长上下文，持续会话 | 工具使用、文件操作、Bash |
| **Kimi CLI** | 自然语言或 `--goal` | 主 Agent + Sub-agents | 中等上下文，分轮次 | 内置 subagent 系统 |
| **Codex** | 自然语言或 `/goal` | 单 Agent | 与 Claude Code 类似 | 工具使用、文件操作 |
| **OpenClaw** | 自然语言 | 单 Agent 或 subagent | 取决于配置 | 工具调用（MCP） |

---

## 2. 环境探测方法

在启动时，探测当前环境的特征：

### 2.1 Claude Code 探测

**特征**：
- 存在 `claude` 命令或 `ANTHROPIC_API_KEY` 环境变量
- 支持 `claude` CLI 工具调用
- 文件系统工具可用（`Read`, `Write`, `Edit`, `Bash`）
- 支持 `Agent` 工具调用（Kimi CLI 风格）或内部 subagent

**探测方式**：
```bash
# 检查 claude 命令
which claude 2>/dev/null || echo "Claude Code not detected"

# 检查环境变量
echo "Claude: ${CLD:-not detected}"
```

### 2.2 Kimi CLI 探测

**特征**：
- 存在 `kimi` 命令或 `KIMI_API_KEY` 环境变量
- 支持 `Agent` 工具调用（`subagent_type` 参数）
- 内置 `explore`, `plan`, `coder` 三种 subagent 类型
- 支持 `PythonRun` 工具

**探测方式**：
```bash
# 检查 kimi 命令
which kimi 2>/dev/null || echo "Kimi CLI not detected"

# 检查 Kimi 环境变量
echo "Kimi: ${KIMI_API_KEY:-not detected}"
```

### 2.3 Codex 探测

**特征**：
- 存在 `codex` 命令或 `OPENAI_API_KEY` 环境变量
- 支持 `codex` CLI 工具调用
- 与 Claude Code 类似的工具集
- 可能没有内置 subagent 系统

**探测方式**：
```bash
# 检查 codex 命令
which codex 2>/dev/null || echo "Codex not detected"

# 检查 OpenAI 环境变量
echo "Codex: ${OPENAI_API_KEY:-not detected}"
```

### 2.4 通用探测（Fallback）

如果无法确定具体工具链，使用通用探测：

```bash
# 检查可用的工具
echo "=== Environment Check ==="
echo "Python: $(python3 --version 2>/dev/null || python --version 2>/dev/null || echo 'not available')"
echo "Node: $(node --version 2>/dev/null || echo 'not available')"
echo "Git: $(git --version 2>/dev/null || echo 'not available')"
echo "Docker: $(docker --version 2>/dev/null || echo 'not available')"
echo "Working Dir: $(pwd)"
echo "Write Test: $(touch .goal-write-test 2>/dev/null && echo 'OK' || echo 'FAIL')"
rm -f .goal-write-test 2>/dev/null
echo "========================"
```

---

## 3. 工具链适配策略

### 3.1 Claude Code 适配

**特点**：
- 单 Agent 执行，没有内置 subagent 分发机制
- 需要手动模拟多阶段流程
- 长上下文，可以容纳较多信息

**适配策略**：

1. **阶段执行**：
   - 每个阶段在对话中明确标记：
   ```
   【Stage 1: Understand】
   ...执行内容...
   【Stage 1 Checkpoint】
   ✅ 全部通过，进入 Stage 2
   ```

2. **状态跟踪**：
   - 由于单 Agent，状态文件尤为重要
   - 每次阶段切换时更新状态文件
   - 用户可以通过查看状态文件了解进度

3. **Subtask 模拟**：
   - 如果没有 subagent，将子任务分解为顺序步骤
   - 在对话中明确标记每个子任务的开始和结束

4. **用户确认**：
   - 在关键决策点明确向用户展示选项
   - 使用清晰的格式让用户容易选择

### 3.2 Kimi CLI 适配

**特点**：
- 内置 `Agent` 工具支持 subagent 分发
- 三种 subagent 类型：`explore`, `plan`, `coder`
- 支持 `PythonRun` 进行代码执行

**适配策略**：

1. **Subagent 使用**（遵循 SKILL.md 中的 Concurrency 部分）：
   - `Agent(subagent_type="plan")`：用于设计、规划、审查任务
   - `Agent(subagent_type="coder")`：用于实现、写作、文件组装任务
   - `Agent(subagent_type="explore")`：用于研究、分析、事实查找任务

2. **主 Agent 职责**：
   - 保留 checkpoint 门控、上报决策和最终交付的责任
   - 不将 checkpoint 门控交给 subagent
   - Sub-agent 只执行分配的任务，不执行跨阶段决策

3. **状态文件同步**：
   - 主 Agent 在 subagent 执行前后更新状态文件
   - Subagent 可以读取状态文件但不修改（避免冲突）

4. **并发控制**：
   - 注意并发限制（通常 ~4 个 subagent 同时运行）
   - 需要分轮次 dispatch subagent 时，按轮次执行

### 3.3 Codex 适配

**特点**：
- 与 Claude Code 类似，单 Agent 执行
- 可能有不同的工具命名或行为

**适配策略**：
- 采用与 Claude Code 相同的策略
- 注意工具名称差异（如 Codex 可能使用不同的文件操作工具名）
- 如果没有内置 subagent，手动模拟多阶段流程

### 3.4 OpenClaw 适配

**特点**：
- 通过 MCP (Model Context Protocol) 工具调用
- 工具集取决于配置的 MCP servers
- 可能没有内置的文件系统工具

**适配策略**：
- 检测可用的 MCP 工具
- 如果缺少文件系统工具，使用 Python 脚本进行文件操作
- 使用 `PythonRun` 执行辅助脚本

---

## 4. 工具链特定的工作流程差异

### 4.1 /goal 模式（Claude Code / Codex）

在 `/goal` 模式下，用户输入一个目标后，AI 应该：

1. **立即进入启动协议**（不等待用户确认）
2. **执行环境探测**
3. **创建状态文件**
4. **进入阶段 1**

**与对话模式的区别**：
- `/goal` 模式：用户说一个目标，AI 自动执行完整流程
- 对话模式：用户可能希望逐步交互，AI 应该在每个阶段后确认

**默认行为**：假设 `/goal` 模式意味着"全自动"，但仍保留关键决策点确认（除非用户明确说"不要问我"）。

### 4.2 Kimi CLI 模式

在 Kimi CLI 中，用户通常期望：
- 可以并行执行多个任务（通过 subagent）
- 主 Agent 负责协调和汇报
- 结果通过文件系统保存

**适配策略**：
- 充分利用 subagent 进行并行子任务执行
- 主 Agent 在状态文件中跟踪所有 subagent 的进度
- 最终汇总和交付由主 Agent 完成

### 4.3 混合模式（Web UI / Chat）

在 Web UI 或聊天界面中，用户可能期望：
- 实时看到进度更新
- 可以随时中断或变更
- 结果直接在对话中展示

**适配策略**：
- 在阶段切换时向用户发送进度更新
- 将中间产物在对话中展示（摘要形式）
- 最终交付物提供下载链接或文件路径

---

## 5. 工具链兼容性矩阵

| 功能 | Claude Code | Kimi CLI | Codex | OpenClaw |
|------|-------------|----------|-------|----------|
| 文件操作 | ✅ 内置 | ✅ 内置 | ✅ 内置 | ⚠️ 需 MCP |
| Bash 执行 | ✅ 内置 | ✅ 内置 | ✅ 内置 | ⚠️ 需 MCP |
| Subagent 分发 | ❌ 无 | ✅ 内置 | ❌ 无 | ❌ 无 |
| Python 执行 | ⚠️ Bash 调用 | ✅ PythonRun | ⚠️ Bash 调用 | ✅ PythonRun |
| 状态文件 | ✅ 文件操作 | ✅ 文件操作 | ✅ 文件操作 | ⚠️ 需文件 MCP |
| 长上下文 | ✅ 支持 | ✅ 支持 | ✅ 支持 | ⚠️ 取决于配置 |
| Web 搜索 | ⚠️ 需工具 | ✅ kimi_search | ⚠️ 需工具 | ⚠️ 需 MCP |

**符号说明**：
- ✅ 原生支持
- ⚠️ 可用但需额外配置或间接调用
- ❌ 不支持

---

## 6. 环境特定注意事项

### 6.1 Claude Code

- **工具命名**：文件操作工具可能叫 `Read`, `Write`, `Edit`（或类似）
- **Subagent**：没有内置 `Agent` 工具，需要手动模拟
- **Context**：上下文窗口较长，可以保留更多历史
- **建议**：在对话中明确标注阶段，依赖状态文件跟踪进度

### 6.2 Kimi CLI

- **工具命名**：文件操作工具叫 `Read`, `Write`, `Edit`
- **Subagent**：有 `Agent` 工具，支持 `subagent_type` 参数
- **PythonRun**：有 `PythonRun` 工具，可以直接执行 Python 代码
- **Context**：注意上下文窗口管理，subagent 不继承上下文
- **建议**：充分利用 subagent 进行并行工作，主 Agent 负责 checkpoint 门控

### 6.3 Codex

- **工具命名**：可能与 Claude Code 类似
- **Subagent**：没有内置 subagent，与 Claude Code 类似
- **建议**：采用与 Claude Code 相同的策略

### 6.4 Windows 环境

- **路径处理**：Windows 路径使用反斜杠，但 Bash 工具可能使用正斜杠
- **Bash 可用性**：Git Bash 可能可用，但原生 Bash 可能不可用
- **PowerShell**：可能需要使用 PowerShell 替代 Bash
- **建议**：优先使用 Python 脚本进行跨平台操作，避免依赖 shell 特定语法

---

## 7. 工具链检测与自动适配流程

```
启动
  │
  ▼
探测环境（运行通用探测脚本）
  │
  ├─ 检测到 Kimi CLI → 使用 Kimi 适配策略
  ├─ 检测到 Claude Code → 使用 Claude 适配策略
  ├─ 检测到 Codex → 使用 Codex 适配策略
  ├─ 检测到 OpenClaw → 使用 OpenClaw 适配策略
  └─ 无法检测 → 使用通用适配策略（假设单 Agent，文件操作可用）
  │
  ▼
记录工具链到状态文件
  │
  ▼
继续执行启动协议的其余部分
```

---

## 8. 通用适配策略（Fallback）

当无法确定具体工具链时，使用以下保守策略：

1. **假设单 Agent 执行**：不依赖 subagent 分发
2. **假设文件操作可用**：通过文件操作进行状态跟踪
3. **假设 Bash 可用**：通过 Bash 执行环境探测和辅助操作
4. **最小化工具依赖**：只使用最基本的文件操作和 Bash 工具

**通用策略的检查清单**：
- [ ] 使用文件操作（Read/Write/Edit）进行状态跟踪
- [ ] 使用 Bash 执行环境探测
- [ ] 使用 Python 脚本（通过 Bash 调用 python）进行复杂操作
- [ ] 在对话中明确标记阶段和进度
- [ ] 不依赖 subagent 分发，手动模拟子任务执行
