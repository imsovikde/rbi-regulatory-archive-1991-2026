# Contributing to RBI DOC MCP

Thank you for your interest in contributing to the Reserve Bank of India Regulatory Model Context Protocol server.

## Ground Rules and Verification Requirements

1. Deterministic Verification: All pull requests must pass local tests (`npm test`) and the live edge backtest (`python test/live_backtest.py`) before review.
2. Verified Commits: All commits must be signed using GPG or SSH keys matching your GitHub profile.
3. Writing Standard: Documentation and commit messages must avoid promotional prose, em dashes, en dashes, and filler words. State facts directly.
4. Token Budget: Any changes to Plane 1 Code Mode API definitions must keep total token footprint strictly below 900 tokens.

## Development Workflow

1. Fork and clone the repository.
2. Install dependencies:
   ```bash
   npm ci
   ```
3. Run the local unit test suite:
   ```bash
   npm test
   ```
4. Verify edge compatibility:
   ```bash
   python test/live_backtest.py
   ```
5. Build using Cloudflare CLI:
   ```bash
   cf build
   ```

## Pull Request Submission

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Commit your changes with clear, descriptive commit messages.
3. Push to your fork and submit a Pull Request targeting `main`.
4. Ensure all continuous integration checks pass.
