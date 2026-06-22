# Development Standards — 开发标准参考

加载此文件在 **阶段 3（设计）** 和 **阶段 4（执行）**，作为设计决策和代码实现的质量参考。

---

## 1. 界面设计标准（UI/UX）

### 1.1 设计原则

**10 条核心原则**（源自 Jakob Nielsen 可用性启发式）：
1. **系统状态可见**：用户始终知道系统正在做什么（加载动画、进度条、状态指示）
2. **现实与系统匹配**：使用用户熟悉的语言和概念，不用技术术语
3. **用户控制与自由**：支持撤销、重做、返回（明显的"返回"按钮、Ctrl+Z）
4. **一致性与标准**：同类型的操作用相同方式完成，遵循平台惯例
5. **错误预防**：在错误发生前阻止（如确认删除、输入验证）
6. **识别而非回忆**：让用户看到选项，而不是记住命令（菜单、工具栏、图标）
7. **使用灵活高效**：新用户简单，高级用户快捷（快捷键、批量操作）
8. **审美与简约**：只展示必要信息，每增加一个元素都需要理由
9. **帮助用户识别/恢复错误**：清晰的错误信息 + 解决方案建议
10. **帮助与文档**：即使有好的设计，也要提供简短的帮助文档

### 1.2 布局标准

**网格系统**：
- 使用 8px 或 4px 基准网格（margin、padding 都是 8 的倍数）
- 主要内容区域宽度：桌面端 1200px 或 1440px，移动端全宽
- 行高：1.5（正文）、1.2（标题）
- 字体大小层级：12px（辅助）、14px（正文）、16px（强调）、20px（小标题）、24px（中标题）、32px（大标题）

**间距规范**：
- 最小可点击区域：44×44px（移动端）
- 按钮间距：8px（紧凑）、16px（标准）、24px（宽松）
- 段落间距：1.5 倍行高或 16px
- 卡片内边距：16px（标准）、24px（宽松）

### 1.3 色彩标准

**色彩原则**：
- 主色：1-2 种（品牌色），用于主要按钮、导航、Logo
- 辅助色：2-3 种，用于次要按钮、标签、图标
- 中性色：黑/白/灰，用于文字、背景、边框
- 功能色：红（错误）、绿（成功）、黄（警告）、蓝（信息）

**对比度要求**：
- 正文与背景：WCAG AA 标准（对比度 >= 4.5:1）
- 大标题与背景：WCAG AA 标准（对比度 >= 3:1）
- 用工具检查：如 WebAIM Contrast Checker

**色彩使用比例**：
- 60% 中性色（背景）
- 30% 辅助色（次要内容）
- 10% 主色（重点、CTA）

### 1.4 字体标准

**字体选择**：
- 中文正文：思源黑体、苹方、微软雅黑（无衬线）
- 英文正文：Inter、Roboto、Open Sans（无衬线）
- 代码：JetBrains Mono、Fira Code、Source Code Pro（等宽）
- 标题可用衬线字体增加优雅感（如 Noto Serif）

**字体层级**：
```
H1: 32px / 粗体 / 行高 1.2
H2: 24px / 粗体 / 行高 1.3
H3: 20px / 半粗体 / 行高 1.4
Body: 14px / 常规 / 行高 1.5 / 字间距 0.02em
Caption: 12px / 常规 / 行高 1.5
Button: 14px / 半粗体 / 大写或常规
```

### 1.5 响应式设计

**断点标准**：
- 移动端：< 768px
- 平板：768px - 1024px
- 桌面：1024px - 1440px
- 大屏：> 1440px

**移动端优先**：
- 先设计移动端，再扩展到大屏
- 触摸目标 >= 44×44px
- 支持手势操作（滑动、捏合）
- 隐藏非核心内容，优先展示关键信息

### 1.6 组件设计标准

**按钮**：
- 主按钮：实心填充，主色，白色文字
- 次要按钮：边框样式，主色边框
- 危险按钮：红色，用于删除/危险操作
- 禁用状态：降低透明度（50%），cursor: not-allowed
- 按钮组：主按钮在右，次按钮在左（阅读方向）

**输入框**：
- 标签在上方或左侧，不在框内（避免输入后消失）
- 占位符文字用浅灰色，不是标签
- 错误状态：红色边框 + 红色错误信息
- 成功状态：绿色边框或勾选图标
- 必填项：红色星号（*）在标签旁

**卡片/面板**：
- 圆角：4px（标准）、8px（现代）、16px（友好）
- 阴影：1px 2px 4px rgba(0,0,0,0.1)（浅）、0 4px 12px rgba(0,0,0,0.15)（中）
- 边框：1px solid #e0e0e0（浅灰色）
- 内边距：16px 或 24px

