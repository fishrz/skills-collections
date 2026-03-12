---
name: architecture-decision-records
description: Write and maintain Architecture Decision Records (ADRs) following best practices for technical decision documentation. Use when documenting significant technical decisions, reviewing past architectural choices, or establishing decision processes.
---

# Architecture Decision Records

Comprehensive patterns for creating, maintaining, and managing Architecture Decision Records (ADRs) that capture the context and rationale behind significant technical decisions.

## When to Use This Skill

- Making significant architectural decisions
- Documenting technology choices
- Recording design trade-offs
- Onboarding new team members
- Reviewing historical decisions
- Establishing decision-making processes

## Core Concepts

### 1. What is an ADR?

An Architecture Decision Record captures:

- **Context**: Why we needed to make a decision
- **Decision**: What we decided
- **Consequences**: What happens as a result

### 2. When to Write an ADR

| Write ADR | Skip ADR |
| -------------------------- | ---------------------- |
| New framework adoption | Minor version upgrades |
| Database technology choice | Bug fixes |
| API design patterns | Implementation details |
| Security architecture | Routine maintenance |
| Integration patterns | Configuration changes |

### 3. ADR Lifecycle

```
Proposed → Accepted → Deprecated → Superseded
              ↓
           Rejected
```

## Templates

### Template 1: Standard ADR (MADR Format)

```markdown
# ADR-0001: [Title]

## Status
Accepted

## Context
[Why we needed to make this decision]

## Decision Drivers
- **Must have**: [requirement]
- **Should have**: [preference]

## Considered Options
### Option 1: [Name]
- **Pros**: ...
- **Cons**: ...

## Decision
We will use **[Choice]**.

## Consequences
### Positive
- [benefit]

### Negative
- [drawback]

## Related Decisions
- ADR-XXXX: [Related decision]
```

### Template 2: Lightweight ADR

```markdown
# ADR-[N]: [Title]

**Status**: Accepted
**Date**: YYYY-MM-DD
**Deciders**: @name1, @name2

## Context
[Problem statement in 2-3 sentences]

## Decision
[What was decided]

## Consequences
**Good**: [benefits]
**Bad**: [drawbacks]
**Mitigations**: [how to address drawbacks]
```

### Template 3: Y-Statement Format

```markdown
In the context of **[situation]**,
facing **[concern]**,
we decided for **[option]**
and against **[other options]**,
to achieve **[quality]**,
accepting that **[downside]**.
```

### Template 4: ADR for Deprecation

```markdown
# ADR-[N]: Deprecate [X] in Favor of [Y]

## Status
Accepted (Supersedes ADR-[original])

## Context
[Why original decision no longer fits]

## Decision
Deprecate [X] and migrate to [Y].

## Migration Plan
1. Phase 1: [steps]
2. Phase 2: [steps]
3. Phase 3: [steps]

## Lessons Learned
- [what was overestimated]
- [what was underestimated]
```

## ADR Management

### Directory Structure

```
docs/
└── adr/
    ├── README.md           # Index and guidelines
    ├── template.md         # Team template
    ├── 0001-database-choice.md
    └── 0002-caching-strategy.md
```

### ADR Index (README.md)

```markdown
| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-database-choice.md) | Use PostgreSQL | Accepted | 2024-01-10 |
```

## Review Checklist

- [ ] Context clearly explains the problem
- [ ] All viable options considered (minimum 3)
- [ ] Pros/cons balanced and honest
- [ ] Consequences (positive and negative) documented
- [ ] Related ADRs linked
- [ ] At least 2 senior engineers reviewed

## Best Practices

### Do's
- Write ADRs **before** implementation starts
- Keep them short (1-2 pages max)
- Be honest about trade-offs
- Link related decisions
- Update status when superseded

### Don'ts
- Don't change accepted ADRs — write new ones to supersede
- Don't skip context
- Don't hide failures — rejected decisions are valuable
- Don't be vague about consequences
