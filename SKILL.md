---
name: goal-skill
description: Universal goal execution framework for systematically completing any task from idea to result, with automatic reflection and up to 6 rounds of evolution for continuous improvement. Use when the user describes a goal, objective, or task to accomplish — such as "build me a todo app", "write a report", "create a presentation", "analyze this data", "develop a feature", "make a website", "optimize my code", or any natural-language request that implies a deliverable outcome. This skill provides a structured 7-phase process (Understand → Plan → Design → Execute → Verify → Deliver → Retrospective → Evolution Loop) with checkpoint gates, quality validation, automatic escalation for unsolvable blockers, and built-in development standards (UI/UX, architecture, code quality, security, performance). Compatible with /goal mode in Claude Code, Codex, and Kimi CLI.
---

# Goal Execution Framework

Systematically execute any user goal through a 6-phase process with mandatory quality checkpoints and automatic escalation for blockers.

> **先执行启动协议**：此 skill 被触发时，**不要直接跳到阶段 1**。首先读取 `references/goal-execution-protocol.md`，执行环境探测、创建状态文件、评估复杂度。然后按六阶段流程执行。

> **工具链适配**：根据当前执行环境（Claude Code / Kimi CLI / Codex / OpenClaw）调整执行策略。读取 `references/tool-adaptation.md` 在环境探测阶段。

> **状态跟踪**：在 `{workspace}/.goal-state.md` 维护执行状态，记录阶段进度、检查点结果、重试次数、上报日志。每次阶段切换时更新此文件。

**Core principle**: Every goal, regardless of domain, follows the same execution pattern — Understand → Plan → Design → Execute → Verify → Deliver. The framework ensures nothing is skipped and every stage meets quality standards before proceeding.

**When other skills exist**: This skill provides the process framework and quality gates. It does not replace domain-specific skills (e.g., `swarm-coding`, `report-writing`, `pptx-swarm`). Instead, it identifies which skills are needed and orchestrates their use within the framework. Load domain skills at the appropriate phase.

**Path**: `{workspace}` is the current working directory. Resolve this placeholder; never hardcode absolute paths.

---

## Workflow Overview

```
User Goal
  │
  ▼
[Stage 1] UNDERSTAND → Checkpoint → ✅ Pass / ❌ Retry(max 3)
  │
  ▼
[Stage 2] PLAN → Checkpoint → ✅ Pass / ❌ Retry(max 3)
  │
  ▼
[Stage 3] DESIGN → Checkpoint → ✅ Pass / ❌ Retry(max 3)  (skip if not needed)
  │
  ▼
[Stage 4] EXECUTE → Checkpoint → ✅ Pass / ❌ Retry(max 3)
  │
  ▼
[Stage 5] VERIFY → Checkpoint → ✅ Pass / ❌ Retry(max 3)
  │
  ▼
[Stage 6] DELIVER → Final Checkpoint → ✅ Deliver
  │
  ▼
[Stage 7] RETROSPECTIVE → 评分 + 改进清单
  │
  ├─ 无改进点 或 质量 >= 25/30 → 结束，归档
  ├─ 有改进点 且 轮次 < 6 → 回到 Stage 3/4（进化）→ 重新交付 → 再次反思
  └─ 有改进点 且 轮次 == 6 → 上报用户，请求决策
```

> **关键机制**：
> - **启动协议**：技能触发后先执行环境探测、创建状态文件、评估复杂度。见 `references/goal-execution-protocol.md` 第 1-3 节。
> - **用户确认**：阶段 1、2、3 结束后主动向用户确认，阶段 4 中期展示进度。见 `references/goal-execution-protocol.md` 第 3 节。
> - **回溯机制**：验证失败可回到设计或执行阶段重新修正，计划不可行可回到规划阶段。见 `references/goal-execution-protocol.md` 第 4 节。
> - **变更处理**：执行中用户可修改目标，小变更直接处理，中/大变更触发回溯。见 `references/goal-execution-protocol.md` 第 5 节。
> - **状态跟踪**：通过 `{workspace}/.goal-state.md` 记录全程进度，支持中断恢复。见 `references/goal-execution-protocol.md` 第 2 节。
> - **进化循环**：阶段 6 交付后自动进入反思（阶段 7），发现改进点后进入第 2-6 轮优化循环。最多 6 轮。见 `references/evolution-loop.md`。
> - **开发标准**：阶段 3 和阶段 4 参考设计/开发标准（UI/UX、架构、代码、安全、性能）。见 `references/development-standards.md`。

