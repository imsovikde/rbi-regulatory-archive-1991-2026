#!/usr/bin/env bash
# setup_verified_signing.sh
#
# Local one-command provisioning script for the RBI Regulatory Archive.
# A human runs this on their OWN machine to (re)create the GPG signing
# setup used by the GitHub Actions workflows in this repository.
#
# What it does:
#   1. Checks that gpg, git (and gh, for the secret commands) exist.
#   2. Generates a dedicated RSA 4096 GPG key for imsovikde@gmail.com,
#      but ONLY if no secret key for that email exists yet.
#   3. Configures git globally for Verified commits as Souvik Dey.
#   4. Prints the exact commands to register the public key on GitHub
#      and to store the three secrets (GPG_PRIVATE_KEY, GPG_PASSPHRASE,
#      GH_PAT). Secret VALUES are never embedded here and never printed;
#      the gh commands prompt for them interactively.
#   5. Verifies the setup with git log --show-signature when run inside
#      a repository that already has signed commits.
#
# Safety rules enforced by this script:
#   - It refuses to run with --yes / -y (no unattended runs).
#   - It refuses to run non-interactively (stdin must be a terminal).
#   - It asks for an explicit YES before doing anything.
#   - It never prints a private key, passphrase, or token.
#
# Usage: bash scripts/setup_verified_signing.sh
# Run it from anywhere. Do NOT pipe secrets into it.
set -euo pipefail

REPO="imsovikde/rbi-regulatory-archive-1991-2026"
NAME="Souvik Dey"
EMAIL="imsovikde@gmail.com"

# Refuse unattended runs.
for arg in "$@"; do
  if [ "$arg" = "--yes" ] || [ "$arg" = "-y" ]; then
    echo "ERROR: this script refuses --yes / -y. Run it interactively." >&2
    exit 2
  fi
done
if [ ! -t 0 ]; then
  echo "ERROR: stdin is not a terminal. Run this script interactively in a terminal." >&2
  exit 2
fi

command -v gpg >/dev/null 2>&1 || { echo "ERROR: gpg is not installed. Install Gpg4win (Windows) or gnupg (Linux/macOS) first." >&2; exit 1; }
command -v git >/dev/null 2>&1 || { echo "ERROR: git is not installed." >&2; exit 1; }
if ! command -v gh >/dev/null 2>&1; then
  echo "WARNING: gh (GitHub CLI) is not installed. The secret commands below will not run until you install it."
  echo "You can still add the secrets by hand at https://github.com/${REPO}/settings/secrets/actions"
fi

echo "RBI Regulatory Archive: verified signing setup"
echo "Repo:  ${REPO}"
echo "Name:  ${NAME}"
echo "Email: ${EMAIL}"
echo ""
echo "This script will create (only if missing) a dedicated RSA 4096 GPG key,"
echo "configure git for signed commits, and print the commands that store the"
echo "secrets on GitHub. It never prints a secret value."
echo ""
read -r -p "Type YES to continue: " CONFIRM
if [ "$CONFIRM" != "YES" ]; then
  echo "Aborted. Nothing was changed."
  exit 0
fi

# Find an existing secret key for this email, if any.
KEYID="$(gpg --list-secret-keys --keyid-format=long --with-colons "$EMAIL" 2>/dev/null \
  | awk -F: '/^sec:/ {print $5; exit}' || true)"

if [ -n "${KEYID:-}" ]; then
  echo ""
  echo "A secret GPG key already exists for ${EMAIL}: ${KEYID}"
  echo "No new key will be generated. Reusing the existing key."
else
  echo ""
  echo "No secret GPG key found for ${EMAIL}. Generating a dedicated RSA 4096 key (expires in 2 years)."
  read -r -s -p "Choose a strong passphrase for the new GPG key: " PASSPHRASE
  echo ""
  read -r -s -p "Type the passphrase again to confirm: " PASSPHRASE2
  echo ""
  if [ "$PASSPHRASE" != "$PASSPHRASE2" ]; then
    echo "ERROR: passphrases do not match. Nothing was changed." >&2
    exit 1
  fi
  unset PASSPHRASE2
  gpg --batch --pinentry-mode loopback --passphrase "$PASSPHRASE" \
    --quick-gen-key "${NAME} <${EMAIL}>" rsa4096 default 2y
  unset PASSPHRASE
  KEYID="$(gpg --list-secret-keys --keyid-format=long --with-colons "$EMAIL" \
    | awk -F: '/^sec:/ {print $5; exit}')"
  echo "Generated key: ${KEYID}"
fi

echo ""
echo "Key fingerprint:"
gpg --fingerprint "$KEYID"
echo ""

git config --global user.name "$NAME"
git config --global user.email "$EMAIL"
git config --global user.signingkey "$KEYID"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
echo "Git configured: user.name, user.email, user.signingkey=${KEYID}, commit.gpgsign=true"

echo ""
echo "=== STEP 1: register the PUBLIC key on GitHub (safe to share) ==="
echo "Run this to print the public key, then paste it at"
echo "https://github.com/settings/keys -> New GPG key"
echo ""
echo "  gpg --armor --export ${KEYID}"
echo ""
echo "=== STEP 2: store the three secrets (values are prompted, never shown) ==="
echo "Run each command and paste the value when prompted."
echo "Nothing below contains a secret value."
echo ""
echo "  # Private key (armored export, piped straight into the secret):"
echo "  gpg --armor --export-secret-keys ${KEYID} | gh secret set GPG_PRIVATE_KEY --repo ${REPO}"
echo ""
echo "  # Passphrase you chose above:"
echo "  gh secret set GPG_PASSPHRASE --repo ${REPO}"
echo ""
echo "  # Fine-grained PAT for this repo only (Contents: Read and write, 90-day expiry):"
echo "  gh secret set GH_PAT --repo ${REPO}"
echo ""
echo "  # Optional, for the weekly Hugging Face backfill only:"
echo "  gh secret set HF_TOKEN --repo ${REPO}"
echo ""
echo "=== STEP 3: verify ==="
echo "Make one signed test commit in this repo, push it, and run:"
echo "  git log --show-signature -1"
echo "You must see 'Good signature' and author '${NAME} <${EMAIL}>'."
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo ""
  echo "Latest commit signature in this repository:"
  git log --show-signature -1 || echo "(no commits yet in this repository)"
fi
echo ""
echo "Done. If the test commit shows a good signature from ${KEYID}, the setup is complete."
