# GPG Commit Signing — Setup Report

Repository: `imsovikde/rbi-regulatory-archive-1991-2026`
Owner: Souvik Dey (`imsovikde`)
Report date: 2026-11-13
Last verified: 2026-11-13 (Actions run `43377069291`, commit `e053334`)
Machine: Windows 11, Git for Windows 2.55.0.windows.5

This report is written for human maintainers and for AI agents working in this
repository. It records what was verified, how it was proven, and how to rotate
or revoke the setup.

**No private key, passphrase, or access token appears in this file, and none
may ever be added to this repository.**

---

## 1. Status at a glance

| Gate | Status | Evidence |
|---|---|---|
| GPG installed and working | PASS | `gpg (GnuPG) 2.5.24` |
| Dedicated key exists | PASS | `E3A0ABB6FBEC5840`, RSA 4096, expires 2028-11-12 |
| Global git signing config | PASS | `gpg.format=openpgp`, fingerprint pinned, `commit.gpgsign=true` |
| Local commit signature | PASS | `git log --show-signature` → `Good signature` |
| Public key on GitHub | PASS | Key added on the account; key ID confirmed on `settings/keys` |
| Commit Verified on GitHub | PASS | API: `verified: true`, `reason: valid` |
| Actions workflow committed | PASS | `.github/workflows/archive-update.yml`, state `active` |
| Actions secrets created | PASS | `GH_PAT`, `GPG_PASSPHRASE`, `GPG_PRIVATE_KEY` present (3/3) |
| Actions-signed commit proven | PASS | Run `43377069291` green; commit `e053334` → `verified: true`, `reason: valid` |

All gates pass as of 2026-11-13. Local commits are signed with the primary key;
Actions commits are signed with the signing subkey (see section 4.1). Both
chain to the same primary fingerprint and both verify on GitHub.

---

## 2. Key details

| Field | Value |
|---|---|
| Key ID | `E3A0ABB6FBEC5840` |
| Full fingerprint | `6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840` |
| Primary UID | `Souvik Dey <imsovikde@gmail.com>` |
| Algorithm | RSA 4096 (primary, signing/certifying) |
| Encryption subkey | `72BA468A855F34E2` |
| Created | 2026-11-13 |
| Expires | 2028-11-12 |
| GnuPG version | 2.5.24 |
| GnuPG home | `C:\Users\imsov\AppData\Roaming\gnupg` |
| Pinentry | `C:/Program Files/Gpg4win/bin/pinentry-w32.exe` (GUI dialog) |

This key is treated as a **dedicated signing key**, separate from any personal
key, so it can be revoked on its own without affecting other identities. It
already existed on the machine when this setup ran; it was reused, not
recreated, and no other key was modified or deleted.

The private key is protected by a passphrase held only by the owner. Automation
receives it exclusively through GitHub's encrypted secret store.

---

## 3. Effective global git configuration

```
user.name=Souvik Dey
user.email=imsovikde@gmail.com
user.signingkey=6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840!
gpg.format=openpgp
gpg.program=C:/Program Files/GnuPG/bin/gpg.exe
commit.gpgsign=true
```

Notes for future agents:

- `gpg.program` is `C:/Program Files/GnuPG/bin/gpg.exe` on this machine. The
  often-quoted `C:\Program Files (x86)\GnuPG\...` path does **not** exist here.
- The trailing `!` on `user.signingkey` forces use of the primary key by full
  fingerprint, which prevents ambiguity if another key shares the same UID.
- This machine previously used **SSH** commit signing (`gpg.format=ssh` with an
  `id_ed25519_signing.pub` key). It was switched to `openpgp`; `commit.gpgsign`
  was already `true`. Older repositories may still carry local overrides.
- `gpg.ssh.allowedsignersfile` remains set but is inert while
  `gpg.format=openpgp`.

---

## 4. Verified local commit

Root commit on `main`:

- SHA: `96291352ac3e5acad5ee8c24f56ae05262b3312f`
- Message: `Verify GPG signing`
- URL: https://github.com/imsovikde/rbi-regulatory-archive-1991-2026/commit/96291352ac3e5acad5ee8c24f56ae05262b3312f
- GitHub API verification: `verified: true`, `reason: valid`
- Author: `Souvik Dey <imsovikde@gmail.com>`
- Committer account: `imsovikde`

Local verification output:

```
gpg: Signature made 11/13/26 11:11:48 India Standard Time
gpg:                using RSA key 6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840
gpg: Good signature from "Souvik Dey <imsovikde@gmail.com>" [ultimate]
```

