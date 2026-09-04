# Product discovery tracker design

Date: 2026-09-03
Status: approved and implemented in `apps/product-discovery/index.html`

## Goal

Replace a paid Jira Product Discovery seat for a single user with a tool that costs nothing to run and keeps its data in a file the user controls.

## Decisions

- **Single user, file-based.** One `.json` project file synced through Box or Drive. No backend, no accounts.
- **One HTML file.** No build toolchain, no dependencies beyond Google Fonts, which fall back to system fonts when offline.
- **Standalone.** Delivery work is a free-text reference on the idea, not a live Jira link.
- **Features in scope.** Ideas table with custom fields and a computed score, board by status, impact-vs-effort matrix, dated timeline roadmap plus Now / Next / Later buckets, insights and comments per idea, filters and search, Auto / Light / Dark theme.

## Approaches considered

1. Single HTML file using the File System Access API. Chosen. Works today in Chrome and Edge with zero setup. Safari and Firefox degrade to browser storage plus export/import.
2. Tauri or Electron desktop app. Works in any engine but adds a build chain and installers for a one-person tool.
3. Local Python server owning the file. Works everywhere but the user must start a process each session.

## Architecture

Everything lives in one file with four layers:

- **Data model.** `{version, name, seq, ideas[]}`. Each idea: `id, key, title, description, status, impact 1-5, effort 1-5, confidence 0-100, reach, labels[], owner, delivery, bucket, start, end, insights[], comments[], history[], created, updated`. `start` and `end` are `YYYY-MM-DD` strings and may be empty. Statuses and buckets are fixed lists. `fields[]` holds custom field definitions and `custom{}` on each idea holds their values.
- **Persistence.** Every change writes to `localStorage` immediately. When a file handle is connected, a debounced write goes to the file 700 ms later. The handle is stored in IndexedDB so the file reconnects after reload; the browser may require one click to re-grant permission. Export and import cover browsers without file access.
- **Views.** `render()` applies filters and sort, then dispatches to list, board, matrix, timeline, or bucket renderers. Board and buckets share one column renderer with HTML5 drag and drop.
- **Timeline.** Scheduled ideas render as absolutely positioned bars on a day-scaled track (4 px per day at month scale, 1.6 px at quarter scale). The visible range runs from one month before the earliest start or today to eight months after today or two months after the latest target. Pointer events move a bar or resize either edge; the change commits as a history entry on release. A click without movement opens the idea.
- **Field registry.** Built-in fields (status, bucket, owner, labels, impact, effort, dates) and user-defined fields share one descriptor shape `{id, name, type, options[]}`. Custom definitions live in `data.fields`; values live on each idea under `custom[fieldId]`. One getter and setter pair covers both kinds, so grouping, sorting, board columns, and search never special-case custom fields. Types: select, multiselect, checkbox, text, number, date, rating.
- **Grouping.** `groupKeys(idea, field)` returns the group or groups an idea belongs to for any field; a multi-select yields one per option, dates yield the month, empty values fall into a trailing "No <field>" group. The Ideas table and Timeline render group header rows with count, total score, and collapse. The Board renders columns from any select or checkbox field's options. Group and column choices persist per view in browser storage.
- **View state.** One `ui` object holds everything a view is: type, search, filter rules, sort, grouping, board column field, hidden columns, and timeline scale. It persists to browser storage between sessions. A saved view is a named snapshot of it stored in `data.views`; selecting one replaces `ui`, and a JSON comparison of the normalized snapshot against the saved copy drives the unsaved marker.
- **Filters.** `ui.rules` is a list of `{field, op, value}`. Operators are chosen by field type; `matchRule` evaluates one rule against an idea and all rules must pass. Status chips read and write a single Status "in" rule so the quick filter and the rule editor never disagree.
- **Formulas.** A custom field of type `formula` carries an expression string. A hand-written tokenizer and recursive-descent parser compile it to a closure once per distinct expression; there is no `eval`. Names resolve case-insensitively against the field registry at evaluation time, checkboxes read as 1 or 0, selects as option position, multi-selects as count. Evaluation depth is capped to break reference cycles, and any failure yields an empty value rather than an error in the view.
- **Fiscal calendar.** `data.fiscalStart` (1 to 12) and `data.fiscalName` (`end` or `start`) live in the project file. `fiscalOf(date)` returns the fiscal quarter and year, and the Timeline's quarter headers are built from it. A January start yields plain calendar labels.
- **Detail panel.** Slide-over editor for a single idea, including a Fields section rendered from the custom field definitions. Field changes append a history entry describing old and new values.

Score is `reach × impact × (confidence ÷ 100) ÷ effort`, rounded to one decimal.

## Error handling

- File write failures show in the rail with the browser's error message and the data stays in browser storage.
- Import rejects files without an `ideas` array.
- Leaving the page with an unsaved file write pending prompts the browser's unload warning.

## Testing

Manual: syntax check of the script, a headless render of the list, matrix, and board views in light and dark, and exercising the sample data. No automated suite, matching the one-file scope.
