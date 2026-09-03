# Discovery Desk

A single-file, no-server replacement for Jira Product Discovery. Open `index.html` in a browser and you have an ideas backlog with scoring, a status board, an impact-vs-effort matrix, a dated timeline roadmap, and insights attached to each idea.

## Run it

1. Open `index.html` in Chrome or Edge. Nothing to install, no build step.
2. Click **Save as** in the left rail and put the `.json` project file in your Box or Google Drive folder. The app writes to that file automatically after every change.
3. Next time, open the page and click **Reconnect** (or **Open file**). The browser remembers the file.

Safari and Firefox cannot write to a local file from a web page. There the app keeps everything in browser storage and you use **Export JSON** / **Import JSON** to move data around.

The first launch loads a sample project so the views have something to show. Delete those ideas or import your own file.

## What it does

| View | What you get |
| --- | --- |
| Ideas | Sortable table with inline editing of status, impact, effort, confidence, reach, and roadmap bucket |
| Board | Kanban by status. Drag cards between columns |
| Matrix | Impact vs effort scatter. Dot size is reach, color is status. Quadrant counts and top five by score |
| Timeline | Dated roadmap. Each idea with a start and target date is a bar across months and quarters. Drag a bar to move it, drag an edge to change one date. Months or Quarters scale, today marker, and an Unscheduled list with a one-click Schedule button |
| Buckets | Now / Next / Later / Unplaced columns for coarse planning. Drag to move |

Every idea has a detail panel with description, owner, labels, delivery ticket reference, start and target dates, your custom fields, insights (text, source link, weight 1 to 3), comments, and a change history.

## Custom fields and grouping

Click **Manage fields** in the rail to add fields the way you would in Jira Product Discovery. Types: single select, multi select, checkbox, text, number, date, and rating 1 to 5. Options for selects are one per line. Renaming a field or editing its options keeps existing values; deleting a field removes its values from every idea.

Custom fields appear as editable columns in the Ideas table and as inputs in the idea panel. Search matches their values.

**Group by** in the toolbar works on the Ideas table and the Timeline, and it lists every field, built in or custom: Status, Bucket, Owner, Labels, Impact, Effort, dates, plus anything you added such as Domain or Committed. Group headers show a count and total score and click to collapse. A multi-select puts an idea under every option it carries. Dates group by month.

The **Board** has a "Columns" selector that switches its columns to any single select or checkbox field, so you can drag ideas between Domains or between Committed yes and no just as you drag them between statuses.

Grouping and column choices are remembered per view.

**Score** is RICE style: `reach × impact × (confidence ÷ 100) ÷ effort`. Impact and effort are 1 to 5, confidence is a percentage, reach is any number you choose (people, transactions, hours).

Filters and search apply to every view. Search covers titles, descriptions, labels, owners, insight text, and comments.

## Keyboard

| Key | Action |
| --- | --- |
| `N` | New idea |
| `/` | Focus search |
| `Esc` | Close panel or dialog |
| `↑` `↓` or `J` `K` | Previous / next idea while the panel is open |

## Data file

Plain JSON, one object with `name`, `seq`, a `fields` array of custom field definitions, and an `ideas` array. Each idea carries its fields plus `insights`, `comments`, and `history` arrays. Dates are `start` and `end` as `YYYY-MM-DD` strings; leave them empty for unscheduled ideas. Custom values live under `custom` keyed by field id. You can edit the file by hand or feed it to another tool. Statuses and buckets are fixed lists in the app: `parked`, `discovery`, `prioritized`, `delivery`, `shipped`, `wontdo` and `now`, `next`, `later`, `none`.

## Theme

Auto, Light, and Dark toggle in the rail. Auto follows the operating system.

## Not included

Multi-user editing and Jira Software integration. The delivery ticket field is free text so you can paste a key or a link.
