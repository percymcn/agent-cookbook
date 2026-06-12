---
name: macos-storage-audit
description: Audit and triage disk usage on Purse's macOS agents without deleting anything prematurely.
version: 1.0.0
author: Hermes Agent
---

# macOS Storage Audit

Use this when Purse asks what is taking up storage, whether the Mac is low on disk, or what can be safely cleaned. The goal is to report real evidence first, then propose cleanup tiers. Do **not** delete data unless Purse explicitly asks for cleanup.

## Workflow

1. **Check real capacity first**
   ```bash
   df -h /
   df -h
   diskutil apfs list
   diskutil info /
   ```
   On APFS, the root `/` volume can look smaller than the Data volume. Pay attention to the APFS container total, Data volume usage, and free space.

2. **Check snapshots**
   ```bash
   tmutil listlocalsnapshots /
   ```
   Local snapshots can consume space, but do not assume they exist.

3. **Find top consumers with bounded scans**
   Full `du` scans can hang on macOS because of permission-protected folders and huge trees. Prefer targeted and timeout-bounded checks:
   ```bash
   du -sh /Users/pharma6/.cache /Users/pharma6/.npm /Users/pharma6/.ollama /Users/pharma6/.colima 2>/dev/null
   du -sh "/Users/pharma6/Library/Application Support"/* 2>/dev/null | sort -h | tail -30
   du -sh /Users/pharma6/* /Users/pharma6/.[!.]* 2>/dev/null | sort -h | tail -50
   ```
   If a broad scan times out, continue with narrower directories instead of waiting indefinitely.

4. **Distinguish apparent vs allocated size**
   Sparse VM files can look enormous but not consume that much physical disk. For Docker/VM images, inspect allocated blocks:
   ```bash
   python3 - <<'PY'
   import os
   p='/Users/pharma6/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw'
   st=os.stat(p)
   print(f'apparent={st.st_size/1024/1024/1024:.2f} GB')
   print(f'allocated={st.st_blocks*512/1024/1024/1024:.2f} GB')
   PY
   ```
   Do not call a sparse `Docker.raw` the main culprit unless allocated size is also high.

5. **Check container/model stores**
   Common large directories on Purse's Mac agents:
   - Colima/Lima: `/Users/pharma6/.colima/_lima`, especially `_disks`
   - Ollama models: `/Users/pharma6/.ollama/models/blobs`
   - HuggingFace cache: `/Users/pharma6/.cache/huggingface`
   - uv cache: `/Users/pharma6/.cache/uv`
   - npm npx cache: `/Users/pharma6/.npm/_npx`
   - Claude app VM bundles: `/Users/pharma6/Library/Application Support/Claude/vm_bundles`
   - oversized logs, e.g. project `logs/*.log`

6. **Report cleanup tiers**
   - **Safe/low risk:** package caches, npx cache, old logs, temporary browser screenshots.
   - **Medium risk:** model caches (HuggingFace/Ollama) if local models are not needed immediately.
   - **High impact but verify first:** Colima/Lima VM disks, Docker data, Claude VM bundles, GitHub runners/workspaces.

7. **When Purse explicitly says something “has to go,” execute deletion and verify**
   Treat direct language like “Colima and Ollama gotta go” as deletion approval for those named targets. Stop relevant services/processes first, remove the named storage roots, then verify free space and path absence before reporting. See `references/container-model-store-cleanup.md` for the Colima/Ollama pattern and concise reporting shape.

## Reporting style

Purse prefers concise, action-oriented results:

- Lead with free space and urgency.
- List top storage consumers with sizes and paths.
- Separate “safe cleanup now” from “needs approval/verification.”
- Avoid long raw dumps; keep evidence in bullets.
- If recommending deletion, state expected reclaimed GB and risk.

## Guardrails

- Never delete, prune Docker/Colima, remove models, or truncate logs without explicit cleanup approval.
- Before deleting container/VM data, check whether Docker/Colima processes are running and whether active projects depend on them.
- Before removing models, list model names/blobs where possible and ask if local inference is still needed.
- Do not treat `command not found`, permission errors, or timeout from a broad scan as durable facts; switch to a narrower scan.
