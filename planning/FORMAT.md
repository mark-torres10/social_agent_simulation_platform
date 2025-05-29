# Planning Document Markdown Format

This document describes the required format and content for all planning markdown files in this folder. Follow these guidelines to ensure consistency, clarity, and traceability across all planning documents.

---

## File Naming
- Use the format: `<number>_<short_description>_planning.md`
  - Example: `7_discover_new_leads_planning.md`
- Number sequentially based on planning chronology.
- Check existing files in the folder and determine what the latest number is, then name the file starting with the next number.

## Structure & Required Sections

### 1. Title
- Format: `# <Short Description> Plan`
  - Example: `# UI Discover New Leads Tab Plan`

### 2. Problem Statement
- Clearly describe the user or technical problem being addressed.
- Use bullet points for clarity.
- Include context, pain points, and any relevant background.

### 3. Solution Overview
- Summarize the proposed solution and high-level approach.
- List main features, flows, or changes.
- Reference relevant files/modules.

### 4. UI/UX Plan (if applicable)
- Detail the user interface and experience design.
- Break down the user flow into steps.
- Specify visual/interaction requirements, error handling, and best practices.
- Reference `UI_PRINCIPLES.md` and `RULES.md` as needed.

### 5. Implementation Checklist
- Use a checklist (`- [ ]` or `- [x]`) for all major tasks required to complete the plan.
- Each item should be actionable and testable.
- Update with `[x]` as tasks are completed.

### 6. References
- List related planning docs, previous updates, or relevant files.
- Use relative paths where possible.

### 7. Additional Notes
- Optionally include a section for ongoing tracking of bugs, improvements, or future work related to this plan.
- Example: `**All future bugs and improvements for this feature will be tracked in this file.**`

---

## Style & Formatting Guidelines
- Use Markdown headers (`#`, `##`, etc.) for section separation.
- Use bullet points and checklists for clarity.
- Keep language concise and actionable.
- Use bold for important terms or section headers within lists.
- Include horizontal rules (`---`) to separate major sections.
- If a section is not applicable, include it with a note (e.g., `## UI/UX Plan\n- Not applicable for this backend-only feature.`)
- For multi-phase or multi-bug plans, use sub-sections with clear headers.

---

## Step-by-Step Guide for Creating a Planning File
1. **Start with a clear, descriptive title.**
2. **Write a concise problem statement.**
3. **Outline the solution and main flows.**
4. **Detail the UI/UX plan if relevant.**
5. **List all implementation tasks as a checklist.**
6. **Add references to related docs or files.**
7. **Include a section for ongoing tracking if needed.**
8. **Review for clarity, completeness, and adherence to this format.**

---

## Example

```
# UI Example Feature Plan

## Problem Statement
- Users cannot currently filter leads by region, making it hard to target outreach.

## Solution Overview
- Add region filter dropdown to leads tab.
- Update backend to support region-based queries.

## UI/UX Plan
- Dropdown for region selection above leads table.
- Show filtered results in real time.
- Error message if no leads match filter.

## Implementation Checklist
- [ ] Add region field to lead model
- [ ] Update leads API to support region filter
- [ ] Add dropdown to UI
- [ ] Test filtering logic

---

**All future bugs and improvements for this feature will be tracked in this file.** 