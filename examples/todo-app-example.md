# 完整示例：开发一个待办应用

这是一个"做一个待办应用"目标的完整 7 阶段执行示例，展示 goal-skill 的实际执行方式。

---

## 用户输入

```
帮我开发一个简单的待办应用，前端用 React，后端用 Node.js + Express，数据存在内存中就行。
```

---

## 阶段 0：启动

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 0 开始】启动
  目标：探测环境、创建状态文件、识别目标类型
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

### 执行步骤：

1. `Bash: pwd` → 输出：`/home/user/projects/todo-app`
2. `Bash: python scripts/goal_state.py init --workspace . --goal "开发一个待办应用（React + Node.js/Express）" --type software`
3. `Bash: python --version && node --version && git --version`
   → 输出：`Python 3.12.0`, `Node v20.0.0`, `git 2.43.0`
4. `Read: references/goal-types.md` → 识别为 **软件开发（Webapp 全栈）**

### 展示给用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 0 结束】启动
  检查点：3/3 项通过
  ✅ 进入阶段 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

环境探测结果：
- 工作目录：/home/user/projects/todo-app
- Python：3.12.0 ✅
- Node.js：20.0.0 ✅
- Git：2.43.0 ✅
- 目标类型：软件开发（Webapp 全栈）
```

---

## 阶段 1：理解目标

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 1 开始】理解目标
  目标：将用户描述转化为清晰、可执行的目标定义
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

### 执行步骤：

1. **提取目标**：
   > "开发一个待办应用，用户可以添加、查看、标记完成、删除待办事项。"

2. **识别隐含需求**：
   - 用户没说要"编辑"待办，但这是常见功能
   - 用户没说要"过滤"（全部/进行中/已完成），但这是基础功能
   - 用户说"数据存在内存中"→ 不需要数据库，但需要重启后数据丢失的说明

3. **确认范围**：
   - **包含**：CRUD 操作、前端界面、后端 API、数据存储（内存）
   - **不包含**：用户认证、数据库持久化、部署、测试

4. **确认约束**：
   - 技术栈：React + Node.js/Express
   - 数据存储：内存（JavaScript 对象/数组）
   - 质量标准：基础可用即可，不要求生产级

5. **提出澄清问题**：
   > "需要支持编辑已有待办吗？需要过滤功能（全部/进行中/已完成）吗？"
   
   用户回答："都需要，谢谢提醒。"

6. **记录状态**：
   `Bash: python scripts/goal_state.py update-stage --workspace . --stage 1 --status "✅ Completed"`

### 展示给用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 1 结束】理解目标
  检查点：4/4 项通过
  ✅ 进入阶段 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

目标总结：
开发一个待办应用，用户可以添加、查看、编辑、标记完成、删除、过滤待办事项。

范围：
✅ 包含：CRUD 操作、前端界面、后端 API、数据存储（内存）
❌ 不包含：用户认证、数据库持久化、部署、测试

约束：
- 技术栈：React + Node.js/Express
- 数据存储：内存（重启后数据丢失）
- 质量标准：基础可用

澄清问题已确认：
✅ 支持编辑待办
✅ 支持过滤（全部/进行中/已完成）
```

---

## 阶段 2：规划

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 2 开始】规划
  目标：将目标分解为可执行的子任务，生成计划文档
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

### 执行步骤：

1. **分解任务**：
   - 子任务 1：初始化后端项目（Express + CORS）
   - 子任务 2：实现后端 API（GET/POST/PUT/DELETE /todos）
   - 子任务 3：初始化前端项目（React + Vite）
   - 子任务 4：实现前端 UI（列表、表单、按钮）
   - 子任务 5：实现前端状态管理（useState + API 调用）
   - 子任务 6：实现过滤功能（全部/进行中/已完成）

2. **确定依赖顺序**：
   - 串行：子任务 1 → 子任务 2（后端必须先有）
   - 串行：子任务 3 → 子任务 4 → 子任务 5 → 子任务 6（前端依赖顺序）
   - 后端和前端可以并行启动，但前端 API 调用依赖后端完成

3. **识别所需技能**：
   - 需要 `swarm-coding`（已内置，不需要额外加载）

4. **生成计划文件**：
   `Write: goal-plan.md`

5. **用户确认**：
   > "计划：分 6 个子任务，先建后端 API，再建前端 UI。预计需要 X 步。确认吗？"
   
   用户回答："确认。"

6. **记录状态**：
   `Bash: python scripts/goal_state.py update-stage --workspace . --stage 2 --status "✅ Completed"`

### 展示给用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 2 结束】规划
  检查点：5/5 项通过
  ✅ 进入阶段 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

子任务列表（6 个）：
1. 初始化后端项目（Express + CORS）
2. 实现后端 API（GET/POST/PUT/DELETE /todos）
3. 初始化前端项目（React + Vite）
4. 实现前端 UI（列表、表单、按钮）
5. 实现前端状态管理（useState + API 调用）
6. 实现过滤功能（全部/进行中/已完成）

依赖关系：
后端：1 → 2
前端：3 → 4 → 5 → 6

