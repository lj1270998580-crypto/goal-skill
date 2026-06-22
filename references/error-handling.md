# Error Handling & Escalation Protocol

Load this file when the standard retry protocol (3 retries) fails to resolve an issue, or when an unexpected error occurs that requires strategic decision-making.

---

## Error Classification Matrix

Classify every error into one of these categories before deciding the response.

| Category | Definition | Example | Response |
|----------|-----------|---------|----------|
| **Information Gap** | Missing information that only the user can provide | "What API key should I use?" | Escalate immediately |
| **Environment Limit** | Tool/permission/resource not available in the current environment | "No write access to /usr/local" | Attempt workaround → Escalate if no workaround |
| **Technical Blocker** | A technical problem that cannot be solved within 3 attempts | "Dependency conflict that breaks build" | Attempt 3 workarounds → Escalate on failure |
| **Goal Conflict** | The user's goal contains contradictions or is infeasible | "Build a real-time app with no server" | Escalate immediately |
| **External Dependency** | Failure caused by an external service, API, or resource | "Third-party API returns 500" | Retry with backoff → Escalate if persistent |
| **Timeout** | Operation takes too long or hangs | "Build process hangs indefinitely" | Kill and retry → Escalate on 3rd failure |
| **Ambiguity** | Goal is too vague to produce a meaningful result | "Make it better" | Ask clarifying questions |

---

## Escalation Decision Tree

```
Error Occurred
    │
    ├─ Is it an Information Gap? → ESCALATE immediately
    │
    ├─ Is it a Goal Conflict? → ESCALATE immediately
    │
    ├─ Is it an Ambiguity? → Ask clarifying questions (no escalation needed)
    │
    ├─ Is it an Environment Limit?
    │   ├─ Can a workaround be found? → Try workaround
    │   └─ No workaround → ESCALATE
    │
    ├─ Is it an External Dependency?
    │   ├─ Retry with exponential backoff (1s, 2s, 4s)
    │   └─ Still failing after 3 retries → ESCALATE
    │
    ├─ Is it a Technical Blocker?
    │   ├─ Attempt 3 different approaches
    │   └─ All fail → ESCALATE
    │
    └─ Is it a Timeout?
        ├─ Kill process, retry with different strategy
        └─ 3rd timeout → ESCALATE
```

---

## Escalation Message Template

Use this exact template when escalating to the user. Fill in every section.

```
🛑 Goal Execution Paused — User Assistance Needed

【Current Stage】: [Stage 1/2/3/4/5/6 — Understand/Plan/Design/Execute/Verify/Deliver]
【Error Category】: [Information Gap / Environment Limit / Technical Blocker / Goal Conflict / External Dependency / Timeout]

【Problem Description】:
  [1-2 sentences describing the blocker clearly and specifically]

【Attempts Made】:
  1. [First attempt: what was tried, what was the result]
  2. [Second attempt: what was tried, what was the result]
  3. [Third attempt: what was tried, what was the result]
  [If fewer than 3 attempts, explain why fewer were sufficient]

【Impact Assessment】:
  - Blocked: [What parts of the goal cannot proceed]
  - Unaffected: [What parts of the goal can still proceed or are already complete]
  - Risk: [What happens if this blocker is not resolved]

【Options for You】:
  A) [Option A: description of what the user can do]
  B) [Option B: description of an alternative approach]
  C) [Option C: what information the user needs to provide]

【Recommendation】:
  [State the preferred option and why]

Please choose an option or provide the needed information to continue.
```

---

## Recovery Patterns

### Pattern 1: Fallback Strategy

When the primary approach fails, have a fallback ready:

1. **Primary approach fails** → Log the failure reason.
2. **Switch to fallback** → Use a simpler, more robust alternative.
3. **Document the fallback** → Note that the fallback was used and why.

**Example**: Primary — use a complex library API. Fallback — use a simpler, standard library approach.

### Pattern 2: Partial Delivery

When the full goal is blocked, deliver what is possible:

1. **Identify blocked vs. unblocked parts**.
2. **Deliver unblocked parts** with a note about what is missing.
3. **Escalate only the blocked parts**.

