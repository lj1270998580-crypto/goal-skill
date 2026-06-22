# Quality Checklist Library

Load this file during Stage 5 (Verification) based on the goal type. Run the general checklist first, then the domain-specific checklist.

---

## General Verification Checklist (All Goal Types)

Run this checklist for every goal before running domain-specific checks.

- [ ] **Completeness**: The result covers the user's entire stated goal.
- [ ] **No Omissions**: No critical content, functionality, or requirement is missing.
- [ ] **No Obvious Errors**: No visible errors, defects, or broken functionality.
- [ ] **Format Match**: The output format matches the requested format (e.g., `.docx`, `.pptx`, `.py`, `.md`).
- [ ] **Quality Standard**: The quality meets the minimum deliverable standard for the domain.
- [ ] **Consistency**: All parts of the result are internally consistent (no contradictions).
- [ ] **User Accessibility**: The user can understand and use the result without extra effort.

---

## Software Development Checklist

Use this for code, applications, scripts, APIs, and any software deliverable.

### Functional Verification
- [ ] The code runs without fatal errors (compiles/parses successfully).
- [ ] Core features described in the goal are implemented.
- [ ] Edge cases are handled (e.g., empty input, invalid input, boundary conditions).
- [ ] Error handling is present (not just happy-path logic).

### Structural Verification
- [ ] Code organization follows a clear structure (modules, files, folders).
- [ ] Naming conventions are consistent and meaningful.
- [ ] No obvious code duplication (DRY principle).
- [ ] Dependencies are declared and manageable.

### Quality Verification
- [ ] No obvious security vulnerabilities (e.g., SQL injection, XSS, hardcoded secrets).
- [ ] No critical performance issues (e.g., infinite loops, excessive memory use).
- [ ] Code is readable with appropriate comments where logic is non-obvious.
- [ ] Tests exist and pass (if testing is part of the goal).

### Integration Verification
- [ ] The code integrates with the target environment correctly.
- [ ] Configuration files are correct and complete.
- [ ] Documentation is sufficient for the user to run/use the code.

---

## Content Creation Checklist

Use this for reports, articles, essays, blog posts, and any prose deliverable.

### Structural Verification
- [ ] The content has a clear beginning, middle, and end.
- [ ] Section hierarchy is logical and easy to follow.
- [ ] Transitions between sections are smooth.
- [ ] The conclusion summarizes key points effectively.

### Content Verification
- [ ] The content addresses the stated topic comprehensively.
- [ ] Arguments are supported by evidence, data, or reasoning.
- [ ] No factual inaccuracies are obvious (cross-check key claims when possible).
- [ ] Tone and style match the intended audience and purpose.

### Language Verification
- [ ] No grammatical errors or awkward phrasing.
- [ ] No typos or spelling errors.
- [ ] Sentences are clear and concise (avoid unnecessary complexity).
- [ ] Terminology is consistent throughout.

### Citation Verification (if applicable)
- [ ] Sources are cited where claims are made.
- [ ] Citations are formatted correctly.
- [ ] No fabricated sources or hallucinated data.

---

## Data Analysis Checklist

Use this for data processing, visualization, statistical analysis, and any data-driven deliverable.

### Data Verification
- [ ] Data sources are correctly identified and loaded.
- [ ] Data is clean (no obvious corruption, missing values handled appropriately).
- [ ] Data transformations are correctly applied.
- [ ] No data leakage or bias is obvious in the analysis pipeline.

### Analysis Verification
- [ ] Analysis methods are appropriate for the data and question.
- [ ] Statistical assumptions are valid (or limitations are noted).
- [ ] Results are reproducible (code/logic can be rerun to get the same result).
- [ ] No p-hacking or cherry-picking is obvious.

### Visualization Verification
- [ ] Charts/graphs are clearly labeled (axes, titles, legends).
- [ ] Visual encodings are appropriate for the data type.
- [ ] No misleading visualizations (e.g., truncated axes, inappropriate scales).
- [ ] Colors are accessible and distinguishable.

### Conclusion Verification
- [ ] Conclusions are directly supported by the analysis results.
- [ ] No overgeneralization beyond what the data supports.
- [ ] Limitations of the analysis are acknowledged.
- [ ] Actionable insights are provided if the goal requires them.

---

## Document Generation Checklist

Use this for PDFs, DOCX, PPTX, and any formatted document deliverable.

### Format Verification
- [ ] The document is generated in the correct format.
- [ ] Page layout, margins, and orientation are correct.
- [ ] Typography is consistent and readable.
- [ ] No broken formatting (e.g., orphaned lines, overlapping text).

### Content Verification
- [ ] All required sections are present.
- [ ] Table of contents (if present) matches actual content.
- [ ] Page numbers, headers, and footers are correct.
- [ ] Tables and figures are properly numbered and captioned.

### Visual Verification
- [ ] Images are clear and not pixelated or stretched.
- [ ] Color scheme is consistent and professional.
- [ ] Branding elements (if applicable) are correct.
- [ ] White space is balanced and not cluttered.

---

## Presentation Checklist

Use this for slide decks, presentations, and any visual storytelling deliverable.

### Slide Structure
- [ ] The deck has a clear opening, narrative arc, and conclusion.
- [ ] Each slide has a single main point.
- [ ] Slide order follows a logical flow.
- [ ] No information overload (one idea per slide, when possible).

### Visual Design
- [ ] Visual style is consistent across all slides.
- [ ] Text is readable from a distance (font size, contrast).
- [ ] Images and charts are high-quality and relevant.
- [ ] Animations/transitions are used purposefully, not gratuitously.

### Content Accuracy
- [ ] All data points and claims are accurate.
- [ ] Speaker notes or talking points are provided if needed.
- [ ] The deck works as a standalone document (if applicable).
- [ ] The call-to-action or key takeaway is clear on the final slide.

---

## Webapp / Frontend Checklist

Use this for websites, web applications, dashboards, and any browser-based deliverable.

### Functional Verification
- [ ] The app builds without errors.
- [ ] All intended routes/pages load correctly.
- [ ] Navigation works (links, buttons, routing).
- [ ] Forms and inputs validate and submit correctly.
- [ ] Responsive behavior works on different screen sizes (if applicable).

### Visual Verification
- [ ] UI matches the design specification (if one was created).
- [ ] No visual regressions (broken layouts, missing styles).
- [ ] Interactive elements are clearly identifiable (hover states, focus states).
- [ ] Loading states and empty states are handled gracefully.

### Performance Verification
- [ ] Initial load time is reasonable.
- [ ] No obvious memory leaks or excessive re-renders.
- [ ] Images and assets are optimized.
- [ ] No console errors in the browser.

### Accessibility Verification (if applicable)
- [ ] Color contrast meets WCAG standards (minimum AA).
- [ ] Interactive elements are keyboard-navigable.
- [ ] Images have alt text where appropriate.
- [ ] Semantic HTML is used where possible.

---

## Multi-Agent / Workflow Checklist

Use this when coordinating multiple sub-agents or complex workflows.

### Coordination Verification
- [ ] All sub-agents completed their assigned tasks.
- [ ] No overlapping or conflicting changes between agents.
- [ ] Integration points are resolved and merged correctly.
- [ ] Final validation has been run on the integrated result.

### Communication Verification
- [ ] Each agent received a clear prompt with context, boundaries, and expected output.
- [ ] Agent outputs are in the expected format and location.
- [ ] No context was lost between handoffs.
- [ ] The final result is a coherent combination of all agent outputs.
