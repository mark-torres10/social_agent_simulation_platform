# UI Fixes Checklist

- [x] Fix ui/README.md: Add H1 heading at top
- [x] Fix ui/app/globals.css: Use --font-sans variable instead of hardcoded system font
- [x] Fix ui/app/layout.tsx: Update metadata (title, description, keywords, etc.)
- [x] Fix ui/app/page.tsx: Use run-specific agents instead of DUMMY_AGENTS
- [x] Fix ui/components/AgentDetail.tsx: Add type="button" to all button elements
- [x] Fix ui/components/ConfigForm.tsx: Fix NaN handling in onChange handlers
- [x] Fix ui/components/DetailsPanel.tsx: Filter agents to only show participating ones
- [x] Fix ui/components/RunHistorySidebar.tsx: Add type="button" to button elements
- [x] Test changes with browser tool
- [x] Commit changes with descriptive message
- [x] Push changes

## Additional Fixes

- [x] Fix ui/components/TurnHistorySidebar.tsx: Add type="button" to Summary and turn navigation buttons
- [x] Fix ui/lib/dummy-data.ts: Rotate agent selection based on turnNumber instead of always first 5
- [x] Fix ui/lib/dummy-data.ts: Add missing turn entries for 'run_2025-01-17T08:20:00' and 'run_2025-01-18T11:00:00'
- [x] Fix .gitignore: Correct malformed *.sqlite pattern
- [x] Test all fixes with browser tool
- [x] Commit and push changes

## Additional Fixes - Run Configuration and TypeScript

- [x] Fix ui/app/page.tsx: Store run configurations keyed by runId to prevent stale configs when switching runs
- [x] Fix ui/app/page.tsx: Add missing Agent import to type imports
- [x] Test fixes with browser tool
- [x] Commit and push changes

## Final Fix - Agent Count Alignment

- [x] Fix ui/lib/dummy-data.ts: Align DUMMY_RUNS.totalAgents with actual agent slices used in DUMMY_TURNS (3, 4, 3, 4, 4)
- [x] Test fix with browser tool
- [ ] Commit and push changes

