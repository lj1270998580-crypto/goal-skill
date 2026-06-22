# Goal Type Classification & Skill Mapping

Load this file during Stage 1 (Understand) or Stage 2 (Plan) when the goal type is unclear, or when deciding which domain-specific skills to load.

---

## Goal Type Decision Tree

```
User Goal
  │
  ├─ Involves writing code, building an application, or creating software?
  │   ├─ Involves a web interface or browser-based app?
  │   │   ├─ Simple static site or landing page → Type: Webapp (Simple)
  │   │   └─ Interactive app, dashboard, or multi-page site → Type: Webapp (Complex)
  │   ├─ Involves backend/API/service logic?
  │   │   └─ Type: Software Development (Backend)
  │   ├─ Involves a CLI tool or script?
  │   │   └─ Type: Software Development (Script/CLI)
  │   └─ Involves a mobile app or desktop app?
  │       └─ Type: Software Development (Native)
  │
  ├─ Involves creating long-form written content (report, article, analysis)?
  │   ├─ Requires research or data gathering first?
  │   │   ├─ Yes → Type: Research Report (requires deep-research + report-writing)
  │   │   └─ No → Type: Content Creation (requires report-writing)
  │   └─ Is it a creative piece (story, poem, lyrics)?
  │       └─ Type: Creative Writing (requires general-writing)
  │
  ├─ Involves creating slides, a presentation, or visual storytelling?
  │   └─ Type: Presentation (requires pptx-swarm)
  │
  ├─ Involves analyzing data, creating charts, or processing datasets?
  │   ├─ Involves creating a spreadsheet with formulas?
  │   │   └─ Type: Data Analysis (Spreadsheet) (requires xlsx)
  │   └─ Involves visualizing data with charts/graphs?
  │       └─ Type: Data Analysis (Visualization) (requires seaborn-visualization)
  │
  ├─ Involves creating or editing a document (PDF, DOCX, formatted output)?
  │   └─ Type: Document Generation (requires docx or md-to-pdf)
  │
  ├─ Involves comparing, evaluating, or analyzing multiple items/options?
  │   └─ Type: Comparative Analysis
  │
  └─ Does not fit any category above?
      └─ Type: General Task (goal-skill framework only)
```

---

## Goal Type Definitions

### Type: Software Development

**Definition**: Creating code, applications, scripts, APIs, or any executable software.

**Signals**:
- Keywords: "build", "develop", "create an app", "write a script", "implement", "code", "program"
- References to programming languages, frameworks, or libraries.
- Mentions of features, functionality, or user interactions.

**Primary Skill**: `swarm-coding`

**Phases**:
- Stage 1 (Understand): Gather requirements, confirm tech stack, identify features.
- Stage 2 (Plan): Load `swarm-coding`. Decompose into modules/pages/features. Identify worker boundaries.
- Stage 3 (Design): Load `swarm-coding` design phase. Create architecture, API contracts, component boundaries.
- Stage 4 (Execute): Load `swarm-coding` execution phase. Implement code, run tests, build.
- Stage 5 (Verify): Run `swarm-coding` integration checklist + `quality-checklist.md` (Software Development).
- Stage 6 (Deliver): Provide run instructions, document known issues.

**Special Subtypes**:

| Subtype | Key Characteristics | Extra Skill |
|---------|-------------------|-------------|
| Webapp (Simple) | Static site, landing page, portfolio | `swarm-coding` (webapp workflow) |
| Webapp (Complex) | Interactive app, dashboard, multi-page | `swarm-coding` (webapp workflow + multi-agent) |
| Backend/API | Service logic, database, API endpoints | `swarm-coding` (general coding) |
| Script/CLI | Command-line tool, automation script | `swarm-coding` (single-agent) |
| Native App | Mobile or desktop application | `swarm-coding` (general coding) |

---

### Type: Research Report

**Definition**: Creating a professional, well-researched, long-form report or analysis.

