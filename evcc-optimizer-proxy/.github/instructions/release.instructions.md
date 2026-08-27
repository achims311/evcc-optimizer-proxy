---
description: "Use when preparing a release, changing the add-on version, updating CHANGELOG.md, creating a Git tag, pushing a release, or modifying GitHub Actions workflows for EVCC Optimizer Proxy."
name: "EVCC Optimizer Proxy Release"
---
# Release And Changelog Rules

- Treat `config.yaml` as the release version source of truth.
- For every user-visible change, add an entry under `## <version>` in `CHANGELOG.md` before creating a release. Keep entries concise and user-focused.
- Keep `config.yaml` `changelog` pointing to the public `CHANGELOG.md` URL on the default branch.
- Before creating tag `vX.Y.Z`, set `config.yaml` to `version: X.Y.Z` and require a matching `## X.Y.Z` section in `CHANGELOG.md`.
- Do not reuse, move, or force-push an existing release tag. Increment the patch version for a new release.
- Use a project-local `.venv` for development and tests. Create it with `python3 -m venv .venv`, activate it with `. .venv/bin/activate`, then install `python -m pip install -r rootfs/app/requirements.txt -r requirements-dev.txt`.
- Before committing a release, run `python -m py_compile rootfs/app/*.py`, `python -m pytest -q`, and `git diff --check` from the activated `.venv`. Do not release when tests fail.
- Add or update focused `pytest` coverage for changed request handling, configuration, and forwarding behavior. Tests must not require a running Home Assistant instance or live optimizer endpoint.
- Before pushing, verify the release workflow remains at `.github/workflows/release.yml` and validates the tag/version match, changelog section, Python syntax, and `pytest -q`.
- After pushing `main` and the tag, verify `git status --short` is empty and confirm the remote branch and tag with `git ls-remote --heads --tags origin main vX.Y.Z`.