计划文件已创建：goal-plan.md

用户已确认 ✅
```

---

## 阶段 3：设计

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 3 开始】设计
  目标：创建架构和 API 设计方案
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

### 执行步骤：

1. **加载设计标准**：
   `Read: references/development-standards.md`（架构章节 + API 设计章节）

2. **创建设计文档**：`Write: goal-design.md`

   内容：
   ```markdown
   # 待办应用设计文档

   ## 架构
   - 前端：React + Vite，单页应用
   - 后端：Node.js + Express，REST API
   - 数据：内存存储（JavaScript Map/Array）

   ## API 设计
   - GET /todos → 获取所有待办
   - POST /todos → 创建待办 { text, completed }
   - PUT /todos/:id → 更新待办 { text, completed }
   - DELETE /todos/:id → 删除待办

   ## 数据模型
   ```typescript
   interface Todo {
     id: string;
     text: string;
     completed: boolean;
     createdAt: number;
   }
   ```

   ## 前端组件结构
   - App：主容器
   - TodoList：待办列表
   - TodoItem：单个待办项
   - TodoForm：添加/编辑表单
   - FilterBar：过滤按钮组
   ```

3. **设计自检**：
   - 覆盖需求：添加 ✅、查看 ✅、编辑 ✅、标记完成 ✅、删除 ✅、过滤 ✅
   - 遵循标准：RESTful API ✅、组件化 ✅

4. **记录状态**：
   `Bash: python scripts/goal_state.py update-stage --workspace . --stage 3 --status "✅ Completed"`

### 展示给用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 3 结束】设计
  检查点：4/4 项通过
  ✅ 进入阶段 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

设计摘要：
- 架构：React + Vite 前端 + Express 后端
- API：4 个 REST 端点（GET/POST/PUT/DELETE）
- 数据模型：Todo { id, text, completed, createdAt }
- 组件：App, TodoList, TodoItem, TodoForm, FilterBar

设计文档已创建：goal-design.md

自检：覆盖全部 6 个需求点 ✅
```

---

## 阶段 4：执行

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 4 开始】执行
  目标：按计划执行子任务，产生实际输出
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

### 执行子任务（逐个展示）：

**子任务 1：初始化后端项目**
- `Bash: mkdir backend && cd backend && npm init -y && npm install express cors`
- `Write: backend/server.js`
- 展示给用户："后端项目初始化完成，Express + CORS 已安装"

**子任务 2：实现后端 API**
- `Write: backend/server.js`（完整 API 实现）
- `Bash: cd backend && node server.js` → 测试 API
- 展示给用户："后端 API 已实现，4 个端点可用。测试：POST /todos → 返回 { id: '1', text: '测试' }"

**子任务 3：初始化前端项目**
- `Bash: npx create-vite@latest frontend --template react && cd frontend && npm install`
- 展示给用户："前端项目初始化完成，React + Vite"

**子任务 4：实现前端 UI**
- `Write: frontend/src/components/TodoList.jsx`
- `Write: frontend/src/components/TodoItem.jsx`
- `Write: frontend/src/components/TodoForm.jsx`
- 展示给用户："UI 组件已实现，包含列表、单项、表单"

**子任务 5：实现前端状态管理**
- `Write: frontend/src/App.jsx`（整合 API 调用）
- `Bash: cd frontend && npm run dev` → 启动开发服务器
- 展示给用户："状态管理已连接，前端可以调用后端 API"

**子任务 6：实现过滤功能**
- `Edit: frontend/src/App.jsx`（添加过滤逻辑）
- `Write: frontend/src/components/FilterBar.jsx`
- 展示给用户："过滤功能已添加：全部 / 进行中 / 已完成"

**记录状态**：
`Bash: python scripts/goal_state.py update-stage --workspace . --stage 4 --status "✅ Completed"`

### 展示给用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 4 结束】执行
  检查点：4/4 项通过
  ✅ 进入阶段 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

执行完成：6/6 子任务

生成的文件：
- backend/server.js
- backend/package.json
- frontend/src/App.jsx
- frontend/src/components/TodoList.jsx
- frontend/src/components/TodoItem.jsx
- frontend/src/components/TodoForm.jsx
- frontend/src/components/FilterBar.jsx
- frontend/src/main.jsx
- frontend/index.html
- frontend/package.json