**Signals**:
- Keywords: "report", "analysis", "research", "study", "white paper", "brief", "overview"
- Requests for data, statistics, or evidence-based conclusions.
- Mentions of specific industries, markets, or topics requiring factual depth.

**Primary Skills**: `deep-research-swarm` + `report-writing`

**Phases**:
- Stage 1 (Understand): Clarify topic, scope, depth, audience, and format requirements.
- Stage 2 (Plan): Load `report-writing` for outline design. Load `deep-research-swarm` for research.
- Stage 3 (Design): Load `report-writing` outline design phase. Create structured outline with chapters/sections.
- Stage 4 (Execute): Load `deep-research-swarm` for research. Load `report-writing` for content writing.
- Stage 5 (Verify): Run `report-writing` review phase + `quality-checklist.md` (Content Creation + Data Analysis if data-heavy).
- Stage 6 (Deliver): Convert to requested format (default `.docx` via `docx` skill).

**Output Format**:
- Default: `.docx` (use `docx` skill for conversion)
- Intermediate: `.md` files under `{workspace}/`
- Research artifacts: `{workspace}/research/`

---

### Type: Content Creation

**Definition**: Writing prose content without deep research (articles, essays, blog posts, summaries).

**Signals**:
- Keywords: "write", "draft", "create content", "blog post", "article", "essay"
- No mention of data, research, or evidence gathering.
- Focus on narrative, opinion, or explanation.

**Primary Skills**: `report-writing` (for long-form) or `general-writing` (for creative)

**Phases**:
- Stage 1 (Understand): Clarify topic, tone, audience, length, and style.
- Stage 2 (Plan): Outline sections and key points. No research needed.
- Stage 3 (Design): Create content structure and narrative flow.
- Stage 4 (Execute): Write the content section by section.
- Stage 5 (Verify): Run `quality-checklist.md` (Content Creation).
- Stage 6 (Deliver): Deliver in requested format (default `.docx` if not specified).

---

### Type: Presentation

**Definition**: Creating a slide deck or visual presentation.

**Signals**:
- Keywords: "presentation", "slides", "PPT", "PowerPoint", "deck", "pitch"
- Mentions of visual storytelling, slides, or presenting to an audience.

**Primary Skill**: `pptx-swarm` (for 20+ slides) or `pptx` (for <20 slides)

**Phases**:
- Stage 1 (Understand): Clarify topic, audience, number of slides, style, and key messages.
- Stage 2 (Plan): Load `pptx-swarm` or `pptx`. Determine slide count and structure.
- Stage 3 (Design): Load `pptx-swarm` design phase. Create visual design (`design.md`), outline (`outline.md`), and master file.
- Stage 4 (Execute): Load `pptx-swarm` production phase. Generate `.page` files. Assemble final presentation.
- Stage 5 (Verify): Run `quality-checklist.md` (Presentation).
- Stage 6 (Deliver): Deliver `.pptx` file.

**Important**: The main agent handles design and outline. Sub-agents handle `.page` production only. See `pptx-swarm` SKILL.md for detailed rules.

---

### Type: Data Analysis

**Definition**: Processing, analyzing, and visualizing data to produce insights.

**Signals**:
- Keywords: "analyze", "data", "chart", "graph", "visualization", "statistics", "metrics", "dashboard"
- References to datasets, CSV files, Excel files, or data sources.

**Primary Skills**: `seaborn-visualization` + `xlsx` (when spreadsheets are needed)

**Phases**:
- Stage 1 (Understand): Clarify data source, analysis question, output format, and audience.
- Stage 2 (Plan): Identify analysis methods and visualization types. Plan data pipeline.
- Stage 3 (Design): Design data model, analysis pipeline, and visualization plan.
- Stage 4 (Execute): Load `seaborn-visualization` for charts. Load `xlsx` for spreadsheets. Process data and create outputs.
- Stage 5 (Verify): Run `quality-checklist.md` (Data Analysis).
- Stage 6 (Deliver): Deliver charts, spreadsheets, and written insights.

