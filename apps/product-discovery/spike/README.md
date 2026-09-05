# Embed probe

`embed-probe.html` answers one question before any code gets written: can a page hosted on your own
domain, embedded in a SharePoint page, sign a user in and read SharePoint lists through Microsoft
Graph?

It matters because MSAL caches tokens in browser storage, and a sandboxed iframe makes reading that
storage throw rather than return nothing. If SharePoint's Embed web part sandboxes the frame, the
embedded approach cannot work at all, and it is much cheaper to learn that now.

## Running it

1. Put the file on your internal HTTPS host.
2. Open it directly as a top-level page. That is the baseline.
3. Embed the same URL in a SharePoint page with the Embed web part and run it again. **This is the
   result that decides the approach.**
4. Once an Entra app registration exists, fill in the client and tenant IDs and click **Sign in and
   test Graph**. Add a site such as `contoso.sharepoint.com:/sites/FinanceTech` to test the data
   path too.

Configuration is kept in the page URL, so a configured probe can be bookmarked and shared.

## Reading the result

| Result | Meaning |
| --- | --- |
| Opaque origin, or storage failures | The frame is sandboxed. Embedding will not work; open the app in its own tab instead |
| Cookies blocked, storage fine | Normal. The first sign-in each session uses a popup rather than being silent |
| All green, sign-in succeeds | The embedded path is viable |

Everything it does is a read. It writes nothing to your tenant.

## Status

The environment checks are tested in three contexts: top-level, a same-origin iframe and a
sandboxed iframe. The MSAL and Graph portions are **untested**, because the machine this was built
on has no Microsoft tenant and cannot reach `graph.microsoft.com`. Expect to fix small things on
first contact with a real tenant.

Background and the full plan: `docs/handoff/2026-09-04-hosted-page-graph.md`.
