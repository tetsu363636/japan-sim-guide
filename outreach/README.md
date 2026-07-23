# Outreach Bundle

This folder reduces the amount of work left after the one-time account and auth steps are done.

## What is here

- `articles/japan-sim-guide-en.md`
  Canonical-first article draft for dev.to or Hashnode.
- `snippets/reddit-movingtojapan.md`
  Manual Reddit post copy with disclosure already included.
- `snippets/quora-answer.md`
  Manual Quora answer draft.
- `snippets/threads-posts.txt`
  Short post options for Threads once the Meta app flow is ready.
- `snippets/bluesky-posts.txt`
  Short post options for Bluesky when you want a compact social post with the same strategy.
- `campaigns/japan-sim-guide.json`
  Central campaign brief that defines the soft-sell positioning, proof points, platform modes, and post angles.
- `../scripts/publish_devto.py`
  dev.to draft/publish helper.
- `../scripts/publish_hashnode.py`
  Hashnode draft/publish helper.
- `../scripts/threads_auth.py`
  Threads OAuth helper for the one-time code exchange and later token refreshes.
- `../scripts/publish_threads.py`
  Threads publish helper for text, link, image, or video posts.
- `../scripts/publish_bluesky.py`
  Bluesky publish helper for App Password-based posting with optional external link cards.
- `../scripts/outreach_campaign.py`
  Central campaign runner that renders strategy-aligned posts per platform and dispatches the API-backed ones.
- `../scripts/hashnode_publication_id.py`
  Helper to resolve a Hashnode publication ID from its host.

## Suggested flow

1. Reissue the dev.to API key.
2. Create the Hashnode publication and resolve its publication ID.
3. Use the social preview image already added to the site so pasted links have a stronger preview.
4. Create a Bluesky App Password once and keep it in your shell or scheduler.
5. Finish the Meta app setup once, exchange the code for a long-lived Threads token, and keep that token in your shell or scheduler.
6. Publish drafts first, then flip to live once the preview and canonical settings look correct.

## Strategy-driven runner

The campaign runner sits above the individual platform scripts.

- One JSON brief defines the positioning, disclosure language, proof points, source-tagged URLs, and reusable post angles.
- `bluesky` can auto-post as soon as you have a handle and App Password.
- The same JSON can also define a playbook, so the recommended launch order lives next to the messaging itself.
- `threads` can be auto-posted immediately once the long-lived token is ready.
- `reddit` and `quora` stay export-first: the runner prepares the full draft so the only manual step left is pasting it into the platform.
- `dev.to` and `hashnode` reuse the canonical article draft that already points back to the main site.

## Source-tagged landing URLs

Use a source tag in the shared URL so the site can show the matching entry path:

- Reddit: `https://tetsu363636.github.io/japan-sim-guide/?src=reddit`
- Quora: `https://tetsu363636.github.io/japan-sim-guide/?src=quora`
- Threads: `https://tetsu363636.github.io/japan-sim-guide/?src=threads`
- Bluesky: `https://tetsu363636.github.io/japan-sim-guide/?src=bluesky`
- dev.to / Hashnode article links: `https://tetsu363636.github.io/japan-sim-guide/?src=article`

The same rule also works for language-specific pages, for example:

- Spanish from Reddit: `https://tetsu363636.github.io/japan-sim-guide/es/?src=reddit`
- Thai from Threads: `https://tetsu363636.github.io/japan-sim-guide/th/?src=threads`
- English from Bluesky: `https://tetsu363636.github.io/japan-sim-guide/?src=bluesky`

## Commands

Preview the dev.to payload:

```bash
python3 scripts/publish_devto.py \
  --file outreach/articles/japan-sim-guide-en.md \
  --dry-run
```

Create a live dev.to post:

```bash
DEVTO_API_KEY=your_key_here \
python3 scripts/publish_devto.py \
  --file outreach/articles/japan-sim-guide-en.md \
  --publish
```

Resolve a Hashnode publication ID from the host:

```bash
python3 scripts/hashnode_publication_id.py \
  --host yourblog.hashnode.dev
```

Preview the Hashnode mutation:

```bash
python3 scripts/publish_hashnode.py \
  --file outreach/articles/japan-sim-guide-en.md \
  --publication-id your_publication_id \
  --dry-run
```

