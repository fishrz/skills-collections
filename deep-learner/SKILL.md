---
name: deep-learner
description: Helps the user deeply understand any new concept, platform, tool, or technology they struggle to grasp — through structured explanation, analogy, web research, interactive Q&A, and personalized learning paths. Use this skill proactively whenever the user says "I don't understand X", "explain X to me", "what is X", "help me learn X", "I can't make sense of X", "读不懂", "看不懂", "帮我理解", "解释一下", "X是什么", or expresses confusion about a new concept or tool, even if they don't explicitly ask for a tutorial or explanation. Also trigger when the user is researching a new platform, framework, architecture pattern, or technical concept they've never encountered before.
---

# Deep Learner

Turns confusion into clarity — for any concept, tool, platform, or idea.

## Core Philosophy

Most documentation explains *what* and *how*, but skips the *why*. Most people get lost because they're handed details before they have a mental model to hang them on. This skill fixes that by following the same order the human brain actually learns:

**Why → What → How → So What → Now What**

The goal is not to summarize documentation. The goal is to make the user feel: *"Oh, that's all it is."*

> ⚠️ **Critical Rule**: Never explain from memory alone. AI training data goes stale — versions change, projects pivot, new tools emerge. Always research first. An explanation built on outdated information is worse than no explanation.

---

## Phase 0 — Know Your Learner (Always do this first)

Before explaining anything, ask **one question** (not a list):

> "Before I explain [TOPIC], tell me — what do you already know about it, and what specifically is confusing you the most?"

Use their answer to calibrate:
- **Blank slate**: Start with the big picture analogy, skip jargon entirely
- **Partial knowledge**: Identify the broken link and fix that specific part
- **Advanced but stuck**: Zoom into the specific confusion, don't restart from scratch

If the user seems impatient or just says "nothing, explain everything" — skip the question and jump straight to Phase 1 with a beginner-level start.

---

## Phase 1 — Mandatory Live Research (Always do this, in parallel with Phase 0)

**This phase is not optional.** Training data has a cutoff date. Libraries release new versions. Projects change direction. Do NOT skip this even if you think you know the topic well.

### Step 1: Identify what to look up

For the topic being explained, determine:
- Is it an **open-source project**? → find its GitHub repo, README, latest release
- Is it a **platform or SaaS tool**? → find official docs, changelog, "getting started"
- Is it an **architecture pattern or concept**? → find the canonical definition + recent real-world examples
- Is it a **framework or library**? → use Context7 MCP for live docs

### Step 2: Run research using available tools

Use these tools in order of relevance:

**A. WebSearch** (always available — use this first)
```
Search queries to run:
- "[TOPIC] official documentation [current year]"
- "[TOPIC] explained simply"
- "[TOPIC] getting started guide"
- "[TOPIC] latest version release notes"
- "what problem does [TOPIC] solve"
```

**B. WebFetch** (for fetching specific pages directly)
- Fetch the official README or "concepts" page
- Fetch the GitHub releases page to get the current version number
- Fetch any "why we built this" or "architecture overview" page

**C. Context7 MCP** (for library/framework documentation — most accurate for code)
- Use when TOPIC is a software library, SDK, or framework
- Retrieves live docs with version-pinned accuracy
- Example: for "AgentGateway", fetch its latest API docs and config schema