A second signed commit hardened the workflow's push target:

- SHA: `abced89be8ddc55dd7ce7e4c41a2b00649361b6d`
- Message: `Harden workflow push target for detached HEAD`
- GitHub API verification: `verified: true`, `reason: valid`

### 4.1 Actions-signed commit (end-to-end proof)

Workflow run: `43377069291` (`workflow_dispatch`, conclusion `success`, all
steps green).

- SHA: `e0533340ba0befea404d7b3bc595c2395756dd79`
- Message: `chore: archive update 2026-11-13`
- URL: https://github.com/imsovikde/rbi-regulatory-archive-1991-2026/commit/e0533340ba0befea404d7b3bc595c2395756dd79
- Author: `Souvik Dey <imsovikde@gmail.com>`
- Committer account: `imsovikde`
- GitHub API: `verified: true`, `reason: valid`, `verified_at`
  `2026-11-13T06:12:31Z`
- Runner log: `Signing key fingerprint: 6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840`

**Subkey detail:** the Actions signature names the signing subkey
`F9BF935234936DB36BCA5BAF72BA468A855F34E2` (`ssb`, RSA 4096, expires
2028-11-12). Local commits name the primary key because `user.signingkey` ends
with `!`. Both are the same key pair, both produce `Good signature`, and GitHub
verifies both. Do not treat the subkey ID as a different identity.

---

## 5. GitHub account configuration

- Public key: added at https://github.com/settings/keys, key ID
  `E3A0ABB6FBEC5840`, email `imsovikde@gmail.com`.
- `imsovikde@gmail.com` is confirmed **verified** on
  https://github.com/settings/emails, which is required for the green Verified
  badge.
- `main` is currently unprotected.

Verification of the account-side key is indirect but conclusive: GitHub reports
the pushed commits as `verified: true` with `reason: valid`. GitHub only returns
that verdict when the signature matches a GPG key on the account **and** the
commit email is verified.

---

## 6. GitHub Actions workflow

File: `.github/workflows/archive-update.yml`
Workflow name: `Archive update`
State: `active`

Key wiring:

```yaml
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.GH_PAT }}
    fetch-depth: 0

- uses: crazy-max/ghaction-import-gpg@v6
  with:
    gpg_private_key: ${{ secrets.GPG_PRIVATE_KEY }}
    passphrase: ${{ secrets.GPG_PASSPHRASE }}
    git_user_signingkey: true
    git_commit_gpgsign: true
    git_tag_gpgsign: true
    git_user_name: Souvik Dey
    git_user_email: imsovikde@gmail.com
```

The commit step runs `git commit -S`, so signing is explicit in addition to
`git_commit_gpgsign: true`, and pushes with `git push origin HEAD:main` so it
works even from a detached HEAD.

Triggers: daily schedule (`0 3 * * *`) and `workflow_dispatch`. Remove the
`schedule:` block if daily marker commits are not wanted.

The `Update archive metadata` step is a placeholder that writes
`.archive-runs/last-run.txt`. Replace it with the real archive ingestion step;
the signing and commit steps should stay as they are.

### Required secrets (names only)

| Secret | Purpose |
|---|---|
| `GPG_PRIVATE_KEY` | ASCII-armored export of the private key |
| `GPG_PASSPHRASE` | Passphrase protecting that key |
| `GH_PAT` | Fine-grained PAT used by `actions/checkout` to push |

Current state: **all three exist.** `gh api
repos/imsovikde/rbi-regulatory-archive-1991-2026/actions/secrets` returns
`total_count: 3` with names `GH_PAT`, `GPG_PASSPHRASE`, `GPG_PRIVATE_KEY`.
Values are write-only and were never recorded here.

---

## 7. Actions enablement — completed steps (kept for rotation)

These steps were completed on 2026-11-13 and are retained so the secrets can be
rotated later without rediscovering the procedure.

### 7.1 Create `GPG_PRIVATE_KEY`

In the owner's own terminal (never in a chat, never in a file inside this repo):

```powershell
gpg --armor --export-secret-keys 6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840 | Set-Clipboard
Set-Clipboard -Value ""   # clear afterwards
```

Paste into https://github.com/imsovikde/rbi-regulatory-archive-1991-2026/settings/secrets/actions
as a new repository secret named `GPG_PRIVATE_KEY`.

### 7.2 Create `GPG_PASSPHRASE`

Same page, name `GPG_PASSPHRASE`, value typed directly into the form.