Create a Hashnode draft:

```bash
HASHNODE_PAT=your_pat_here \
python3 scripts/publish_hashnode.py \
  --file outreach/articles/japan-sim-guide-en.md \
  --publication-id your_publication_id
```

Publish directly on Hashnode:

```bash
HASHNODE_PAT=your_pat_here \
python3 scripts/publish_hashnode.py \
  --file outreach/articles/japan-sim-guide-en.md \
  --publication-id your_publication_id \
  --publish
```

Build the Threads authorization URL for the first manual approval:

```bash
THREADS_APP_ID=your_app_id \
THREADS_REDIRECT_URI=https://your-redirect.example/callback \
python3 scripts/threads_auth.py auth-url
```

Exchange the returned `code` for a short-lived token and immediately upgrade it:

```bash
THREADS_APP_ID=your_app_id \
THREADS_APP_SECRET=your_app_secret \
THREADS_REDIRECT_URI=https://your-redirect.example/callback \
python3 scripts/threads_auth.py exchange-code \
  --code copied_from_redirect \
  --long-lived
```

Sanity-check the long-lived token:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 scripts/threads_auth.py profile
```

List the saved Threads snippet options:

```bash
python3 scripts/publish_threads.py --list-options
```

List the saved Bluesky snippet options:

```bash
python3 scripts/publish_bluesky.py --list-options
```

Preview a direct Bluesky post with an external link card:

```bash
python3 scripts/publish_bluesky.py \
  --option 2 \
  --external-url https://tetsu363636.github.io/japan-sim-guide/?src=bluesky \
  --external-title "Japan SIM Guide" \
  --external-description "Honest Rakuten vs docomo / au / SoftBank comparison, newcomer signup checklist, and monthly cost calculator in 11 languages." \
  --dry-run
```

Publish directly on Bluesky with an App Password:

```bash
BLUESKY_HANDLE=your.handle.bsky.social \
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx \
python3 scripts/publish_bluesky.py \
  --option 2 \
  --external-url https://tetsu363636.github.io/japan-sim-guide/?src=bluesky \
  --external-title "Japan SIM Guide" \
  --external-description "Honest Rakuten vs docomo / au / SoftBank comparison, newcomer signup checklist, and monthly cost calculator in 11 languages."
```

List the campaign angles, platforms, and supported landing languages:

```bash
python3 scripts/outreach_campaign.py list
```

Validate every Threads and Bluesky variant plus the playbook references in one shot:

```bash
python3 scripts/outreach_campaign.py validate
```

Render one strategy-based Threads post:

```bash
python3 scripts/outreach_campaign.py render \
  --platform threads \
  --angle arrival-friction \
  --landing-language en
```

Render one strategy-based Bluesky post:

```bash
python3 scripts/outreach_campaign.py render \
  --platform bluesky \
  --angle honest-comparison \
  --landing-language en
```

Render a full outreach bundle for review:

```bash
python3 scripts/outreach_campaign.py bundle \
  --landing-language en \
  --output-dir /tmp/jsg-outreach
```

Show the recommended launch sequence:

```bash
python3 scripts/outreach_campaign.py playbook --name launch
```

Show the current social-only weekly plan for direct traffic:

```bash
python3 scripts/outreach_campaign.py playbook \
  --name social-direct-week-2026-07-23
```

Materialize the launch playbook into a ready-to-use folder:

```bash
python3 scripts/outreach_campaign.py playbook \
  --name launch \
  --output-dir /tmp/jsg-launch-playbook
```

Materialize the social-only weekly plan into a ready-to-use folder:

```bash
python3 scripts/outreach_campaign.py playbook \
  --name social-direct-week-2026-07-23 \
  --output-dir /tmp/jsg-social-week
```

Export a Reddit draft that matches the strategy but still leaves the final posting click to you:

```bash
python3 scripts/outreach_campaign.py dispatch \
  --platform reddit \
  --angle honest-comparison \
  --landing-language en \
  --output-dir /tmp/jsg-outreach
```

Preview a Threads post request without publishing:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 scripts/outreach_campaign.py dispatch \
  --platform threads \
  --angle arrival-friction \
  --dry-run
```

Publish a strategy-based Threads post:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 scripts/outreach_campaign.py dispatch \
  --platform threads \
  --angle honest-comparison \
  --landing-language en
