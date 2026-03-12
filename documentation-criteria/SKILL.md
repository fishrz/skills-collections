---
name: documentation-criteria
description: Guides PRD, ADR, Design Doc, UI Spec, and Work Plan creation with templates and decision matrix. Use when deciding which documents to create for a feature, or when creating any of these document types.
---

# Documentation Creation Criteria

## Creation Decision Matrix

| Condition | Required Documents | Creation Order |
|-----------|-------------------|----------------|
| New Feature (backend) | PRD → [ADR] → Design Doc → Work Plan | After PRD approval |
| New Feature (frontend/fullstack) | PRD → **UI Spec** → [ADR] → Design Doc → Work Plan | UI Spec before Design Doc |
| ADR conditions met | ADR → Design Doc → Work Plan | Start immediately |
| 6+ files touched | ADR → Design Doc → Work Plan (Required) | Start immediately |
| 3–5 files touched | Design Doc → Work Plan (Recommended) | Start immediately |
| 1–2 files touched | None | Direct implementation |

## ADR Creation Conditions (Required if Any Apply)

### 1. Type System Changes
- Adding nested types with 3+ levels
- Changing/deleting types used in 3+ locations
- Type responsibility changes (e.g., DTO→Entity)

### 2. Data Flow Changes
- Storage location changes (DB→File, Memory→Cache)
- Processing order changes with 3+ steps
- Data passing method changes (props→Context, direct→events)

### 3. Architecture Changes
- Layer addition, responsibility changes, component relocation

### 4. External Dependency Changes
- Library/framework/external API introduction or replacement

### 5. Complex Implementation Logic
- Managing 3+ states
- Coordinating 5+ asynchronous processes

## Document Definitions

### PRD (Product Requirements Document)
**Purpose**: Define business requirements and user value

**Includes**:
- Business requirements and user value
- Success metrics and KPIs (measurable)
- User stories and use cases
- MoSCoW prioritization (Must/Should/Could/Won't)
- MVP vs. Future phase separation
- User journey diagram (required, mermaid)
- Scope boundary diagram (required, mermaid)

**Excludes**: Technical implementation, task breakdown, schedules

---

### ADR (Architecture Decision Record)
**Purpose**: Record technical decision rationale

**Includes**:
- Decision (what was selected)
- Rationale (why that selection was made)
- Option comparison (minimum 3 options) + trade-offs
- Architecture impact
- Implementation guidelines

**Excludes**: Schedule, detailed implementation code, resource assignments

---

### UI Specification
**Purpose**: Define UI structure, screen transitions, component decomposition

**Includes**:
- Screen list and transition conditions
- Component decomposition with state × display matrix (default/loading/empty/error)
- Interaction definitions linked to PRD acceptance criteria
- AC traceability from PRD to screens/components
- Existing component reuse map
- Accessibility requirements

**Excludes**: Technical implementation, API contracts, schedules

---

### Design Document
**Purpose**: Define technical implementation methods in detail

**Includes**:
- Existing codebase analysis (required)
- Technical implementation approach
- Interface and type definitions
- Data flow and component design
- Acceptance criteria (EARS format: When/While/If-then)
- Change impact map
- Integration points and data contracts

**Excludes**: Why technology was chosen (→ADR), schedule/assignments (→Work Plan)

---

### Work Plan
**Purpose**: Implementation task management and progress tracking

**Includes**:
- Task breakdown and dependencies (max 2 levels)
- Schedule and duration estimates
- E2E verification procedures (copied from Design Doc)
- Phase 4 Quality Assurance (required)
- Progress records (checkbox format)

**Phase Structure**:
1. **Phase 1 — Foundation**: Type definitions, interfaces, test scaffolding
2. **Phase 2 — Core Features**: Business logic, unit tests
3. **Phase 3 — Integration**: External connections, presentation layer
4. **Phase 4 — QA (Required)**: All acceptance criteria met, tests/types/linting pass

**Task Completion = Implementation Complete + Quality Complete + Integration Complete**

## Storage Locations

| Document | Path | Naming Convention |
|----------|------|-------------------|
| PRD | `docs/prd/` | `[feature-name]-prd.md` |
| ADR | `docs/adr/` | `ADR-[4-digits]-[title].md` |
| UI Spec | `docs/ui-spec/` | `[feature-name]-ui-spec.md` |
| Design Doc | `docs/design/` | `[feature-name]-design.md` |
| Work Plan | `docs/plans/` | `YYYYMMDD-{type}-{description}.md` |

## ADR Status Flow
`Proposed` → `Accepted` → `Deprecated` / `Superseded` / `Rejected`

## Diagram Requirements (mermaid)

| Document | Required Diagrams |
|----------|------------------|
| PRD | User journey, scope boundary |
| ADR | Option comparison (when helpful) |
| UI Spec | Screen transition, component tree |
| Design Doc | Architecture, data flow |
| Work Plan | Phase structure, task dependencies |

## AI Automation Rules
- 5+ files affected → suggest ADR creation
- Type/data flow change detected → ADR mandatory
- Check existing ADRs before implementation begins