**Example**: Goal is to build a full app with authentication. Authentication is blocked → deliver the app without auth, escalate auth as a separate issue.

### Pattern 3: Scope Reduction

When the full goal is too complex, propose a reduced scope:

1. **Identify the minimum viable subset** of the goal.
2. **Deliver the MVP** first.
3. **Propose the remaining scope** as a follow-up task.

**Example**: Goal is to build a full CRM. Reduce to a simple contact list first, then propose adding CRM features.

### Pattern 4: Environment Workaround

When the environment is limiting:

1. **Identify the missing tool/resource**.
2. **Check if an alternative exists** in the environment.
3. **If no alternative exists**, document the environment requirement and escalate.

**Example**: Goal requires `docker` but it's not installed. Check if `podman` exists. If not, document that Docker is needed and escalate.

---

## Retry Strategy Guide

### When to Retry

- **Transient errors**: network timeouts, temporary unavailability → retry with backoff.
- **Incorrect parameters**: the approach was wrong but fixable → retry with corrected parameters.
- **Partial failure**: some parts worked, others didn't → retry only the failed parts.

### When NOT to Retry

- **Persistent errors**: same error after 3 attempts → escalate.
- **Fundamental limitations**: the approach is fundamentally flawed → try a different approach (counts as new attempt).
- **User-side issues**: missing information, permission denied → escalate.

### Retry Counter Rules

- **Counter scope**: Each subtask or checkpoint item has its own retry counter.
- **Counter reset**: When switching to a fundamentally different approach, reset the counter (but document that a new approach was tried).
- **Counter max**: Never exceed 3 retries for the same subtask or approach.

---

## Common Error Scenarios

### Scenario 1: Build Fails

```
Error: npm run build fails with compilation errors
Category: Technical Blocker
Response:
  1. Read the error message carefully. Fix the specific compilation error.
  2. If error is unclear, run build with verbose output. Analyze.
  3. If still unclear, try a clean build (delete node_modules, reinstall, rebuild).
  4. If all fail → ESCALATE with error logs and attempts.
```

### Scenario 2: Test Fails

```
Error: Unit tests fail after implementation
Category: Technical Blocker (could be bug or test issue)
Response:
  1. Read the failing test output. Identify the failing assertion.
  2. Check if the test is correct (not a false positive). If test is wrong, fix the test.
  3. If test is correct, fix the implementation to match the expected behavior.
  4. If test keeps failing and logic seems correct → ESCALATE with test output.
```

### Scenario 3: Missing Dependency

```
Error: ImportError: No module named 'xyz'
Category: Environment Limit
Response:
  1. Try to install the dependency: pip install xyz
  2. If installation fails, check if an alternative library exists.
  3. If no alternative exists → ESCALATE with dependency requirement.
```

### Scenario 4: API Rate Limit

```
Error: API returns 429 Too Many Requests
Category: External Dependency
Response:
  1. Wait 1 second, retry.
  2. Wait 2 seconds, retry.
  3. Wait 4 seconds, retry.
  4. If still rate-limited → ESCALATE with API details.
```

### Scenario 5: Permission Denied

```
Error: Cannot write to /protected/path
Category: Environment Limit
Response:
  1. Try writing to the user's workspace instead.
  2. If the goal specifically requires the protected path → ESCALATE.
  3. If an alternative path works, proceed with the alternative and note the change.
```

### Scenario 6: User Goal is Vague

```
Error: "Make the website better"
Category: Ambiguity
Response:
  1. Do NOT escalate. Ask clarifying questions instead.
  2. "What specific aspect would you like to improve? (design, performance, features, accessibility)"
  3. "Do you have a reference or benchmark in mind?"
  4. After clarification, proceed with the goal-skill framework.
```

---

## Post-Escalation Recovery

When the user resolves the blocker:

1. **Acknowledge the resolution** and confirm understanding.
2. **Assess impact**: Does the resolution change the plan or design?
3. **Resume execution**: Return to the stage where the blocker occurred.
4. **Reset retry counters**: Fresh attempts after a resolution.
5. **Document the change**: Note what was changed based on user input.