**Never skip stages**. Always execute the checkpoint before advancing. If a checkpoint fails 3 retries, escalate to the user with the escalation template.

---

## Stage 1: Understand the Goal

**Purpose**: Convert a vague user description into a clear, actionable goal definition.

**Process**:
1. Extract the core objective from the user's request.
2. Identify the goal type: software development, content creation, data analysis, document generation, or general task.
3. Determine the scope — what is included and what is explicitly excluded.
4. Identify constraints: format, technology stack, quality standards, deadlines.
5. Detect ambiguities, contradictions, or missing critical information.

**Checkpoint Gate** — Run this checklist before proceeding:

- [ ] The core objective is clearly understood.
- [ ] The goal type is identified (software/content/data/document/general).
- [ ] The scope is explicit — included and excluded items are defined.
- [ ] Key constraints are confirmed (format, tech stack, quality bar).
- [ ] No obvious contradictions or infeasible requirements detected.
- [ ] If information is insufficient, clarification questions have been asked.

**On failure**: If any item is unchecked, either ask the user clarifying questions or re-analyze the goal. Retry up to 3 times. On the 3rd failure, escalate.

---

## Stage 2: Plan the Approach

**Purpose**: Create an executable, sequenced plan with identified dependencies and tools.

**Process**:
1. Based on the goal type, select the appropriate execution flow. Read `references/goal-types.md` if the goal type is unclear.
2. Decompose the goal into subtasks with clear outputs.
3. Identify dependencies and execution order (sequential vs. parallel).
4. Identify which domain-specific skills are needed. Load them at the appropriate phase.
5. Assess resource requirements and estimate effort.
6. Present the plan to the user for confirmation if the goal is complex or ambiguous.

**Checkpoint Gate**:

- [ ] The goal is decomposed into executable subtasks.
- [ ] Dependencies and execution order are explicit.
- [ ] Required tools/skills are identified and will be loaded at the right phase.
- [ ] The plan covers the full scope of the user's goal.
- [ ] No critical steps are missing.
- [ ] The plan is presented to the user if confirmation is needed.

**On failure**: Refine the decomposition, add missing steps, or adjust the approach. Retry up to 3 times. Escalate on the 3rd failure.

---

## Stage 3: Design (Conditional)

**Purpose**: Create an architecture or structural design before implementation, when needed.

**When to execute**: Skip only for very small, well-defined tasks where design is trivial. Execute for: software projects, complex content structures, data pipelines, multi-page presentations, and any task where upfront design prevents rework.

**Process**:
1. Create the design artifact appropriate to the goal type:
   - Software: architecture, API contracts, data models, component boundaries.
   - Content: outline, section hierarchy, narrative flow.
   - Data: data model, analysis pipeline, visualization plan.
   - Presentation: slide structure, visual direction, content mapping.
2. Ensure the design satisfies the goal requirements and constraints.
3. Record key design decisions.

**Checkpoint Gate**:

- [ ] The design satisfies the goal requirements.
- [ ] The design follows best practices for the domain.
- [ ] The design considers maintainability and extensibility.
- [ ] Key design decisions are documented.
- [ ] The design has been reviewed for critical flaws.

**On failure**: Redesign, simplify, or supplement the design. Retry up to 3 times. Escalate on the 3rd failure.

---

## Stage 4: Execute

**Purpose**: Execute the plan and produce the actual deliverables.

**Process**:
1. Execute subtasks in the planned order.
2. Track progress and mark completed subtasks.
3. Record key decisions made during execution.
4. Save intermediate artifacts when they are needed for later stages.
5. If a subtask fails, analyze the root cause and retry. If it fails 3 times, treat it as a blocker and escalate.

