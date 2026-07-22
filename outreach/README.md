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
- `../scripts/publish_devto.py`
  dev.to draft/publish helper.
- `../scripts/publish_hashnode.py`
  Hashnode draft/publish helper.
- `../scripts/hashnode_publication_id.py`
  Helper to resolve a Hashnode publication ID from its host.

## Suggested flow

1. Reissue the dev.to API key.
2. Create the Hashnode publication and resolve its publication ID.
3. Use the social preview image already added to the site so pasted links have a stronger preview.
4. Publish drafts first, then flip to live once the preview and canonical settings look correct.

## Source-tagged landing URLs

Use a source tag in the shared URL so the site can show the matching entry path:

- Reddit: `https://tetsu363636.github.io/japan-sim-guide/?src=reddit`
- Quora: `https://tetsu363636.github.io/japan-sim-guide/?src=quora`
- Threads: `https://tetsu363636.github.io/japan-sim-guide/?src=threads`
- dev.to / Hashnode article links: `https://tetsu363636.github.io/japan-sim-guide/?src=article`

The same rule also works for language-specific pages, for example:

- Spanish from Reddit: `https://tetsu363636.github.io/japan-sim-guide/es/?src=reddit`
- Thai from Threads: `https://tetsu363636.github.io/japan-sim-guide/th/?src=threads`

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

## Manual-only platforms

- Reddit
  Use the snippet as a base, keep the disclosure up top, and post manually from your own account.
- Quora
  Use the answer draft and add it to an existing question or a self-asked Q/A once you decide the wording.
- Threads
  Paste one of the short posts after the Meta app and token setup is complete. First confirm the shared URL shows the new preview card and keep the `?src=threads` tag in place.

## Why the article draft is canonical-first

The article front matter points back to the main guide as the canonical URL. That helps the cross-post act like distribution, not a competing duplicate.
