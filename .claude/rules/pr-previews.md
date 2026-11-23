# Pull request previews (website repositories)

The owner's rule (2026-11-07): every pull request in a repository that publishes a website gets a preview of the site, linked on the pull request. Repositories without a website (command-line tools, libraries, papers) do not.

The owner's decision (2026-11-23): previews have no `preview` path. They are on Cloudflare Pages, at the same paths as the live site, and a visit is told apart by its query (`?ref=pr-<number>`) and its host. The live sites stay on GitHub Pages.

## What every website repository does

- Its pull request workflow builds the site exactly as it would be published, checks it, and uploads it with `actions/upload-artifact` as the artifact `preview` (only for pull requests from the same repository, not forks or Dependabot).
- Its `previews.yml` calls the shared workflow `nguekwang/research-aide/.github/workflows/cloudflare-previews.yml@main`. When the pull request workflow passes for the latest commit of an open pull request, it uploads that `preview` artifact to the repository's Cloudflare Pages project with the branch name `pr-<number>`, so the preview is at `https://pr-<number>.<project>.pages.dev/`, and keeps one comment on the pull request (marker `<!-- preview-bot -->`) with its links. When the pull request is closed, it deletes the preview.
- Pull request code never runs where the Cloudflare token is: the shared workflow checks out nothing and refuses a preview that holds Pages Functions (`_worker.js`, `_routes.json`).
- Its `pages.yml` is the only workflow that deploys to GitHub Pages; it calls `pages-with-previews.yml@main` with `previews: false` and runs only for the live site (pushes to `main`, and whatever else changes the live site).
- Preview links carry `?ref=pr-<number>`. On the owner's sites this is the test ID of the pull request: visits with it, or on a `pages.dev` host, are review traffic and are left out of measurement results.
- Cloudflare sends `X-Robots-Tag: noindex` on every preview, so previews are not indexed.
- The Cloudflare free plan allows 20,000 files and 25 MiB per file in a deployment. A site whose preview is larger ships a smaller preview (for example only some generated pages) and says so in its own rules.
- Report the preview comment to the owner; do not post preview links by hand.
- `pages-with-previews.yml` still has the old GitHub Pages previews at `/preview/pr-<number>/` (`previews: true`, the default) until every website repository has moved; then that part is removed.

## Setting it up in a repository

The owner, once per repository: a Cloudflare Pages project made with "Direct Upload" (name `<site>-preview`), and the repository secrets `CLOUDFLARE_API_TOKEN` (a token with only "Account / Cloudflare Pages / Edit") and `CLOUDFLARE_ACCOUNT_ID`. Settings > Pages > Source must be "GitHub Actions". Then `.github/workflows/previews.yml`:

```yaml
name: previews
on:
  workflow_run:
    workflows: [site]   # the `name:` of the pull request workflow that uploads "preview"
    types: [completed]
  pull_request_target:
    types: [closed]     # deletes the preview; nothing of the pull request is checked out
permissions: {}
jobs:
  preview:
    permissions:
      actions: read
      pull-requests: write
    uses: nguekwang/research-aide/.github/workflows/cloudflare-previews.yml@main
    with:
      project: <site>-preview
      links: |
        Top page|
    secrets:
      CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
      CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

- `workflow_run` and `pull_request_target` use the workflow files of the default branch, so previews start once this file is merged.
- `pages.yml` calls `pages-with-previews.yml@main` with `build`, `site-dir` and `previews: false`.
- When a shared workflow changes, check that every website repository still deploys and previews.
- When the build needs data that must be fetched with a token (such as a list of releases from the GitHub API), fetch it in an earlier job of `pages.yml` with only the permissions it needs (`contents: read`), upload it with `actions/upload-artifact`, and pass `artifact: <name>` and `artifact-path: <folder>`; the shared workflow downloads it before the build. Never give the build itself a token: the publishing job can deploy.