**When using domain-specific skills** (e.g., `swarm-coding`, `report-writing`):
- Load the skill at the beginning of this stage.
- Follow the skill's workflow within the execution stage.
- The goal-skill's checkpoint gate runs **after** the domain skill's workflow completes, ensuring the overall quality is met.

**Checkpoint Gate**:

- [ ] All planned subtasks are executed.
- [ ] Outputs match the expected results from the plan.
- [ ] Key decisions are recorded.
- [ ] Issues encountered are resolved or escalated.
- [ ] Intermediate artifacts are saved if needed.

**On failure**: Retry the failed subtask with adjusted parameters. If a subtask fails 3 times, escalate rather than retrying indefinitely.

---

## Stage 5: Verify

**Purpose**: Validate the quality, completeness, and correctness of the result before delivery.

**Process**:
1. Run the **General Verification Checklist** (always).
2. Run the **Domain-Specific Checklist** from `references/quality-checklist.md` based on the goal type.
3. Record any defects found.
4. Fix defects and re-verify. Count verification cycles.

**General Verification Checklist** (always run):

- [ ] The result covers the user's entire goal.
- [ ] No critical content or functionality is missing.
- [ ] No obvious errors or defects are present.
- [ ] The output format matches the requested format.
- [ ] The quality meets the deliverable standard.

**Domain-Specific Verification** (read `references/quality-checklist.md` and run the checklist matching the goal type):

- **Software**: code runs, core functions work, structure is readable, no obvious security flaws.
- **Content**: logic is coherent, language is correct, structure is clear, citations are accurate.
- **Data**: data source is correct, analysis method is sound, conclusions are supported, visualizations are clear.
- **Document**: formatting is correct, all sections are complete, layout is clean.

**On failure**: Fix defects and re-verify. Allow up to 3 verification cycles. On the 3rd cycle, if defects remain, escalate to the user with a summary of what was fixed and what remains.

---

## Stage 6: Deliver

**Purpose**: Present the final deliverable to the user with necessary context.

**Process**:
1. Assemble the final deliverable.
2. Provide usage instructions if the deliverable requires them.
3. Document known limitations, caveats, or next steps.
4. Present the result to the user.

**Final Checkpoint Gate**:

- [ ] The deliverable is complete and ready.
- [ ] Usage instructions are provided if needed.
- [ ] Known limitations are documented.
- [ ] The user is informed of the completed work.

**On failure**: If any item is unchecked, do not claim completion. Fix the issue before delivering.

---

## Stage 7: Retrospective & Evolution Loop

**Purpose**: After delivery, systematically reflect on the result and enter an optimization loop if improvements are found. This stage runs **automatically** after Stage 6 delivery is confirmed.

**Trigger**: User confirms receipt of deliverables, or user explicitly requests optimization ("optimize", "fix bugs", "improve").

**Process**:
1. Read `references/evolution-loop.md` for the retrospective methodology.
2. Evaluate 6 dimensions: Functionality, Bugs, UX, Code Quality, Performance, Security.
3. Score each dimension (1-5) and calculate total (max 30).
4. Identify improvement points, prioritize by severity.
5. **If score >= 25/30 and improvements <= 2**: quality is sufficient. End the loop.
6. **If improvements > 0 and current round < 6**: enter evolution round N+1.
   - Generate improvement plan
   - Determine backtrack target (Stage 2/3/4 depending on improvement scope)
   - Reset affected stages in state file
   - Re-execute from backtrack target through Stage 6
   - After re-delivery, run retrospective again
7. **If current round == 6 and improvements remain**: escalate to user with summary.

**Evolution Round Rules**:
- Round 1: Original user goal (mandatory)
- Rounds 2-6: Automatic optimization based on retrospective findings
- Maximum 6 rounds total
- Record each round in `{workspace}/.goal-state.md` Evolution History

**Retrospective Report Format**:
```
📊 Retrospective Report — Round N

| Dimension | Score | Key Findings |
|-----------|-------|--------------|
| Functionality | X/5 | ... |
| Bugs | X/5 | ... |
| UX | X/5 | ... |
| Code Quality | X/5 | ... |
| Performance | X/5 | ... |
| Security | X/5 | ... |
| **Total** | **XX/30** | |

🔧 Improvement Points: N (X high, X medium, X low)
🔄 Decision: [Continue to Round N+1 / End]
```

