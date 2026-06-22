# Goal Execution Protocol — 启动协议、状态跟踪与环境探测

加载此文件在 **Stage 1 开始之前**，作为整个执行流程的"引擎启动"步骤。

---

## 1. 启动协议（Startup Protocol）

当此 skill 被触发时（用户描述了一个目标），AI 必须首先执行以下启动序列，**而不是直接跳到阶段 1**。

### 1.1 环境探测（Environment Probe）

在启动任何阶段之前，探测当前执行环境：

```
【探测清单】
- [ ] 当前工作目录已确认（`pwd` 或等效命令）
- [ ] 目录可读写（尝试写入临时文件并读取）
- [ ] 文件系统可用（可以创建文件和目录）
- [ ] 关键工具可用性检查（根据目标类型）：
  - 软件开发：检查 git, node/npm, python, 等
  - 内容创作：检查文本编辑器/文件写入权限
  - 数据分析：检查 python, pandas 等
  - 文档生成：检查 docx/pdf 生成工具
- [ ] 网络连接可用（如果需要外部资源）
- [ ] 磁盘空间充足（预估需求）
```

**探测失败处理**：
- 如果环境不满足目标类型的最低要求 → 立即上报（阶段 1 之前）
- 如果缺少非必需工具 → 记录并继续，在相关阶段尝试 workaround

### 1.2 创建状态文件（State File）

在 `{workspace}/.goal-state.md` 创建状态跟踪文件，格式如下：

```markdown
# Goal Execution State

## Goal Info
- **Started**: [timestamp]
- **Goal Summary**: [1-2 sentence summary of user's goal]
- **Goal Type**: [software | content | data | document | presentation | general]
- **Workspace**: [absolute path]

## Stage Tracker
| Stage | Status | Started | Completed | Retries | Notes |
|-------|--------|---------|-----------|---------|-------|
| 1. Understand | ⬜ Not Started | - | - | 0 | |
| 2. Plan | ⬜ Not Started | - | - | 0 | |
| 3. Design | ⬜ Not Started | - | - | 0 | |
| 4. Execute | ⬜ Not Started | - | - | 0 | |
| 5. Verify | ⬜ Not Started | - | - | 0 | |
| 6. Deliver | ⬜ Not Started | - | - | 0 | |

## Checkpoint Tracker
- [ ] Stage 1 Checkpoint (0/6 passed, 0 retries)
- [ ] Stage 2 Checkpoint (0/6 passed, 0 retries)
- [ ] Stage 3 Checkpoint (0/5 passed, 0 retries)
- [ ] Stage 4 Checkpoint (0/5 passed, 0 retries)
- [ ] Stage 5 Checkpoint (0/5 passed, 0 retries)
- [ ] Stage 6 Checkpoint (0/4 passed, 0 retries)

## Escalation Log
[Empty until first escalation]

## User Feedback
[Empty until user provides mid-execution feedback]

## Artifacts
- [ ] Plan file: `{workspace}/goal-plan.md`
- [ ] Design file: `{workspace}/goal-design.md` (if applicable)
- [ ] Execution log: `{workspace}/goal-execution-log.md`
- [ ] Verification report: `{workspace}/goal-verification-report.md`
- [ ] Deliverables: [list as created]
```

**状态文件更新规则**：
- 进入每个阶段时更新 `Status` 为 `🟡 In Progress`
- 完成阶段时更新 `Status` 为 `✅ Completed` 并记录时间戳
- 检查点每次尝试后更新 `Retries` 和 `Notes`
- 用户反馈或变更记录在 `User Feedback` 区域
- 交付物列表在 `Artifacts` 中维护

### 1.3 复杂度评估（Complexity Assessment）

在启动阶段之前，评估目标的复杂度，决定执行深度：

**轻量路径**（跳过阶段 3 Design，简化检查点）：
- 目标明确且范围小（如"写一个 500 字的总结"）
- 不涉及架构或复杂结构
- 可以在 1-2 步内完成

**标准路径**（完整六阶段）：
- 大多数目标默认走此路径

**深度路径**（增加预研和设计评审）：
- 目标复杂、涉及多个领域
- 需要多 agent 协作
- 用户要求高质量或生产级交付

**复杂度评估输出**：记录到状态文件 `Complexity: [light | standard | deep]`

---

## 2. 状态跟踪机制（State Tracking）

### 2.1 为什么需要状态跟踪

AI 在长时间执行中可能：
- 丢失上下文（对话轮数过多）
- 被用户中断后重启
- 发生工具调用失败导致状态丢失
- 需要向用户展示当前进度