**导航**：
- 顶部导航：桌面端水平，移动端汉堡菜单
- 面包屑：多级页面时显示，便于回溯
- 侧边导航：适用于管理后台、文档站点
- 当前位置高亮：用主色或粗体表示

### 1.7 Logo 设计标准

**Logo 原则**：
- 简洁：不超过 2-3 个元素
- 可识别：在 16×16px（favicon）到 512×512px 都清晰
- 可单色：黑白打印时也能识别
- 不依赖文字：图形本身能传达品牌
- 独特：不与知名品牌混淆

**Logo 尺寸**：
- Favicon：16×16px, 32×32px
- App Icon：180×180px（iOS）、192×192px（Android）
- 社交媒体：400×400px（圆形或方形）
- 网站 Logo：120×40px（导航栏）、200×80px（页脚）
- 打印：矢量格式（SVG），可任意缩放

**Logo 与品牌色**：
- Logo 主色应与品牌主色一致
- 提供反色版本（深色背景用白色 Logo，浅色背景用彩色 Logo）
- 预留安全边距（Logo 周围最小留白 = Logo 高度的 1/4）

**如果不需要原创 Logo**：
- 使用开源图标库（如 Lucide、Heroicons、Font Awesome）
- 或使用字母缩写 + 几何图形组合
- 或使用工具生成：LogoMakr、Canva、AI 生成工具

---

## 2. 架构设计标准

### 2.1 架构选择决策树

```
项目规模
  │
  ├─ 简单 CRUD / 原型 → 单体应用（Monolith）
  │
  ├─ 中等复杂度 / 多模块 → 模块化单体（Modular Monolith）
  │
  └─ 高复杂度 / 多团队 → 微服务（Microservices）

团队规模
  │
  ├─ 1-3 人 → 单体应用，快速迭代
  │
  ├─ 4-10 人 → 模块化单体，按模块分工
  │
  └─ 10+ 人 → 微服务，按服务分工

技术栈选择
  │
  ├─ 前端：
  │   ├─ 简单静态 → HTML + CSS + JS
  │   ├─ 交互丰富 → React / Vue / Svelte
  │   └─ 全栈 → Next.js / Nuxt.js / SvelteKit
  │
  ├─ 后端：
  │   ├─ 快速开发 → Node.js / Python (FastAPI/Flask)
  │   ├─ 企业级 → Java (Spring Boot) / Go (Gin/Echo)
  │   └─ 高性能 → Go / Rust
  │
  └─ 数据库：
      ├─ 关系型 → PostgreSQL / MySQL
      ├─ 文档型 → MongoDB
      ├─ 缓存 → Redis
      └─ 搜索 → Elasticsearch / Meilisearch
```

### 2.2 推荐架构模式

**前端架构**：

| 模式 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| **MVC**（Model-View-Controller） | 传统 Web 应用 | 结构清晰，分工明确 | 前端复杂时 Controller 臃肿 |
| **MVVM** | 数据驱动 UI（Vue/React） | 双向绑定，响应式 | 数据流可能难以追踪 |
| **Flux/Redux** | 大型应用状态管理 | 单向数据流，可预测 | 样板代码多 |
| **Component-Based** | 现代前端 | 可复用，易测试 | 组件间通信复杂 |
| **Atomic Design** | 设计系统 | 从原子到页面，系统化 | 初期设计成本高 |

**后端架构**：

| 模式 | 适用场景 | 核心思想 |
|------|----------|----------|
| **Layered Architecture** | 大多数 Web 应用 | 分层：Controller → Service → Repository → DB |
| **Clean Architecture** | 复杂业务逻辑 | 依赖向内指向，核心业务独立 |
| **Hexagonal Architecture** | 需要测试/替换适配器 | 端口和适配器，核心业务隔离 |
| **CQRS** | 读多写少，需要优化查询 | 读写分离，各自优化 |
| **Event Sourcing** | 需要审计、时间旅行 | 用事件流代替状态存储 |

**推荐默认选择**：
- 前端：Component-Based + Flux（React + Redux/Zustand 或 Vue + Pinia）
- 后端：Layered Architecture（简单）或 Clean Architecture（复杂）

### 2.3 项目结构标准

**前端项目结构**（以 React 为例）：
```
src/
├── assets/           # 图片、字体、全局样式
├── components/       # 可复用组件（按 Atomic Design 组织）
│   ├── atoms/        # 最小组件（Button, Input, Label）
│   ├── molecules/     # 组合原子（SearchBar, FormField）
│   ├── organisms/     # 复杂组件（Header, ProductCard）
│   └── templates/     # 页面布局模板
├── hooks/            # 自定义 React Hooks
├── pages/            # 页面级组件（路由对应）
├── services/         # API 调用服务
├── store/            # 状态管理（Redux/Pinia）
├── utils/            # 工具函数
├── types/            # TypeScript 类型定义
├── constants/        # 常量配置
└── App.tsx           # 应用入口
```