### 7.3 Create `GH_PAT`

Fine-grained token at https://github.com/settings/personal-access-tokens/new:

- Token name: `rbi-archive-actions`
- Expiration: 90 days
- Resource owner: `imsovikde`
- Repository access: only `rbi-regulatory-archive-1991-2026`
- Repository permissions: `Contents` = Read and write; `Metadata` = Read-only
  (mandatory, automatic). `Workflows` is not required unless the workflow
  starts modifying files under `.github/workflows/`.
- Generate, copy once, paste as secret `GH_PAT`.

### 7.4 Prove the Actions path (completed — run `43377069291`)

```bash
gh workflow run archive-update.yml \
  --repo imsovikde/rbi-regulatory-archive-1991-2026

gh run list --repo imsovikde/rbi-regulatory-archive-1991-2026 --limit 3

gh api repos/imsovikde/rbi-regulatory-archive-1991-2026/commits/main \
  --jq '{sha: .sha, verified: .commit.verification.verified,
         reason: .commit.verification.reason,
         author: .commit.author.name, email: .commit.author.email}'
```

Success criteria: the run is green, the new commit is authored by
`Souvik Dey <imsovikde@gmail.com>`, and the API returns `verified: true` with
`reason: valid`.

If the run fails: read the failing step's log before changing anything. The
usual causes are a wrong passphrase, an unarmored or truncated private key, a
PAT without `Contents: Read and write`, or a PAT scoped to the wrong repository.

---

## 8. Verification commands (read-only)

```powershell
gpg --version
gpg --list-secret-keys --keyid-format=long
gpg --fingerprint 6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840
git config --global --get user.signingkey
git config --global --get gpg.format
git config --global --get commit.gpgsign
git log --show-signature -1
git verify-commit HEAD
```

```bash
gh api repos/imsovikde/rbi-regulatory-archive-1991-2026/commits/main \
  --jq '.commit.verification'
gh api repos/imsovikde/rbi-regulatory-archive-1991-2026/actions/secrets \
  --jq '{count: .total_count, names: [.secrets[].name]}'
gh api repos/imsovikde/rbi-regulatory-archive-1991-2026/actions/workflows \
  --jq '.workflows[] | {name, path, state}'
```

Secret **values** are write-only on GitHub and can never be read back by an
agent or by the repository owner through the API.

---

## 9. Security invariants

1. The private key, its passphrase, and the PAT exist only in the owner's
   keyring and in GitHub's encrypted Actions secret store.
2. No secret value is committed to this repository. `.gitignore` blocks common
   key-export filenames as a second line of defence.
3. The signing key is dedicated to this purpose and can be revoked
   independently of any other key.
4. The PAT is fine-grained, limited to this one repository, limited to
   `Contents: Read and write`, and expires after 90 days.
5. `GH_PAT` is used instead of the default `GITHUB_TOKEN` so signed commits are
   attributed to the owner's account and can trigger downstream workflows.

---

## 10. Revocation runbook

If the key or passphrase is ever exposed:

1. Revoke the public key on GitHub: https://github.com/settings/keys →
   delete `E3A0ABB6FBEC5840`. This immediately stops new commits from showing
   Verified.
2. Delete the Actions secrets `GPG_PRIVATE_KEY` and `GPG_PASSPHRASE`.
3. Revoke the `GH_PAT` token at
   https://github.com/settings/personal-access-tokens and create a replacement.
4. Optionally publish a revocation certificate so third parties learn the key
   is dead:

   ```powershell
   gpg --gen-revoke 6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840 > revocation.asc
   gpg --import revocation.asc
   ```

   Keep `revocation.asc` out of the repository.
5. Generate a fresh dedicated key, add it to GitHub, and update
   `user.signingkey` plus the `GPG_PRIVATE_KEY` secret.

Rotating the PAT every 90 days is expected and does not require touching the
GPG key.

---

## 11. Handoff summary

- Manual commits from this machine are signed and Verified.
- Actions commits are signed and Verified. Proof: run `43377069291`, commit
  `e0533340ba0befea404d7b3bc595c2395756dd79` (`verified: true`,
  `reason: valid`, author `Souvik Dey <imsovikde@gmail.com>`).
- All three secrets exist: `GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`, `GH_PAT`.
- Nothing is pending. Routine maintenance only: rotate `GH_PAT` before its
  90-day expiry, and renew the GPG key before 2028-11-12.
- To re-verify at any time, run the read-only commands in section 8.
