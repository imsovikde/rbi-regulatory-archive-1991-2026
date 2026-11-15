#!/usr/bin/env python3
"""Hugging Face Scheduled Sync & Upstream Dataset Watcher.

Staged copy under _pipeline/hf_sync/ for autonomous scheduled runs.
"""

from __future__ import annotations

import os
import sys

# Re-export and delegate to scripts/hf_scheduled_sync.py
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from hf_scheduled_sync import main, sync_hf_dataset

if __name__ == "__main__":
    sys.exit(main())
