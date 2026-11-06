# Git and pull requests

## Repositories

- New repositories are private unless the owner decides otherwise.

## Branches

- Never push to `main` directly. Create a branch and open a pull request for every change, so the owner can review it first.
- Start every branch from the latest `main`. Do not build a branch on top of another open pull request.
- Never rebase and never force-push. Rebasing rewrites history, which can break other branches and lose changes.
- If `main` moves on and the pull request conflicts with it, merge `main` into the branch and fix the conflict in a merge commit.

## Before pushing

- Run the repository's own checks (listed in its rule files) and make sure they pass. CI runs the same steps.
- Check the diff for personal information the owner has not approved and for secret values (see `publishing.md`).

## Pull requests

- Title and description in English.
- For a visible change, show before and after screenshots in the pull request.
- Watch CI on the pull request and fix failures until it passes. Do not skip or weaken a check to make it pass.
- The owner reviews and merges. Do not merge your own pull request unless the owner has said so for that task.
- If a new pull request replaces an older one, say in the report that the older one can be closed.
