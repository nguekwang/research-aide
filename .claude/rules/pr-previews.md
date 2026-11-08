# Pull request previews (website repositories)

The owner's rule (2026-11-07): every pull request in a repository that publishes a website gets a preview of the site, linked on the pull request. Repositories without a website (command-line tools, libraries, papers) do not.

## What every website repository does

- Its pull request workflow builds the site exactly as it would be published, checks it, and uploads it with `actions/upload-artifact` as the artifact `preview` (only for pull requests from the same repository, not forks or Dependabot). All links inside the site must be relative, so the copy works under `/preview/pr-<number>/`.
- Its `pages.yml` is the only workflow that deploys to GitHub Pages, and it calls the shared workflow `nguekwang/research-aide/.github/workflows/pages-with-previews.yml@main`. That workflow builds the live site from the default branch, adds the latest passing preview of every open pull request at `/preview/pr-<number>/` (adding `<meta name="robots" content="noindex">` to every page that lacks it), deploys, and keeps one comment on each pull request (marker `<!-- preview-bot -->`) with its links.
- Preview links carry `?ref=pr-<number>`. On the owner's sites this is the test ID of the pull request: visits with it, or under `/preview/`, are review traffic and are left out of measurement results.
- Pages allows 1 GB per site. A site whose preview is large ships a smaller preview (for example only some generated pages) and says so in its own rules; previews that do not fit under `size-limit-mb` are left out with a note on the pull request.
- Report the preview comment to the owner; do not post preview links by hand.

## Setting it up in a repository

Settings > Pages > Source must be "GitHub Actions". Then `.github/workflows/pages.yml`:

```yaml
name: pages
on:
  push:
    branches: [main]
  workflow_run:
    workflows: [site]   # the `name:` of the pull request workflow that uploads "preview"
    types: [completed]
  pull_request_target:
    types: [closed]     # drops the preview; the shared workflow checks out main, never the pull request
  workflow_dispatch:
permissions:
  contents: read
jobs:
  publish:
    if: github.event_name != 'workflow_run' || (github.event.workflow_run.event == 'pull_request' && github.event.workflow_run.conclusion == 'success')
    concurrency:
      group: pages
      cancel-in-progress: false
    permissions:
      contents: read
      actions: read
      pull-requests: write
      pages: write
      id-token: write
    uses: nguekwang/research-aide/.github/workflows/pages-with-previews.yml@main
    with:
      build: |
        <commands that check and build the site>
      site-dir: <build output directory>
      preview-workflow: site.yml
      links: |
        Top page|
```

- `workflow_run` and `pull_request_target` use the workflow files of the default branch, so previews start once this file is merged.
- When the shared workflow changes, check that every website repository still deploys.
- When the build needs data that must be fetched with a token (such as a list of releases from the GitHub API), fetch it in an earlier job of `pages.yml` with only the permissions it needs (`contents: read`), upload it with `actions/upload-artifact`, and pass `artifact: <name>` and `artifact-path: <folder>`; the shared workflow downloads it before the build. Never give the build itself a token: the publishing job can deploy and comment.