**后端项目结构**（以 Node.js/Express 为例）：
```
src/
├── config/           # 配置（数据库、环境变量、中间件）
├── controllers/      # 路由控制器（接收请求、返回响应）
├── services/         # 业务逻辑（核心业务规则）
├── repositories/     # 数据访问层（数据库操作）
├── models/           # 数据模型/实体
├── middleware/       # 中间件（认证、日志、错误处理）
├── routes/           # 路由定义
├── utils/            # 工具函数
├── validators/       # 输入验证
├── tests/            # 测试文件
└── app.js            # 应用入口
```

### 2.4 API 设计标准

**RESTful API 原则**：
- 使用 HTTP 方法表达操作：GET（读）、POST（创建）、PUT（全更新）、PATCH（部分更新）、DELETE（删除）
- URL 用名词，不用动词：`/users` 而不是 `/getUsers`
- 使用复数形式：`/users` 而不是 `/user`
- 嵌套资源：`/users/123/orders`
- 过滤、排序、分页用查询参数：`/users?role=admin&sort=created_at&page=1&limit=20`

**响应格式**：
```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功",
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

**错误响应**：
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "输入数据验证失败",
    "details": [
      { "field": "email", "message": "邮箱格式不正确" }
    ]
  }
}
```

**HTTP 状态码**：
- 200 OK：成功
- 201 Created：创建成功
- 400 Bad Request：请求参数错误
- 401 Unauthorized：未认证
- 403 Forbidden：无权限
- 404 Not Found：资源不存在
- 422 Unprocessable Entity：验证失败
- 500 Internal Server Error：服务器错误

### 2.5 数据库设计标准

**命名规范**：
- 表名：复数形式，小写，下划线分隔（`users`, `order_items`）
- 列名：小写，下划线分隔（`created_at`, `first_name`）
- 主键：用 `id`（自增或 UUID）
- 外键：用 `表名_id`（`user_id`）
- 时间戳：必须包含 `created_at` 和 `updated_at`
- 软删除：用 `deleted_at`（NULL 表示未删除）

**索引原则**：
- 主键自动有索引
- 外键必须有索引（加速 JOIN）
- 经常查询的字段加索引
- 不要给所有字段加索引（影响写性能）
- 联合索引注意列的顺序（最左前缀原则）

**数据库设计范式**：
- 至少达到 3NF（第三范式），避免冗余
- 适度反范式：查询性能关键时允许少量冗余
- 用连接表处理多对多关系

---

## 3. 代码质量标准

### 3.1 命名规范

**变量**：
- 用有意义的名称（`userCount` 而不是 `uc`）
- 布尔值用 `is`/`has`/`can` 前缀（`isActive`, `hasPermission`）
- 常量用全大写（`MAX_RETRY_COUNT = 3`）
- 避免单字母命名（循环中的 `i` 可以，但业务逻辑不行）

**函数**：
- 动词开头（`getUser`, `createOrder`, `validateEmail`）
- 只做一件事（函数长度 <= 20 行是理想）
- 参数 <= 3 个，超过用对象（`options`）

**类**：
- 名词（`UserService`, `OrderRepository`）
- 职责单一（一个类只做一类事）

### 3.2 代码结构

**函数设计**：
- 单一职责：一个函数只做一件事
- 纯函数优先：无副作用，相同输入永远返回相同输出
- 早期返回：减少嵌套层级
- 错误处理：用异常或 Result 模式，不要用错误码

**代码注释**：
- 为什么做（Why），不是做什么（What）
- 复杂算法必须注释
- 公共 API 必须文档注释（JSDoc / docstring）
- 不要注释显而易见的代码
- 过时注释比没有注释更糟糕

### 3.3 测试标准

**测试金字塔**：
- 单元测试（70%）：测试单个函数/组件，快速、独立
- 集成测试（20%）：测试模块间交互，涉及数据库/API
- E2E 测试（10%）：测试完整用户流程，慢但真实

**测试原则**：
- 每个功能至少一个测试
- 测试边界条件（空值、最大值、异常输入）
- 测试名称描述行为：`should_return_user_when_id_exists`
- 测试要独立，不依赖其他测试的执行顺序
- 覆盖率 >= 80%（核心业务逻辑 >= 90%）

### 3.4 版本控制（Git）标准

**提交规范**（Conventional Commits）：
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档变更
- `style:` 代码格式（不影响功能）
- `refactor:` 重构（不改功能）
- `test:` 测试相关
- `chore:` 构建、依赖等杂项