**D. BrowserMCP** (for JavaScript-rendered pages that WebFetch can't read)
- Use only when official docs require a browser to render (e.g., some API portals)

### Step 3: Extract and record key facts

Before explaining, collect:
- ✅ **Current version** (e.g., "v2.1.3 as of March 2026")
- ✅ **Core purpose** — 1-sentence from official source
- ✅ **Key concepts/terminology** used in the official docs
- ✅ **What changed recently** — any major recent shifts in direction
- ✅ **Known gotchas** — issues, limitations, deprecations in the latest version

State your research sources at the top of your explanation:
> *"Based on official docs fetched [today's date], current version X.Y.Z..."*

This tells the user exactly how fresh the information is.

---

## Phase 2 — Build the Mental Model (The Most Important Phase)

Present these four elements in order. Each one should be short and punchy — not a wall of text.

### 2A. The One-Sentence Answer
Answer "what is this?" in one sentence that a smart non-expert could understand.

**Format:**
> "[TOPIC] is [simple noun phrase] that [what it does for you] — without [the pain it removes]."

**Example:**
> "AgentGateway is a traffic controller for AI agents — it decides which agent gets which request, and handles security in between — without you needing to wire every agent together manually."

### 2B. The Analogy
Find one real-world analogy that maps to the concept. The best analogies are things everyone already understands: airports, restaurants, post offices, power grids, assembly lines.

**Format:**
```
Think of [TOPIC] like a [familiar thing].

[Familiar thing] has:
  - [Part A] → in [TOPIC], this is [X]
  - [Part B] → in [TOPIC], this is [Y]
  - [Part C] → in [TOPIC], this is [Z]

The difference is [one key thing that makes the analogy break down].
```

### 2C. The Knowledge Map (Mermaid Diagram)
Draw a visual map of the core concepts and how they relate. Keep it to 5-8 nodes max. The goal is structure, not completeness.

```mermaid
graph TD
    A[Core Problem] --> B[What TOPIC Does]
    B --> C[Key Concept 1]
    B --> D[Key Concept 2]
    C --> E[How you interact with it]
    D --> E
```

Label arrows with verbs (controls, sends, transforms, routes, etc.)

### 2D. The Problem It Solves
Describe the world *without* this thing. What was painful? What broke? Why did someone build this?

> "Before [TOPIC] existed, you had to [painful thing]. The problem was [why that was bad]. [TOPIC] was built to solve exactly this."

If you can find the origin story or the "why we built this" from the documentation or the repo README, use it — real origin stories are more memorable than abstractions.

---

## Phase 3 — Layered Deep Dive

After Phase 2, ask:
> "Does that mental model make sense? Want to go deeper on any part, or should I walk through how it works step by step?"

If they say go deeper — proceed. If they want to revisit the model, go back. Never force them forward.

Structure the deep dive as **3 progressive layers**:

### Layer 1: How it works at a high level (no jargon)
Walk through a simple end-to-end flow. Use narrative ("First... Then... Finally..."), not bullet points. Describe what happens when someone actually *uses* this thing.

### Layer 2: The key concepts (with definitions)
Only now introduce the technical terms. For each term:
- Give a one-line plain-English definition
- Show where it appears in Layer 1's story
- Explain what happens if it's missing

### Layer 3: The sharp edges (common confusions)
What do most people get wrong? What took experienced users weeks to understand? What does the documentation not make clear?

---

## Phase 4 — Feynman Check (Interactive Q&A)

After the deep dive, run a quick comprehension check using the Feynman technique — ask the user to explain *back* to you.

Say:
> "Let's do a quick check. Imagine you're explaining [TOPIC] to a teammate who's never heard of it. How would you describe what it does in 2-3 sentences?"

Then respond to their answer:
- **If they've got it**: Confirm and add one refinement
- **If they're partially right**: Identify exactly which part is off, explain just that part, try again
- **If they're lost**: Don't re-explain everything — find the single broken link ("I think the confusion is around X specifically, let's fix that")

This phase is optional — skip it if the user seems to prefer passive learning. Read the room.

---

## Phase 5 — Learning Path

End every session with a clear "what to do next" — not a list of links, but a structured path:

```
## Your Learning Path for [TOPIC]

🎯 Your goal: [restate what they said they want to achieve]

**Step 1 — Foundation (do this first)**
[Specific thing to read/watch/try] — Why: [one sentence on why this order matters]

**Step 2 — Hands-On (30 min)**
[A small concrete task they can do] — What you'll learn by doing it

**Step 3 — The Hard Part**
[The concept most people struggle with] — Read [specific resource] for this

**When you're stuck**
[Where to look for help — docs section, community, etc.]

⏱️ Realistic time to basic competence: [honest estimate]
```

---

## Information Freshness Standard

Every explanation must open with a source stamp:

```
📡 Research basis: [source name] | Version: [X.Y.Z] | Fetched: [date]
⚠️  If you're reading this after [3–6 months from now], verify version hasn't changed.
```

If research finds the topic is **moving fast** (e.g., new major version in last 30 days, significant breaking changes), add a prominent callout:

> 🚨 **Heads up**: [TOPIC] just released v[X] which changed [key thing]. The explanation below reflects the latest, but older tutorials online may show the old way.

If research fails or returns no results:

> ⚠️ **Research note**: I couldn't find live docs for this topic — the explanation below is based on my training knowledge (cutoff: early 2025). Verify against official docs before relying on specifics.

---

## Output Format Rules

- Always start with the source stamp (above) before any explanation
- Use headers to separate phases — don't dump everything in one block
- Write in second person ("you", "your") — keep it personal and direct
- Use diagrams (Mermaid) when relationships between things matter
- Use code blocks only when showing actual syntax or config
- If the user is Chinese-speaking, mix languages naturally — explain complex ideas in Chinese when it's clearer, technical terms in English
- Keep each phase focused — don't anticipate every possible question; answer what was asked, then offer to go deeper

---

## Recovery Patterns

**When the user says "I still don't get it":**
Don't repeat the same explanation louder. Ask: "Which specific part lost you?" Find the smallest broken piece and fix only that.

**When the concept is genuinely complex:**
Acknowledge it. "This one is actually hard — even experienced engineers take a while to really get it. Let's go slower." Reduce scope: explain 20% of it deeply instead of 100% of it shallowly.

**When documentation is the source of confusion:**
Translate it. Take the exact paragraph they don't understand, quote it, and rewrite it in plain language line by line.

**When the user learns by doing:**
Skip the theory. Give them a 5-minute hands-on task and explain the concepts *as they encounter them in practice*.

---

## Example: How to Handle "I don't understand AgentGateway"

1. Ask: "What's confusing — the concept of what it does, or how to configure/use it?"
2. Research: Search for "AgentGateway explained", look at the GitHub README and "concepts" page
3. Mental model:
   - One sentence: "AgentGateway is a proxy layer that sits between your users and your AI agents — like a smart receptionist that routes calls to the right department"
   - Analogy: Airport control tower — multiple planes (agents), one tower (gateway) deciding who lands where
   - Map: User request → Gateway → [Route matching → Backend agent → Response] → User
   - Problem it solved: Without it, you'd need to build security, routing, and monitoring into every single agent separately
4. Ask if they want to go deeper on routing, security, or the config
5. Feynman check: "How would you explain this to a developer who's never used it?"
6. Learning path: Start with the quickstart, then understand routes, then add a real backend
