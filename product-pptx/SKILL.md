---
name: product-pptx
description: "Generate product presentations from markdown Q&A data using PPTX templates. Use when Claude needs to: (1) Transform Q&A content into presentation-ready slides, (2) Follow embedded template guidelines to generate appropriate content, (3) Intelligently summarize, reformat, or rewrite content to fit slide constraints, (4) Fill table cells with data, (5) Delete guideline boxes from final output"
license: Proprietary
---

# Product Presentation Generator

Transform markdown Q&A data into polished PowerPoint presentations using templates with embedded guidelines.

## Workflow Overview

1. **Analyze Template** - Extract structure, placeholders, and embedded guidelines
2. **Parse Markdown** - Read Q&A data from structured markdown file
3. **Generate Content** - Transform Q&A into slide-ready content following guidelines
4. **Apply Replacements** - Fill slides and delete guideline boxes

---

## Step 1: Analyze Template

### Create Visual Reference
```bash
python scripts/thumbnail.py template.pptx template-thumbnails --outline-placeholders
```

### Extract Text Inventory
```bash
python scripts/inventory.py template.pptx template-inventory.json
```

### Identify Guideline Boxes

**Marker:** Shapes containing `"Delete this box from the final version!"` are instruction boxes (gold-colored).

When reviewing inventory, separate shapes into:
- **Content shapes**: Regular placeholders to fill with content
- **Guideline shapes**: Instruction boxes to read, follow, then clear

Create a guidelines summary for each slide:
```
Slide 0: [Title slide - product name only]
Slide 1: "Include 3-5 key applications with customer benefits..."
Slide 2: "List market trends as bullet points, max 4 items..."
```

### Inventory Structure
```json
{
  "slide-0": {
    "shape-0": {
      "placeholder_type": "TITLE",
      "width": 7.5,
      "height": 1.2,
      "paragraphs": [{ "text": "Product Name" }]
    },
    "shape-1": {
      "paragraphs": [{ "text": "Delete this box from the final version! Instructions..." }]
    }
  },
  "slide-6": {
    "table-0": {
      "type": "table",
      "rows": 4,
      "columns": 5,
      "cells": {
        "0,0": { "text": "Header 1", "row": 0, "col": 0 },
        "0,1": { "text": "Header 2", "row": 0, "col": 1 },
        "1,0": { "text": "Row 1 Data", "row": 1, "col": 0 }
      }
    }
  }
}
```

Key fields:
- **Slides**: `slide-0`, `slide-1`, etc. (0-indexed)
- **Shapes**: Ordered by position (top-to-bottom, left-to-right)
- **Tables**: Identified as `table-0`, `table-1`, etc. with `"type": "table"`
- **placeholder_type**: `TITLE`, `SUBTITLE`, `BODY`, `OBJECT`, or `null`
- **width/height**: Shape dimensions in inches (for content fitting)
- **cells**: Table cell content indexed by `"row,col"` (e.g., `"0,0"`, `"1,2"`)

---

## Step 2: Parse Markdown Q&A

Read structured Q&A file and extract answers by section:

```markdown
## Section N: Section Name

### QN: Question Title
**Question:** What is X?

**Answer:**
The answer content here...
```

### Map Sections to Slides

| Q&A Section | Typical Slide |
|-------------|---------------|
| Title/Product Name | Title slide |
| Target Applications | Use cases slide |
| Market Trends | Trends slide (bullets) |
| Technology Trends | Technology slide |
| Product Features | Feature slides |
| Portfolio Matrix | Comparison table slide |

---

## Step 3: Generate Content

**This is the intelligence step.** Transform raw Q&A answers into presentation-ready content.

### Content Transformation Types

| Transformation | When to Apply | Example |
|----------------|---------------|---------|
| **Summarize** | Q&A verbose, slide space limited | 5 paragraphs → 3-7 bullets |
| **Reformat** | Q&A prose, slide needs structure | Paragraph → bullet list |
| **Condense** | Text too long for shape | Long sentence → short phrase |
| **Expand** | Q&A brief, slide needs detail | Notes → full explanation |
| **Rewrite** | Technical specs → customer language | Specs → benefits |

### Follow Guideline Instructions

