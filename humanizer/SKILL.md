---
name: humanizer
description: Rewrites AI-generated or robotic text to sound natural, human, and authentic. Use when the user asks to humanize, rewrite, improve writing tone, remove AI patterns, or make text sound less like an AI wrote it. Triggers include "humanize this", "make this sound more human", "rewrite this", "remove AI patterns", "fix the tone", "make it less robotic", "polish my writing", "edit for voice", or any request to improve prose quality.
version: 1.0.0
author: local
tags:
  - writing
  - humanizer
  - tone
  - editing
  - ai-writing
---

# Humanizer Skill

Rewrites text to sound natural, authentic, and genuinely human — stripping out AI "tells" and replacing them with clear, confident prose.

## When to Use

- User pastes text and says "humanize this", "make this sound more human", or "less robotic"
- Text feels stiff, overly formal, or reads like a template
- Writing has repetitive sentence openers, hedging phrases, or filler transitions
- User wants to improve voice, flow, or readability without changing the core message

---

## How to Humanize Text

Follow this systematic process every time:

### Step 1 — Diagnose Before Rewriting

Scan for these AI/robotic patterns first, then fix them:

**Banned phrases (delete or rephrase):**
- "It's worth noting that..."
- "It is important to note..."
- "Delve into", "dive deep", "unpack"
- "In today's fast-paced world..."
- "In conclusion," / "To summarize,"
- "Furthermore," / "Moreover," / "Additionally," (when overused)
- "Leverage", "utilize" (use "use")
- "Ensure" (usually replace with "make sure" or cut)
- "At the end of the day"
- "When it comes to..."
- "The fact that..."
- "In order to" (replace with "to")
- "As previously mentioned"
- "That being said,"
- "It goes without saying"
- "Needless to say"
- Excessive "very", "really", "quite", "rather"

**Structural patterns to fix:**
- Every sentence starting with the same subject
- Three-part lists used as a substitute for a real sentence
- Passive voice where active reads better
- Walls of text with no breath — break into shorter paragraphs
- Over-hedged language ("might", "could potentially", "arguably") when confidence is appropriate

### Step 2 — Apply Humanizing Techniques

**Sentence rhythm:** Vary length deliberately. Short punches. Then a longer sentence that gives the reader room to breathe and absorb the idea before moving forward.

**Voice:** Write like you'd explain it to a smart colleague over coffee — not to a committee.

**Specificity over generality:** "Saved 3 hours a week" > "significantly improved efficiency"

**Show, don't hedge:** "This breaks authentication" > "This could potentially impact authentication functionality"

**Natural transitions:** Use real connectives — "But", "So", "Here's why", "The catch is", "What this means in practice" — not "Furthermore" and "Moreover."

**Contractions:** Use them freely — "it's", "don't", "you'll", "here's" — unless the tone is formally technical.

**First/second person:** Engage the reader with "you" where appropriate. Use "we" for shared context.

### Step 3 — Preserve What Matters

- Keep all facts, data, and claims intact — never invent or omit information
- Preserve the original structure/order unless reorganizing genuinely helps
- Match the user's desired register (casual blog vs. professional report) — ask if unclear
- Keep domain-specific terminology exactly as-is

### Step 4 — Output Format

Present the rewrite clearly:

```
[HUMANIZED VERSION]
<rewritten text here>

[CHANGES MADE]
- Removed: [list of deleted phrases/patterns]
- Restructured: [what changed structurally]
- Tone shift: [brief note on what changed in feel]
```

If the text is short (under 100 words), skip the changes summary and just provide the rewrite.

---

## Tone Modes

If the user specifies a mode, apply it:

| Mode | Style |
|------|-------|
| **Casual** | Conversational, contractions, short sentences, first-person friendly |
| **Professional** | Clear and direct, no jargon, confident without being stiff |
| **Technical** | Precise vocabulary preserved, but flow improved; active voice |
| **Marketing** | Punchy, benefit-first, specific numbers, strong verbs |
| **Academic** | Formal register kept, but hedging reduced; passive voice minimized |

Default to **Professional** if no mode is specified.

---

## Quick Examples

**Before (AI-generated):**
> It is important to note that in today's fast-paced world, leveraging the right tools is crucial to ensure that teams can effectively utilize their resources and furthermore, drive meaningful outcomes across various organizational contexts.

**After (Humanized):**
> The right tools make a real difference. When teams have what they need, they get things done — and the results show up across the whole organization.

---

**Before:**
> The implementation of this feature may potentially lead to significant improvements in user experience, as it could arguably streamline the process by which users are able to navigate through the interface.

**After:**
> This feature simplifies navigation. Users get where they're going faster.

---

## When to Ask Before Rewriting

- Audience is unclear (internal vs. external? expert vs. general?)
- Desired tone is ambiguous
- Text is very long — confirm scope before rewriting everything
- Original contains unusual formatting that needs to be preserved