```

Preview a strategy-based Bluesky post request without publishing:

```bash
BLUESKY_HANDLE=your.handle.bsky.social \
python3 scripts/outreach_campaign.py dispatch \
  --platform bluesky \
  --angle arrival-friction \
  --landing-language en \
  --dry-run
```

Publish a strategy-based Bluesky post:

```bash
BLUESKY_HANDLE=your.handle.bsky.social \
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx \
python3 scripts/outreach_campaign.py dispatch \
  --platform bluesky \
  --angle honest-comparison \
  --landing-language en
```

Refresh the long-lived token on a schedule:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 scripts/threads_auth.py refresh-token
```

Once the token is in place, the publish command is cron-friendly. Example:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 /home/testuhirokankeko/japan-sim-guide/scripts/outreach_campaign.py dispatch \
  --platform threads \
  --angle multilingual-helper \
  --landing-language en \
  --output /tmp/threads-last-post.json
```

Create a dev.to draft from the canonical article through the same runner:

```bash
DEVTO_API_KEY=your_key_here \
python3 scripts/outreach_campaign.py dispatch \
  --platform devto
```

Publish directly on dev.to:

```bash
DEVTO_API_KEY=your_key_here \
python3 scripts/outreach_campaign.py dispatch \
  --platform devto \
  --publish
```

Create a Hashnode draft through the same runner:

```bash
HASHNODE_PAT=your_pat_here \
HASHNODE_PUBLICATION_ID=your_publication_id \
python3 scripts/outreach_campaign.py dispatch \
  --platform hashnode
```

Publish directly on Hashnode:

```bash
HASHNODE_PAT=your_pat_here \
HASHNODE_PUBLICATION_ID=your_publication_id \
python3 scripts/outreach_campaign.py dispatch \
  --platform hashnode \
  --publish
```

## Manual-only platforms

- Reddit
  Use `outreach_campaign.py dispatch --platform reddit` to generate the full draft, keep the disclosure up top, and post manually from your own account.
- Quora
  Use `outreach_campaign.py dispatch --platform quora` to generate the answer draft and then add it to an existing question or a self-asked Q/A.

## Bluesky notes

- Bluesky automation only needs a handle plus an App Password.
  Create the App Password in your Bluesky settings and keep using that instead of your main account password.
- The campaign runner attaches the `?src=bluesky` landing URL as an external card automatically.
  That keeps the source-aware entry path active without spending post characters on a raw URL.
- `publish_bluesky.py` can also add rich-text link facets if your text includes raw URLs.
  Leave that on unless you have a reason to post plain text only.
- If the strategic angle changes, update `campaigns/japan-sim-guide.json` first.
  The runner will reuse that same brief across Bluesky, Threads, Reddit, Quora, dev.to, and Hashnode.

## Current social-only plan

- Use the `social-direct-week-2026-07-23` playbook when the focus is direct traffic from Bluesky and Threads instead of backlinks.
- That playbook already encodes the July 24-29, 2026 posting windows, platform split, English-first order, and the final Spanish multilingual test.
- The prerequisites inside the playbook assume dev.to, Hashnode, Reddit, and Quora are out of scope for this week.

## Threads notes

- The first Meta approval step is still manual.
  Open the URL from `threads_auth.py auth-url`, approve the app in a browser, and paste the returned `code` back into the CLI.
- Use the `?src=threads` landing URL somewhere in the post text or as `--link-attachment`.
  That keeps the tailored entry card active on the site.
- If the strategic angle changes, update `campaigns/japan-sim-guide.json` first.
  The runner will reuse that same brief across Threads, Bluesky, Reddit, Quora, dev.to, and Hashnode.
- If the execution order changes, update the `playbooks` section in the same JSON.
  That keeps the posting sequence and the messaging source in one place.
- `publish_threads.py` defaults to the saved `threads-posts.txt` file, but you can also post from `--text`, `--text-file`, `--image-url`, or `--video-url`.
- If you later find that your app only accepts versioned endpoints, override the base with `THREADS_PUBLISH_BASE=https://graph.threads.net/v1.0`.

## Why the article draft is canonical-first

The article front matter points back to the main guide as the canonical URL. That helps the cross-post act like distribution, not a competing duplicate.