**Design/Development Standards Reference**:
- During retrospective, reference `references/development-standards.md` for specific evaluation criteria.
- UI/UX evaluation: refer to Section 1 (UI Design Standards)
- Architecture evaluation: refer to Section 2 (Architecture Standards)
- Code quality evaluation: refer to Section 3 (Code Quality Standards)
- Security evaluation: refer to Section 4 (Security Standards)
- Performance evaluation: refer to Section 5 (Performance Standards)

---

**When to escalate** (stop execution and ask the user):

1. Missing critical information that only the user can provide.
2. Environment limitations (missing tools, permissions, access).
3. Technical blockers that cannot be resolved after 3 retry attempts.
4. Goal contradictions or infeasibility detected.
5. Any checkpoint gate fails 3 consecutive retries.

**Escalation message format** (use this template exactly):

```
🛑 Goal Execution Paused — User Assistance Needed

【Current Stage】: [Stage name]
【Problem Description】:
  [Clear, concise description of the blocker]

【Attempts Made】:
  1. [First attempt and result]
  2. [Second attempt and result]
  3. [Third attempt and result]

【Impact】:
  [What parts of the goal are blocked vs. what can still proceed]

【Options for You】:
  A) [Option A description]
  B) [Option B description]
  C) [Provide specific information: ...]

Please choose an option or provide the needed information to continue.
```

**After escalation**: Wait for user input. Do not proceed until the blocker is resolved.

---

## Retry Rules

- **Retry limit**: 3 attempts per checkpoint item or subtask.
- **Retry strategy**: Change the approach on each retry; do not repeat the same failed method.
- **Retry documentation**: Record what was attempted and why it failed before escalating.
- **Partial success**: If some items pass and others fail, retry only the failed items.

---

## Skill Orchestration

This skill coordinates with domain-specific skills. Follow this pattern:

```
Stage 1 (Understand) → goal-skill only
Stage 2 (Plan) → goal-skill only; identify which skills to load
Stage 3 (Design) → goal-skill + domain skill (e.g., report-writing outline design)
Stage 4 (Execute) → domain skill (e.g., swarm-coding coding, report-writing writing)
Stage 5 (Verify) → goal-skill checkpoint + domain skill verification
Stage 6 (Deliver) → goal-skill + domain skill final assembly
```

**Skill loading**: Load domain skills only when their stage begins. Do not pre-load all skills. This keeps the context window efficient.

**Common skill mappings**:

| Goal Type | Primary Skill | Phase to Load |
|-----------|--------------|---------------|
| Software development | `swarm-coding` | Stage 3 |
| Report writing | `report-writing` + `deep-research-swarm` | Stage 2-3 |
| PPT creation | `pptx-swarm` | Stage 3 |
| Data analysis | `seaborn-visualization` + `xlsx` | Stage 3-4 |
| Webapp | `swarm-coding` (webapp workflow) | Stage 3 |

---

## Concurrency and Agent Mapping

When using sub-agents (e.g., in Kimi CLI):

- Use `Agent(subagent_type="plan")` for design, planning, and review tasks.
- Use `Agent(subagent_type="coder")` for implementation, writing, and file assembly tasks.
- Use `Agent(subagent_type="explore")` for research, analysis, and fact-finding tasks.
- The main agent retains responsibility for checkpoint gates, escalation decisions, and final delivery.
- Sub-agents do not inherit context; pass the goal definition, plan, and constraints explicitly in each prompt.

---

## Reference Files

Load these references only when needed during execution:

