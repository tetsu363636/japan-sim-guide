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
- `../scripts/threads_auth.py`
  Threads OAuth helper for the one-time code exchange and later token refreshes.
- `../scripts/publish_threads.py`
  Threads publish helper for text, link, image, or video posts.
- `../scripts/hashnode_publication_id.py`
  Helper to resolve a Hashnode publication ID from its host.

## Suggested flow

1. Reissue the dev.to API key.
2. Create the Hashnode publication and resolve its publication ID.
3. Use the social preview image already added to the site so pasted links have a stronger preview.
4. Finish the Meta app setup once, exchange the code for a long-lived Threads token, and keep that token in your shell or scheduler.
5. Publish drafts first, then flip to live once the preview and canonical settings look correct.

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

Preview a Threads post request without publishing:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 scripts/publish_threads.py \
  --option 2 \
  --dry-run
```

Publish one of the saved Threads snippets:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 scripts/publish_threads.py \
  --option 2
```

Publish custom text with the source-tagged landing URL attached explicitly:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 scripts/publish_threads.py \
  --text "I turned the Japan SIM answer I kept repeating into a public guide for newcomers." \
  --link-attachment https://tetsu363636.github.io/japan-sim-guide/?src=threads
```

Refresh the long-lived token on a schedule:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 scripts/threads_auth.py refresh-token
```

Once the token is in place, the publish command is cron-friendly. Example:

```bash
THREADS_ACCESS_TOKEN=your_long_lived_token \
python3 /home/testuhirokankeko/japan-sim-guide/scripts/publish_threads.py \
  --option 1 \
  --output /tmp/threads-last-post.json
```

## Manual-only platforms

- Reddit
  Use the snippet as a base, keep the disclosure up top, and post manually from your own account.
- Quora
  Use the answer draft and add it to an existing question or a self-asked Q/A once you decide the wording.

## Threads notes

- The first Meta approval step is still manual.
  Open the URL from `threads_auth.py auth-url`, approve the app in a browser, and paste the returned `code` back into the CLI.
- Use the `?src=threads` landing URL somewhere in the post text or as `--link-attachment`.
  That keeps the tailored entry card active on the site.
- `publish_threads.py` defaults to the saved `threads-posts.txt` file, but you can also post from `--text`, `--text-file`, `--image-url`, or `--video-url`.
- If you later find that your app only accepts versioned endpoints, override the base with `THREADS_PUBLISH_BASE=https://graph.threads.net/v1.0`.

## Why the article draft is canonical-first

The article front matter points back to the main guide as the canonical URL. That helps the cross-post act like distribution, not a competing duplicate.