For each slide with a guideline box:
1. **Read** the guideline text (what it asks for)
2. **Find** matching Q&A content from markdown
3. **Transform** content to meet guideline requirements
4. **Fit** to shape constraints (width, height, bullet count)

### Fitting Content to Shapes

Use shape dimensions from inventory to estimate capacity:
- **Title shapes**: 1-2 lines, short phrases
- **Body shapes**: Estimate lines from height (~0.3" per line)
- **Bullet lists**: Typically 3-6 items max for readability

**If content overflows**: Summarize further, use shorter phrasing, or note for user review.

### Create Replacement JSON

```json
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        { "text": "Automotive PSoC 4000", "bold": true, "alignment": "CENTER" }
      ]
    },
    "shape-1": {
      "delete": true
    }
  },
  "slide-1": {
    "shape-0": {
      "paragraphs": [
        { "text": "Target Applications", "bold": true },
        { "text": "Body Electronics - window lifts, seat controls", "bullet": true, "level": 0 },
        { "text": "Sensor Interfaces - temperature, pressure sensing", "bullet": true, "level": 0 },
        { "text": "Touch Sensing - capacitive buttons and sliders", "bullet": true, "level": 0 }
      ]
    },
    "shape-1": {
      "delete": true
    }
  }
}
```

**Important:**
- Guideline boxes get `"delete": true` to remove them entirely
- Regular content shapes get generated text with proper formatting
- To clear a shape but keep it visible: use `"paragraphs": []`
- Shapes not in JSON are automatically cleared (text removed)

### Paragraph Formatting Rules

| Property | Usage |
|----------|-------|
| `delete` | `true` to remove entire shape (for guideline boxes) |
| `text` | Content (required for paragraphs) |
| `bold` | `true` for headers/titles |
| `bullet` | `true` for list items |
| `level` | `0` for first-level bullets (required when bullet: true) |
| `alignment` | `CENTER`, `RIGHT`, `JUSTIFY` (LEFT is default) |
| `font_size` | Size in points (optional) |

**Critical:**
- Do NOT include bullet symbols in text - added automatically
- Bullets are automatically left-aligned
- Match original formatting from inventory when appropriate

### Table Cell Replacement

For tables (e.g., portfolio matrix), use cell coordinates:

```json
{
  "slide-6": {
    "table-0": {
      "cells": {
        "0,0": { "text": "" },
        "0,1": { "text": "PSoC 4000" },
        "0,2": { "text": "PSoC 4100" },
        "1,0": { "text": "Flash (KB)" },
        "1,1": { "text": "16-32" },
        "1,2": { "text": "32-64" },
        "2,0": { "text": "GPIO" },
        "2,1": { "text": "24" },
        "2,2": { "text": "36" }
      }
    }
  }
}
```

**Table cell notes:**
- Cell keys use `"row,col"` format (0-indexed)
- Row 0 is typically the header row
- Column 0 is typically the row labels
- Only cells with replacements need to be included
- Cell text replaces existing content while preserving formatting
- Map Q&A table data thoughtfully: column/row names may not match exactly

---

## Step 4: Apply Replacements

```bash
python scripts/replace.py template.pptx replacement-text.json output.pptx
```

The script will:
1. Validate all shapes and tables in JSON exist in template
2. Clear ALL text shapes from inventory
3. Apply new paragraphs from JSON
4. Fill table cells with replacement data
5. Check for text overflow issues
6. Save final presentation

### Validation Errors

**Missing shape:**
```
ERROR: Shape 'shape-5' not found on 'slide-0'. Available shapes: shape-0, shape-1
```

**Text overflow:**
```
ERROR: overflow worsened by 1.25" (was 0.00", now 1.25")
```
Fix: Reduce text length, use shorter phrasing, or decrease font size.

---

## Complete Example

### Given Markdown Q&A:
```markdown
## Section 1: Title Slide
### Q1: Product Title
**Answer:**
Automotive PSoC 4000

## Section 2: Target Applications
### Q2: Use Cases
**Answer:**
- Automotive Sensor Interfaces: Integration of analog front ends
- Body Electronics: Control modules for lighting, window lifts
- Human-Machine Interface: Capacitive touch sensing for buttons
- Signal Conditioning: Analog signal processing and filtering

## Section 10: Product Portfolio Matrix
### Q10: Portfolio Comparison
**Answer:**
| Feature | PSoC 4000T | PSoC 4100T |
|---------|-----------|-----------|
| Flash | 16-32 KB | 32-64 KB |
| GPIO | 24 | 36 |
| CapSense | Yes | Yes |
```

### Template Inventory Shows:
- `slide-0/shape-0`: Title placeholder
- `slide-0/shape-1`: Guideline box - "Delete this box..."
- `slide-1/shape-0`: Body placeholder
- `slide-1/shape-1`: Guideline box - "Include 3-5 applications with benefits"
- `slide-6/table-0`: Portfolio matrix table (4 rows x 3 columns)

### Generate Replacement JSON:
```json
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        { "text": "Automotive PSoC 4000", "bold": true, "alignment": "CENTER" }
      ]
    },
    "shape-1": { "delete": true }
  },
  "slide-1": {
    "shape-0": {
      "paragraphs": [
        { "text": "Target Applications", "bold": true },
        { "text": "Sensor Interfaces - analog front-end integration", "bullet": true, "level": 0 },
        { "text": "Body Electronics - lighting and motor control", "bullet": true, "level": 0 },
        { "text": "Touch Sensing - capacitive HMI solutions", "bullet": true, "level": 0 }
      ]
    },
    "shape-1": { "delete": true }
  },
  "slide-6": {
    "table-0": {
      "cells": {
        "0,1": { "text": "PSoC 4000T" },
        "0,2": { "text": "PSoC 4100T" },
        "1,0": { "text": "Flash" },
        "1,1": { "text": "16-32 KB" },
        "1,2": { "text": "32-64 KB" },
        "2,0": { "text": "GPIO" },
        "2,1": { "text": "24" },
        "2,2": { "text": "36" },
        "3,0": { "text": "CapSense" },
        "3,1": { "text": "Yes" },
        "3,2": { "text": "Yes" }
      }
    }
  }
}
```

Note: Q&A had 4 verbose items; transformed to 3 concise bullets per guideline. Table data mapped from markdown table to slide table structure.

### Run:
```bash
python scripts/replace.py template.pptx replacement-text.json output.pptx
```

---

## Quick Reference

### Commands
| Task | Command |
|------|---------|
| Visual preview | `python scripts/thumbnail.py template.pptx thumbnails --outline-placeholders` |
| Extract inventory | `python scripts/inventory.py template.pptx inventory.json` |
| Apply replacements | `python scripts/replace.py template.pptx replacements.json output.pptx` |

### Guideline Box Handling
- **Identify**: Contains `"Delete this box from the final version!"` (gold-colored)
- **Use**: Read instructions to guide content generation
- **Delete**: Set `"delete": true` in replacement JSON (removes entire shape)

### Internal Guidance Slide Handling
Some templates contain entire slides marked for deletion (not just guideline boxes within slides). These are internal-only guidance slides that should not appear in the final presentation.

- **Marker:** Shapes containing `"This slide to be deleted – only for internal guidance!"` (red text, centered)
- **Common location:** Usually slide 1 (the slide after the title), containing content guidelines tables and writing policy references
- **Action:** The replace.py script cannot delete entire slides — only shapes. To handle these:
  1. **During inventory analysis:** Identify guidance-only slides and note their slide index
  2. **In replacement JSON:** Clear all text shapes on the guidance slide (they will be auto-cleared since no paragraphs are specified) — do NOT include the slide in replacement JSON at all, so all its text gets cleared automatically
  3. **Post-generation:** Note to user that the guidance slide(s) need manual deletion from the final PPTX (e.g., "Delete slide 2 — internal guidance only")

**Example guidance slides found across templates:**
| Template | Guidance Slide(s) | Content |
|----------|--------------------|---------|
| Fighting guide | Slide 1 | Minimum content recommendations, writing policies |
| Product presentation | Slide 1 | Content requirements per section |
| Customer connector | Slide 1 | Section requirements and guidelines |
| Product roadmap | Slide 1 | Content requirements per section |

### Slide Indexing
- Slides are **0-indexed**: first slide = `slide-0`
- Shapes are sorted by visual position (top-to-bottom, left-to-right)

### Dependencies
- `python-pptx`: `pip install python-pptx`
- `Pillow`: `pip install Pillow`
- `LibreOffice`: For thumbnail generation
- `poppler-utils`: For PDF to image conversion