**示例**：`feat: add user authentication with JWT`

**分支策略**：
- `main`：生产分支，永远可部署
- `develop`：开发分支，合并功能
- `feature/*`：功能分支，从 develop 切出
- `hotfix/*`：紧急修复，从 main 切出

**提交原则**：
- 每次提交只包含一个逻辑变更
- 提交信息解释"为什么"和"做了什么"
- 不要提交半成品（broken build）

---

## 4. 安全标准

### 4.1 输入验证

- 永远不要信任用户输入
- 服务端验证必须存在（客户端验证只是 UX）
- 使用白名单而非黑名单（只允许已知安全的输入）
- 参数化查询（防止 SQL 注入）
- 转义输出（防止 XSS）

### 4.2 认证与授权

- 使用 JWT 或 Session 认证，不要自己实现加密算法
- 密码用 bcrypt/Argon2 哈希，永远不以明文存储
- 实现 RBAC（基于角色的访问控制）
- API 端点默认拒绝访问，显式授权
- 敏感操作需要二次确认（如删除、转账）

### 4.3 数据安全

- 使用 HTTPS（TLS 1.2+）
- 敏感数据加密存储（AES-256）
- 日志中不要记录敏感信息（密码、token、银行卡号）
- 环境变量存储密钥，不要硬编码
- 定期轮换 API 密钥和数据库密码

### 4.4 常见漏洞清单

- SQL 注入 → 参数化查询
- XSS → 输出转义 + CSP
- CSRF → CSRF Token + SameSite Cookie
- 不安全的反序列化 → 白名单验证
- 敏感数据泄露 → 加密 + 最小权限
- 暴力破解 → 速率限制 + 账户锁定
- 目录遍历 → 输入验证 + 路径规范化

---

## 5. 性能标准

### 5.1 前端性能

**加载性能**：
- 首屏时间 < 3 秒（3G 网络）
- 首字节时间（TTFB）< 600ms
-  Largest Contentful Paint（LCP）< 2.5s
-  Total Blocking Time（TBT）< 200ms
-  Cumulative Layout Shift（CLS）< 0.1

**优化策略**：
- 代码分割（Code Splitting），按路由懒加载
- 图片优化：WebP 格式、响应式图片、懒加载
- 压缩：Gzip/Brotli 压缩资源
- 缓存：Service Worker 缓存、HTTP 缓存策略
- CDN：静态资源放 CDN
- 减少 HTTP 请求：合并 CSS/JS、使用雪碧图

### 5.2 后端性能

**响应时间**：
- API 响应 < 200ms（95th percentile）
- 数据库查询 < 100ms
- 页面渲染 < 500ms

**优化策略**：
- 数据库：索引优化、查询优化、连接池
- 缓存：Redis 缓存热点数据、CDN 缓存静态资源
- 异步处理：消息队列处理非实时任务（邮件、导出）
- 分页：列表接口必须分页，默认 limit=20
- N+1 问题：使用 JOIN 或预加载

### 5.3 性能预算

在项目开始时定义性能预算：
- 首包 JS 大小 < 200KB（gzip）
- 首屏图片总大小 < 1MB
- 第三方脚本 < 3 个
- 字体文件 <= 2 个

---

## 6. 可访问性（Accessibility）标准

### 6.1 基本要求

- 所有图片有 alt 文本
- 所有表单元素有关联的 label
- 所有交互元素可通过键盘操作
- 焦点状态清晰可见（outline 或高亮）
- 颜色不是唯一的信息传递方式（如错误状态同时用图标 + 文字）
- 对比度满足 WCAG AA 标准

### 6.2 ARIA 使用

- 只在语义化 HTML 不足时使用 ARIA
- 不要过度使用 ARIA（如 `role="button"` 在 `<button>` 上多余）
- 动态内容更新使用 `aria-live`
- 模态对话框使用 `aria-modal` 和焦点管理

---

## 7. 开发工具推荐

| 类别 | 工具 | 用途 |
|------|------|------|
| **代码规范** | ESLint + Prettier | JavaScript/TypeScript 格式和规则 |
| **类型安全** | TypeScript | 静态类型检查 |
| **测试** | Jest + React Testing Library | 单元测试 |
| **E2E** | Playwright / Cypress | 端到端测试 |
| **UI 组件** | Storybook | 组件开发和文档 |
| **性能** | Lighthouse | 性能审计 |
| **安全** | npm audit / Snyk | 依赖安全扫描 |
| **CI/CD** | GitHub Actions | 自动化构建和测试 |
| **文档** | Swagger / OpenAPI | API 文档 |
| **设计** | Figma | UI 设计 |