### 2.2 状态文件更新时机

**必须更新状态文件的时刻**：
1. 启动时（创建状态文件）
2. 进入每个阶段时（标记阶段开始）
3. 完成每个阶段时（标记阶段完成，记录时间）
4. 检查点失败并重试时（记录重试次数和原因）
5. 发生上报时（记录上报内容）
6. 用户中途变更目标时（记录变更）
7. 交付完成时（标记所有阶段完成，列出交付物）

### 2.3 状态恢复（State Recovery）

如果执行被中断后恢复（如用户重启对话，AI 重新加载 skill）：

1. 检查 `{workspace}/.goal-state.md` 是否存在
2. 如果存在，读取状态文件，从最后一个未完成的阶段继续
3. 如果不存在，视为新目标，执行完整启动协议

**恢复时的检查**：
- 确认当前工作目录与状态文件中的 `Workspace` 一致
- 如果目录不一致，询问用户是否继续或重新开始
- 检查已创建的中间产物是否仍然存在

---

## 3. 关键决策点用户确认（User Confirmation Gates）

### 3.1 不是只在失败时上报

除了异常上报，在以下**关键决策点**主动请求用户确认：

| 决策点 | 确认内容 | 不确认的处理 |
|--------|----------|-------------|
| 阶段 1 结束后 | 目标理解是否正确？ | 修正理解 |
| 阶段 2 结束后 | 执行计划是否接受？ | 调整计划 |
| 阶段 3 结束后（设计） | 设计方案是否满意？ | 修改设计 |
| 阶段 4 中期（长执行） | 展示进度，确认方向 | 根据反馈调整 |
| 阶段 5 发现重大缺陷 | 告知缺陷，确认修复方案 | 用户选择修复或接受 |

### 3.2 确认消息格式

```
✅ [Stage X] 完成 — 请确认

【当前进度】：阶段 X / 6 完成
【下一步】：进入阶段 Y（[描述]）

【需要您确认的内容】：
  [具体的确认事项，如计划摘要、设计要点等]

请选择：
  ✅ 确认，继续执行
  🔄 需要修改：[请描述修改内容]
  ⏸ 暂停，稍后继续
```

### 3.3 静默执行模式

如果用户明确表示"全自动，不要问我"（如 /goal --auto 或类似模式），则：
- 跳过所有确认点
- 仅在上报阈值触发时停止
- 在阶段 2 生成的计划自动执行，不等待确认

---

## 4. 多轮迭代与回溯机制（Iteration & Backtracking）

### 4.1 为什么需要回溯

六阶段不是严格线性的。实际执行中：
- 阶段 5 验证发现设计问题 → 需要回到阶段 3 修改设计
- 阶段 4 执行发现计划不可行 → 需要回到阶段 2 修改计划
- 用户中途改变目标 → 需要回到阶段 1 重新理解

### 4.2 回溯规则

**允许的回溯**：
- 从阶段 5 回到阶段 3（设计缺陷）
- 从阶段 5 回到阶段 4（实现缺陷）
- 从阶段 4 回到阶段 2（计划不可行）
- 从任何阶段回到阶段 1（用户变更目标）

**不允许的跳过**：
- 不能跳过阶段 1（必须始终理解目标）
- 不能跳过阶段 5（必须验证后才能交付）
- 不能跳过阶段 6（必须正式交付）

**回溯流程**：
1. 记录回溯原因到状态文件
2. 更新状态文件（将目标阶段的 `Status` 重置为 `⬜ Not Started`）
3. 重新执行目标阶段
4. 重新执行所有后续阶段（不能假设之前的结果仍然有效）

### 4.3 最大迭代次数

防止无限循环：
- 同一对阶段之间的回溯最多 3 次（如 5→3 最多 3 次）
- 超过 3 次 → 上报用户，请求决策

---

## 5. 用户目标变更处理（Goal Change Handling）

### 5.1 检测变更

用户可能在执行过程中说：
- "等等，我改主意了，我想..."
- "能不能加上..."
- "其实我不需要..."
- "这个方向不对，换一种方式..."

### 5.2 变更处理流程

1. **识别变更类型**：
   - 小变更（不影响整体架构）：如措辞修改、小功能添加
   - 中变更（影响部分阶段）：如增加一个新模块
   - 大变更（影响整体方向）：如改变目标类型、技术栈

2. **小变更处理**：
   - 在当前阶段直接处理
   - 记录到状态文件 `User Feedback`
   - 继续执行