---

### Type: Document Generation

**Definition**: Creating formatted documents (PDF, DOCX, etc.) with specific formatting requirements.

**Signals**:
- Keywords: "document", "PDF", "DOCX", "Word", "formatted", "template"
- Focus on layout, formatting, and document structure rather than content research.

**Primary Skills**: `docx` (for Word documents) or `md-to-pdf` (for PDF conversion)

**Phases**:
- Stage 1 (Understand): Clarify document type, format, template, content, and styling requirements.
- Stage 2 (Plan): Plan document structure, sections, and formatting.
- Stage 3 (Design): Design document layout and styling (if custom).
- Stage 4 (Execute): Load `docx` or `md-to-pdf`. Generate the document.
- Stage 5 (Verify): Run `quality-checklist.md` (Document Generation).
- Stage 6 (Deliver): Deliver the final document file.

---

### Type: Comparative Analysis

**Definition**: Comparing, evaluating, or analyzing multiple options, products, or entities.

**Signals**:
- Keywords: "compare", "versus", "vs", "evaluate", "pros and cons", "which is better", "benchmark"
- Multiple subjects being compared side by side.

**Primary Skill**: None specific; use goal-skill framework with research tools.

**Phases**:
- Stage 1 (Understand): Clarify what is being compared, on what dimensions, and for what purpose.
- Stage 2 (Plan): Identify comparison dimensions and data sources.
- Stage 3 (Design): Design comparison matrix or framework.
- Stage 4 (Execute): Gather data, analyze, and populate comparison.
- Stage 5 (Verify): Check accuracy, completeness, and fairness of comparison.
- Stage 6 (Deliver): Deliver comparison table, analysis, and recommendation.

---

### Type: General Task

**Definition**: Any task that does not fit the above categories.

**Examples**: File organization, batch renaming, data migration, configuration, setup tasks.

**Primary Skill**: None; use goal-skill framework only.

**Phases**: Follow the standard 6-phase framework with minimal domain-specific tooling.

---

## Multi-Type Goals

Some goals span multiple types. Handle them by identifying the **primary type** and treating others as sub-tasks:

**Example 1**: "Build a dashboard that shows sales data and generates a weekly report"
- Primary: Data Analysis (dashboard)
- Sub-task: Content Creation (report)
- Approach: Execute data analysis first, then use the analysis results to write the report.

**Example 2**: "Create a presentation about the research I just did"
- Primary: Presentation
- Sub-task: Content Creation (summarize research into presentation content)
- Approach: Summarize the research into slide content first, then create the presentation.

**Example 3**: "Build a web app that analyzes stock data and generates charts"
- Primary: Software Development (Webapp)
- Sub-task: Data Analysis (stock data + charts)
- Approach: Build the web app framework, then integrate data analysis and visualization.

**Rule**: Always start with the primary type. Execute sub-tasks within the relevant stage, not as separate full cycles.

---

## Skill Loading Reference Table

| Goal Type | Primary Skill | Stage to Load | Notes |
|-----------|--------------|---------------|-------|
| Software Development | `swarm-coding` | Stage 3 | For webapps, use webapp workflow |
| Research Report | `deep-research-swarm` + `report-writing` | Stage 2-3 | Research first, then writing |
| Content Creation | `report-writing` or `general-writing` | Stage 3 | Long-form vs. creative |
| Presentation | `pptx-swarm` or `pptx` | Stage 3 | Main agent handles design |
| Data Analysis | `seaborn-visualization` + `xlsx` | Stage 3-4 | Visualization + spreadsheets |
| Document Generation | `docx` or `md-to-pdf` | Stage 4 | Format-specific |
| General Task | None | N/A | Framework only |

**Progressive loading**: Only load the skill when its stage begins. Do not pre-load all skills at the start. This keeps the context window efficient and follows the progressive disclosure principle.