- `references/phase-operators.md` — **Step-by-step operational guide for each stage. How to run checklists, retry strategies, user interaction handling, cancelation, and metacognition. Load at the beginning of each stage.**
- `references/goal-execution-protocol.md` — **Startup protocol, state tracking, environment probe, user confirmation gates, backtracking, and goal-change handling. Load FIRST, before Stage 1.**
- `references/tool-adaptation.md` — **Cross-toolchain adaptation guide. Load during environment probe to detect the current tool chain and adjust strategy.**
- `references/development-standards.md` — **UI/UX design, architecture patterns, code quality, security, and performance standards. Load during Stage 3 (Design) and Stage 4 (Execute).**
- `references/evolution-loop.md` — **Retrospective methodology, 6-dimension evaluation, and evolution loop rules. Load after Stage 6 (Deliver) for automatic reflection.**
- `references/quality-checklist.md` — Domain-specific verification checklists. Load during Stage 5.
- `references/error-handling.md` — Detailed error handling strategies and recovery patterns. Load when encountering an error that is not resolved by the standard retry protocol.
- `references/goal-types.md` — Goal type classification and skill mapping guide. Load during Stage 1-2 when the goal type is unclear.

---

## Progressive Loading Priority

To avoid context window overflow, follow this loading order. **Never load all references at once.** Only load the file(s) needed for the current phase.

| Execution Phase | Load These Files | Do NOT Load |
|-----------------|------------------|-------------|
| **Skill triggered** | `SKILL.md` only | Any reference files |
| **Startup (before Stage 1)** | `references/goal-execution-protocol.md` + `references/tool-adaptation.md` | `quality-checklist.md`, `goal-types.md` |
| **Stage 1 (Understand)** | `references/phase-operators.md` (Section 2.1) | `error-handling.md` (unless error occurs) |
| **Stage 2 (Plan)** | `references/phase-operators.md` (Section 2.2) + `references/goal-types.md` (if type unclear) | `quality-checklist.md` |
| **Stage 3 (Design)** | `references/phase-operators.md` (Section 2.3) + `references/development-standards.md` (Section 2) + domain skill references | `error-handling.md`, `evolution-loop.md` |
| **Stage 4 (Execute)** | `references/phase-operators.md` (Section 2.4) + `references/development-standards.md` (Sections 3-5) + domain skill references | `quality-checklist.md`, `evolution-loop.md` |
| **Stage 5 (Verify)** | `references/phase-operators.md` (Section 2.5) + `references/quality-checklist.md` | `goal-types.md`, `development-standards.md` |
| **Stage 6 (Deliver)** | `references/phase-operators.md` (Section 2.6) | All other references |
| **Stage 7 (Retrospective)** | `references/evolution-loop.md` + `references/development-standards.md` (for evaluation) | — |
| **On error** | `references/error-handling.md` + `references/phase-operators.md` (Section 3) | — |
| **On user change** | `references/goal-execution-protocol.md` (Section 5) | — |

**Key rule**: If a file is >200 lines, only read the section relevant to the current phase. Use `Read` with `line_offset` to read the specific section.

---

## Automation Scripts

This skill includes helper scripts under `scripts/` for deterministic operations that should not be rewritten each time.

### `scripts/goal_state.py` — State File Manager

A pure-Python (no external dependencies) script for managing the `.goal-state.md` file. Use it instead of manually writing Markdown state updates.

**Commands**:
```bash
# Initialize a new state file
python scripts/goal_state.py init --workspace /path/to/workspace --goal "用户目标描述" --type software

# Update a stage status
python scripts/goal_state.py update-stage --workspace /path/to/workspace --stage 1 --status "🟡 In Progress"
python scripts/goal_state.py update-stage --workspace /path/to/workspace --stage 1 --status "✅ Completed"

# Record checkpoint results
python scripts/goal_state.py checkpoint --workspace /path/to/workspace --stage 2 --passed 5 --total 6 --retries 1

# Read current state
python scripts/goal_state.py read --workspace /path/to/workspace

# Recover from interruption (detects last unfinished stage)
python scripts/goal_state.py recover --workspace /path/to/workspace

# Log an escalation
python scripts/goal_state.py escalate --workspace /path/to/workspace --stage 3 --reason "缺少 API key"

# Record a deliverable
python scripts/goal_state.py deliver --workspace /path/to/workspace --artifact "app.py"

# Append execution log
python scripts/goal_state.py log --workspace /path/to/workspace --message "Stage 4: 完成子任务 3"

# Record user change
python scripts/goal_state.py user-change --workspace /path/to/workspace --change "增加登录功能" --scope minor

# Record retrospective (after Stage 6 delivery)
python scripts/goal_state.py retrospective --workspace /path/to/workspace --round 1 --scores "func=4,bug=3,ux=3,code=4,perf=2,sec=4" --improvements "3"

# Start evolution round N+1 (reset stages and increment round)
python scripts/goal_state.py evolution --workspace /path/to/workspace --round 2 --backtrack-to 4

# View evolution history
python scripts/goal_state.py evolution-history --workspace /path/to/workspace
```