关键决策：
- 使用内存存储（Map 存储 todos，重启后数据丢失）
- 使用 UUID 作为 id（避免自增 ID 冲突）
- 前端使用 fetch 调用 API（不引入 axios 减少依赖）
```

---

## 阶段 5：验证

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 5 开始】验证
  目标：验证结果质量和完整性
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

### 执行验证：

1. **加载检查清单**：`Read: references/quality-checklist.md`（通用 + 软件开发）

2. **逐项验证**（展示给用户每项结果）：

| 检查项 | 验证方法 | 结果 | 证据 |
|--------|----------|------|------|
| 代码可运行 | `Bash: cd backend && node server.js &` → 测试 curl | ✅ | 服务器在 3000 端口启动，curl 返回 JSON |
| 核心功能实现 | 手动测试：添加、查看、编辑、完成、删除、过滤 | ✅ | 6 个功能全部可用 |
| 代码结构清晰 | 检查文件组织 | ✅ | 组件分离到单独文件 |
| 无安全漏洞 | 检查输入验证 | ⚠️ | 缺少输入验证（内存应用，风险低） |
| 格式正确 | 检查文件扩展名 | ✅ | .jsx, .js, .json 正确 |

3. **修复缺陷**：
   - 发现缺少输入验证 → 添加 `validator` 中间件
   - 展示给用户："已修复：添加输入验证，防止空文本提交"

4. **生成验证报告**：`Write: goal-verification-report.md`

5. **记录状态**：`Bash: python scripts/goal_state.py update-stage --workspace . --stage 5 --status "✅ Completed"`

### 展示给用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 5 结束】验证
  检查点：5/5 项通过
  ✅ 进入阶段 6
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

验证结果：
| 检查项 | 结果 | 证据 |
|--------|------|------|
| 代码可运行 | ✅ | 服务器启动，API 返回正确 |
| 核心功能实现 | ✅ | 6 个功能全部可用 |
| 代码结构清晰 | ✅ | 组件分离到单独文件 |
| 无安全漏洞 | ✅ | 已添加输入验证 |
| 格式正确 | ✅ | 文件类型正确 |

修复：1 项（添加输入验证）
验证报告：goal-verification-report.md
```

---

## 阶段 6：交付

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 6 开始】交付
  目标：将最终成果呈现给用户
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

### 执行交付：

1. **组装交付物**：
   - backend/server.js
   - frontend/src/**/*
   - goal-plan.md
   - goal-design.md
   - goal-verification-report.md

2. **使用说明**：
   - 步骤 1：进入 backend 目录，运行 `npm install && node server.js`
   - 步骤 2：进入 frontend 目录，运行 `npm install && npm run dev`
   - 步骤 3：浏览器打开 http://localhost:5173

3. **已知限制**：
   - 数据存储在内存中，重启后丢失
   - 没有用户认证，所有用户共享同一份数据
   - 没有持久化数据库
   - 没有生产环境部署配置

4. **正式交付**：展示文件路径

5. **记录状态**：`Bash: python scripts/goal_state.py update-stage --workspace . --stage 6 --status "✅ Completed"`

### 展示给用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 6 结束】交付
  检查点：4/4 项通过
  ✅ 目标完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 交付完成！

文件位置：
- 后端：backend/server.js
- 前端：frontend/src/
- 计划：goal-plan.md
- 设计：goal-design.md
- 验证：goal-verification-report.md

使用说明：
1. 后端：cd backend && npm install && node server.js
2. 前端：cd frontend && npm install && npm run dev
3. 浏览器：打开 http://localhost:5173

已知限制：
- 数据存储在内存中，重启后丢失
- 没有用户认证
- 没有持久化数据库
- 没有生产环境部署配置

是否需要进一步优化？（回复"优化"进入反思阶段）
```

---

## 如果用户说"优化"

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 7 开始】反思
  目标：评估交付质量，发现改进点
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

### 执行反思：

1. `Read: references/evolution-loop.md`

2. **6 维度评估**：

| 维度 | 评分 | 发现 |
|------|------|------|
| 功能完整性 | 4/5 | 缺少批量删除、拖拽排序 |
| Bug 与缺陷 | 4/5 | 输入验证已添加，但 XSS 过滤未做 |
| 用户体验 | 3/5 | 没有加载动画、空状态提示 |
| 架构与代码质量 | 4/5 | 组件分离清晰，但缺少错误处理 |
| 性能 | 4/5 | 内存存储性能 OK，但无缓存策略 |
| 安全与稳定性 | 3/5 | 缺少错误处理、缺少 XSS 过滤 |
| **总分** | **22/30** | |

3. **改进清单**：
   - [高] 添加错误处理（API 失败时的 UI 反馈）
   - [高] 添加空状态提示（无待办时的友好提示）
   - [中] 添加加载动画
   - [中] 添加 XSS 过滤
   - [低] 添加批量删除

4. **决策**：总分 22/30 < 25，改进点 5 个 > 2 → 进入第 2 轮优化

5. **记录状态**：`Bash: python scripts/goal_state.py retrospective --workspace . --round 1 --scores "func=4,bug=4,ux=3,code=4,perf=4,sec=3" --improvements "5"`

6. **进入第 2 轮**：回到阶段 3（设计），针对改进点修改设计，然后重新执行阶段 4-6。

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  【阶段 7 结束】反思
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

---

## 总结

这个示例展示了 goal-skill 的完整执行流程：

1. 每个阶段有明确的开始/结束标记
2. 每个步骤有具体执行动作（不是模糊描述）
3. 每个阶段有展示给用户的输出内容
4. 检查点有具体验证方法（不是自我判定）
5. 状态文件在每个阶段切换时更新
6. 反思阶段有 6 维评估和具体改进清单

**关键原则**：绝不走形式，每个阶段都有可验证的输出。
