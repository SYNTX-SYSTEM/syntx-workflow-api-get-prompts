# Log Rotation Scripts

## Deployment

Scripts are deployed via **symlink**:
```
/opt/syntx-config/scripts -> /opt/syntx-workflow-api-get-prompts/scripts
```

This means:
- **Git is source of truth**
- `git pull` updates scripts immediately (no manual deployment!)
- Always in sync
- Easy rollback via `git revert`

## Scripts Overview

### rotate_logs_daily.sh
**Schedule:** Daily at 2am (crontab)

**Function:** Rotates current log files to dated versions

**Example:**
```
field_flow.jsonl → field_flow.20251207.jsonl
wrapper_requests.jsonl → wrapper_requests.20251207.jsonl
evolution.jsonl → evolution.20251207.jsonl
```

Creates new empty files for continued logging.

---

### archive_logs_monthly.sh
**Schedule:** 1st of month at 3am (crontab)

**Function:** Archives previous month's daily files

**Example:**
```
field_flow.202512*.jsonl → field_flow.202512.jsonl.gz
wrapper_requests.202512*.jsonl → wrapper_requests.202512.jsonl.gz
evolution.202512*.jsonl → evolution.202512.jsonl.gz
```

Compresses and removes daily files.

---

### cleanup_old_logs.sh
**Schedule:** Sundays at 4am (crontab)

**Function:** Removes daily files older than 7 days

**Retention:**
- Daily files: 7 days
- Monthly archives: Indefinite

## Crontab Configuration
```bash
# SYNTX Log Rotation
0 2 * * * /opt/syntx-config/scripts/rotate_logs_daily.sh >> /opt/syntx-config/logs/rotation.log 2>&1
0 3 1 * * /opt/syntx-config/scripts/archive_logs_monthly.sh >> /opt/syntx-config/logs/archive.log 2>&1
0 4 * * 0 /opt/syntx-config/scripts/cleanup_old_logs.sh >> /opt/syntx-config/logs/cleanup.log 2>&1
```

Crontabs use symlink path → always execute latest version from Git!

## Manual Execution
```bash
# Test daily rotation
/opt/syntx-config/scripts/rotate_logs_daily.sh

# Force monthly archive (for testing)
/opt/syntx-config/scripts/archive_logs_monthly.sh

# Cleanup old files
/opt/syntx-config/scripts/cleanup_old_logs.sh
```

## Log Files

Rotation logs stored in:
```
/opt/syntx-config/logs/rotation.log
/opt/syntx-config/logs/archive.log
/opt/syntx-config/logs/cleanup.log
```

## Architecture Benefits

**Symlink Approach:**
- ✅ Single source of truth (Git)
- ✅ Instant updates (`git pull`)
- ✅ Version controlled
- ✅ Easy rollback
- ✅ Infrastructure as Code
- ✅ No deployment step needed

**vs Traditional Copy:**
- ❌ Two copies to maintain
- ❌ Manual deployment required
- ❌ Can get out of sync
- ❌ Unclear which is source

## Updating Scripts
```bash
# 1. Edit script in repo
vim scripts/rotate_logs_daily.sh

# 2. Test
/opt/syntx-config/scripts/rotate_logs_daily.sh

# 3. Commit
git add scripts/rotate_logs_daily.sh
git commit -m "Update rotation script"
git push

# Done! Changes are immediately live via symlink
```

## New Server Setup
```bash
# 1. Clone repo
git clone <repo> /opt/syntx-workflow-api-get-prompts

# 2. Create symlink
ln -s /opt/syntx-workflow-api-get-prompts/scripts /opt/syntx-config/scripts

# 3. Install crontabs
crontab -e
# (add rotation entries)

# Done! Scripts operational
```
