"""Verified git commits for the RBI Regulatory Archive.

Every commit this module makes is authored by Souvik Dey
<imsovikde@gmail.com> and signed with ``git commit -S`` so GitHub renders
the green Verified badge. The signing itself is done by the
crazy-max/ghaction-import-gpg@v6 step in the workflow, which imports the
owner's GPG key and sets ``commit.gpgsign``; this module only asserts that
the configuration is present and refuses to commit unsigned.

Rules enforced here, no exceptions:

- Never commit if there is nothing staged.
- Never force-push (no ``--force``, ever).
- Never touch ``.github/workflows/`` (workflow files are committed by the
  owner only, never by the conversion loop).
- Push goes to ``origin HEAD:main`` after a ``git pull --rebase``.
"""

from __future__ import annotations

import os
import subprocess
import time

__all__ = [
    "CommitError",
    "commit_batch",
    "configure_identity",
    "get_last_commit_sha",
    "verify_last_commit",
]

COMMIT_NAME = "Souvik Dey"
COMMIT_EMAIL = "imsovikde@gmail.com"
_MAX_PUSH_RETRIES = 3
_PUSH_PACING_SECONDS = 5


class CommitError(Exception):
    """A git identity, commit, rebase or push step failed."""


def _run(args, cwd, check=True):
    """Run a git command in ``cwd`` and return its stripped stdout."""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if check and result.returncode != 0:
        raise CommitError(
            f"git {' '.join(args)} failed (exit {result.returncode}): "
            f"{(result.stderr or result.stdout).strip()[:500]}"
        )
    return result.stdout.strip()


def _config_get(key, cwd):
    """Return a git config value (local, falling back to global), or ''."""
    result = subprocess.run(
        ["git", "config", "--get", key],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def configure_identity(name=None, email=None, cwd=None):
    """Set the commit identity and assert signing is enabled.

    Name/email come from the ``GIT_COMMIT_NAME`` / ``GIT_COMMIT_EMAIL``
    environment variables when set, else the explicit arguments, else the
    defaults Souvik Dey / imsovikde@gmail.com. Sets repo-local config so
    the runner's global git config is never modified.

    Raises CommitError unless ``commit.gpgsign`` is true and a signing key
    is configured, which means the GPG import step has not run yet.
    Returns (name, email).
    """
    cwd = cwd or os.getcwd()
    name = name or os.environ.get("GIT_COMMIT_NAME") or COMMIT_NAME
    email = email or os.environ.get("GIT_COMMIT_EMAIL") or COMMIT_EMAIL
    _run(["config", "user.name", name], cwd)
    _run(["config", "user.email", email], cwd)
    gpgsign = _config_get("commit.gpgsign", cwd)
    if gpgsign.lower() != "true":
        raise CommitError(
            "commit.gpgsign is not true; the GPG key import step "
            "(crazy-max/ghaction-import-gpg) has not run, refusing to "
            "commit unsigned."
        )
    signing_key = _config_get("user.signingkey", cwd)
    if not signing_key:
        raise CommitError(
            "no user.signingkey is configured; the GPG key import step "
            "has not run, refusing to commit unsigned."
        )
    return name, email


def _assert_safe_paths(paths):
    """Reject empty input and any path under .github/workflows/."""
    if not paths:
        raise CommitError("commit_batch called with no paths.")
    for path in paths:
        normalised = os.path.normpath(str(path)).replace(os.sep, "/")
        if normalised == ".github/workflows" or normalised.startswith(
            ".github/workflows/"
        ):
            raise CommitError(
                f"refusing to commit workflow file: {path} "
                "(.github/workflows/ is owner-only, never touched by "
                "the conversion loop)."
            )


def commit_batch(paths, message, cwd=None):
    """Stage exactly ``paths`` and push one signed commit.

    Steps: ``git add -- <paths>``; if nothing is staged, return False
    without committing. Otherwise ``git commit -S -m <message>``,
    ``git pull --rebase origin main``, then ``git push origin HEAD:main``
    with up to 3 retries and a 5 second pacing pause between attempts.
    Returns True when a commit was pushed, False when there was nothing
    to commit. Raises CommitError on any failure. Never force-pushes.
    """
    cwd = cwd or os.getcwd()
    _assert_safe_paths(paths)
    _run(["add", "--"] + [str(p) for p in paths], cwd)
    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=cwd,
        capture_output=True,
        timeout=60,
    )
    if staged.returncode == 0:
        return False  # nothing staged, nothing to commit
    _run(["commit", "-S", "-m", message], cwd)
    _run(["pull", "--rebase", "origin", "main"], cwd)
    last_error = None
    for attempt in range(_MAX_PUSH_RETRIES):
        if attempt:
            time.sleep(_PUSH_PACING_SECONDS)
        try:
            _run(["push", "origin", "HEAD:main"], cwd)
            return True
        except CommitError as exc:
            last_error = exc
    raise CommitError(
        f"git push failed after {_MAX_PUSH_RETRIES} attempts: {last_error}"
    )


def get_last_commit_sha(cwd=None):
    """Return the full SHA of HEAD, or '' when the repo has no commits."""
    cwd = cwd or os.getcwd()
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def verify_last_commit(cwd=None):
    """Return True only if HEAD carries a signature.

    Uses ``git log -1 --format=%G?``: "G" is a good signature, "U" is a
    good signature from an untrusted key (normal on a fresh runner where
    the key is not in the local trust database), "N" means no signature.
    Any other status, or an empty result, returns False.
    """
    cwd = cwd or os.getcwd()
    result = subprocess.run(
        ["git", "log", "-1", "--format=%G?"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30,
    )
    status = result.stdout.strip() if result.returncode == 0 else ""
    return status in ("G", "U")