**When to use the script vs. manual file operations**:
- Use the script for: stage updates, checkpoint recording, escalation logging, deliverable tracking
- Use manual `Read`/`Write`/`Edit` for: reading state, making complex edits, recovery analysis

### `scripts/checkpoint_validator.py` — Checkpoint Auto-Validation

A helper script that reads the quality checklist and attempts to auto-detect which items can be verified automatically vs. which require manual review.

**Usage**:
```bash
python scripts/checkpoint_validator.py --workspace /path/to/workspace --stage 5 --type software --goal-dir /path/to/goal-skill
```

**Output**: Lists each checklist item with 🤖 (auto-detectable) or 👤 (manual verification required), plus evidence or reason.

**When to use**: Run during Stage 5 to get a quick assessment of what needs manual verification. Do not rely solely on this script — it only detects, does not fully validate.

---

## Checkpoint Execution Enforcement

To prevent "checklist theater" (where checklists are read but not actually verified), follow these rules for every checkpoint:

### Rule 1: Every checklist item must have evidence

Before marking any item ✅, you MUST be able to answer: **"我怎么知道这一项是对的？"

| Bad (no evidence) | Good (with evidence) |
|-------------------|----------------------|
| "✅ 代码可以运行" | "✅ 代码可以运行 — 运行 `python main.py` 输出 `Hello World` 无错误" |
| "✅ 设计满足需求" | "✅ 设计满足需求 — 对比需求文档，所有 5 个需求点都有对应设计" |
| "✅ 没有遗漏" | "✅ 没有遗漏 — 检查计划中的 8 个子任务，全部有对应输出" |

### Rule 2: Auto-verifiable items MUST be auto-verified

If a checklist item says "code runs" or "file exists", actually run the command or check the file. Do not assume it works without testing.

### Rule 3: Manual judgment items MUST state reasoning

If a checklist item requires judgment (e.g., "quality is good"), state your reasoning explicitly:
- "质量达标 — 内容覆盖了用户要求的全部 3 个要点，结构清晰，无语法错误"
- "设计合理 — 架构分 3 层，各层职责明确，无循环依赖"

### Rule 4: Failed items MUST be recorded with reason

If a checklist item fails ❌, record:
- What failed
- Why it failed
- What will be done to fix it
- When it will be re-verified

### Rule 5: Never skip the checkpoint

Before advancing to any next stage, you MUST have completed the current stage's checkpoint gate. If you are tempted to skip it because "it looks fine", that is exactly when the checkpoint is most needed.

---

## Post-Execution & Evolution Loop Completion

### After Each Round Delivery (Stage 6)

1. Run **Stage 7: Retrospective** automatically (read `references/evolution-loop.md`)
2. Evaluate 6 dimensions, calculate score, identify improvement points
3. Record retrospective results via `goal_state.py retrospective`
4. **Decision point**:
   - Score >= 25/30 and improvements <= 2 → proceed to finalization
   - Improvements > 0 and round < 6 → enter evolution round N+1 via `goal_state.py evolution`
   - Round == 6 and improvements remain → escalate to user

### After Evolution Loop Completes

1. Archive the state file: rename `.goal-state.md` to `.goal-state-{goal-name}-{date}-r{rounds}.md`
2. Preserve execution log: `goal-execution-log.md` is kept for audit
3. Preserve evolution history: `goal-evolution-report.md` (summary of all rounds)
4. Clean up intermediate artifacts if requested by user
5. Final user satisfaction check before closing