3. **中变更处理**：
   - 评估影响范围（哪些阶段需要重做）
   - 回到最早受影响的阶段
   - 重新执行该阶段及后续阶段

4. **大变更处理**：
   - 相当于新目标
   - 重置状态文件（或创建新的状态文件）
   - 从阶段 1 重新开始

### 5.3 变更记录格式

```markdown
## User Feedback — [timestamp]

**变更类型**: [minor | medium | major]
**变更内容**: [用户原话或摘要]
**影响范围**: [哪些阶段受影响]
**处理方式**: [在当前阶段处理 / 回到阶段 X / 重新开始]
**执行结果**: [已处理 / 处理中 / 待处理]
```

---

## 6. 执行日志（Execution Log）

在 `{workspace}/goal-execution-log.md` 维护详细执行日志：

```markdown
# Goal Execution Log

## [timestamp] — Stage 1: Understand Started
- 用户目标：...
- 目标类型识别：...
- 关键问题：...
- 用户回答：...

## [timestamp] — Stage 1 Checkpoint
- 检查项：6/6 通过
- 结果：✅ 通过

## [timestamp] — Stage 2: Plan Started
- 技能映射：...
- 子任务列表：...
- 依赖关系：...

## [timestamp] — Stage 2 Checkpoint
- 检查项：5/6 通过（缺少 X）
- 修正：...
- 重试 1：结果 ...
- 结果：✅ 通过

## [timestamp] — Stage 4: Execute — Subtask "X" Failed
- 错误：...
- 根因分析：...
- 重试 1：方案 A → 失败（原因）
- 重试 2：方案 B → 失败（原因）
- 重试 3：方案 C → 失败（原因）
- 决策：上报用户

## [timestamp] — Escalation
- [上报内容]
- 用户回复：...
- 恢复执行：阶段 X
```

**日志规则**：
- 记录所有关键决策、错误、重试、上报
- 用户回复和反馈也要记录
- 日志是故障排查和审计的依据

---

## 7. 元认知检查（Metacognition Checkpoints）

在执行过程中，AI 需要定期"停下来"检查自己：

### 7.1 自我检查时机

- 每个阶段完成时（ checkpoint 之前）
- 每个子任务完成时（长执行中）
- 遇到意外情况时
- 用户长时间无响应时（检查是否偏离目标）

### 7.2 自我检查问题

```
【元认知检查】
- [ ] 我当前做的事情是否仍然服务于用户的原始目标？
- [ ] 我是否偏离了计划？如果是，为什么？
- [ ] 我是否在做一个子任务应该做的事情？（角色检查）
- [ ] 上下文是否被污染？（是否混入了无关信息）
- [ ] 我是否需要重新确认用户的意图？
- [ ] 当前进度是否仍然可控？（是否过于复杂）
```

如果任何一项为"否"或"需要"，则暂停并处理。

---

## 8. 交付物规范（Deliverable Specifications）

### 8.1 交付清单

最终交付应包含：

1. **主要交付物**（用户请求的内容）
   - 文件路径
   - 格式
   - 简要说明

2. **辅助交付物**（根据复杂度决定是否包含）
   - `goal-plan.md` — 执行计划（标准/深度路径）
   - `goal-design.md` — 设计方案（如果有设计阶段）
   - `goal-verification-report.md` — 验证报告
   - `.goal-state.md` — 执行状态（可选，作为审计）

3. **使用说明**（如需要）
   - 如何运行/使用交付物
   - 依赖项和安装步骤
   - 已知限制

4. **后续建议**（可选）
   - 可能的改进方向
   - 扩展功能建议

### 8.2 文件命名规范

- 状态文件：`.goal-state.md`（隐藏文件，避免干扰）
- 计划文件：`goal-plan.md`
- 设计文件：`goal-design.md`
- 执行日志：`goal-execution-log.md`
- 验证报告：`goal-verification-report.md`
- 都放在 `{workspace}` 根目录

---

## 9. 快速启动检查单（Quick Start Checklist）

每次 skill 触发时，按此顺序执行：

- [ ] 探测环境（1.1）
- [ ] 创建/读取状态文件（1.2）
- [ ] 评估复杂度（1.3）
- [ ] 进入阶段 1：理解
- [ ] 阶段 1 检查点 → 确认 → 阶段 2
- [ ] 阶段 2 检查点 → 确认（标准/深度路径）→ 阶段 3
- [ ] ...继续六阶段流程...
