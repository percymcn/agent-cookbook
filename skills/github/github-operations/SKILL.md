---
name: github-operations
description: "GitHub operations umbrella: authentication, repository setup, issues, pull requests, code review, CI, releases, and codebase inspection via gh, git, curl, and pygount. Use for any GitHub task that previously matched github-auth, github-issues, github-pr-workflow, github-code-review, github-repo-management, or codebase-inspection."
---

# GitHub Operations

Use this class-level skill for GitHub work. Prefer `gh` when authenticated; fall back to `git` plus the GitHub REST API with `GITHUB_TOKEN` when `gh` is unavailable.

## 1. Prerequisite discovery

```bash
git --version
gh --version 2>/dev/null || echo "gh not installed"
gh auth status 2>/dev/null || echo "gh not authenticated"
```

Inside a repository, derive owner/repo once:

```bash
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

If `gh` is unavailable, load `GITHUB_TOKEN` from the environment, `~/.hermes/.env`, or `~/.git-credentials` before REST calls.

## 2. Authentication patterns

- `gh auth login` for browser login; `echo "$TOKEN" | gh auth login --with-token` for headless hosts.
- For git-only HTTPS, configure `git config --global credential.helper store` and use a GitHub PAT as the password.
- For SSH, generate `ed25519`, add it at GitHub Settings → SSH keys, then verify with `ssh -T [REDACTED-EMAIL]`.
- Always configure commit identity before committing: `git config --global user.name` and `git config --global user.email`.

## 3. Repository management

Use `gh repo clone/create/fork/view/edit`, `gh release`, `gh workflow`, and `gh secret` when available. For fallback:

- Clone with plain `git clone`.
- Create/fork/edit repos with REST endpoints under `/user/repos`, `/orgs/{org}/repos`, `/repos/{owner}/{repo}`.
- Releases: `POST /repos/{owner}/{repo}/releases`.
- Workflows/runs: `/repos/{owner}/{repo}/actions/...`.
- Branch protection: `PUT /repos/{owner}/{repo}/branches/{branch}/protection`.

## 4. Issues

Common commands:

```bash
gh issue list --state open
gh issue view 42
gh issue create --title "..." --body "..." --label bug
gh issue edit 42 --add-label priority:high --add-assignee @me
gh issue comment 42 --body "..."
gh issue close 42 --reason completed
```

Fallback endpoints: `GET/POST/PATCH /repos/{owner}/{repo}/issues`, issue comments under `/issues/{n}/comments`, labels under `/issues/{n}/labels`, assignees under `/issues/{n}/assignees`. Remember GitHub's issues API also returns PRs; filter entries with a `pull_request` key when listing actual issues.

## 5. Pull request lifecycle

1. Start clean: `git fetch origin && git checkout main && git pull origin main`.
2. Branch: `git checkout -b feat/short-description`.
3. Make changes with file tools, run tests, and commit with Conventional Commits.
4. Push: `git push -u origin HEAD`.
5. Create PR: `gh pr create --title ... --body ...` or REST `POST /pulls`.
6. Monitor CI: `gh pr checks --watch`, `gh run view --log-failed`, or REST Actions/status endpoints.
7. Fix failures, commit, push, and re-check.
8. Merge with `gh pr merge --squash --delete-branch` when appropriate.

## 6. Code review

For local or PR review:

1. Get scope: `git diff main...HEAD --stat` and `git log main..HEAD --oneline`.
2. Read changed-file diffs and surrounding file context.
3. Check correctness, security, code quality, testing, performance, and documentation.
4. Run relevant tests/lints when feasible.
5. Report findings by severity: Critical, Warnings, Suggestions, Looks Good.

For GitHub PRs use `gh pr view`, `gh pr diff`, `gh pr checkout`, `gh pr review`, and `gh pr comment`. For inline REST comments, use the PR head SHA and `POST /repos/{owner}/{repo}/pulls/{pr}/comments` or an atomic review via `/pulls/{pr}/reviews`.

## 7. CI troubleshooting loop

When CI fails:

1. Identify failed workflow/job: `gh run list --branch $(git branch --show-current)`.
2. Fetch logs: `gh run view <RUN_ID> --log-failed`.
3. Fix root cause locally.
4. Commit and push.
5. Re-check status; repeat up to a bounded number of attempts before escalating.

## 8. Codebase inspection

Use `pygount` for LOC/language breakdowns. Always exclude dependency and build folders:

```bash
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party" \
  .
```

Pitfalls: Markdown is counted as comments, JSON counts can be conservative, and missing exclusions can make pygount crawl huge dependency trees.
