# BLKSHP OS Scripts

## Available Scripts

### test.sh

Automated testing and setup script.

**Usage:**
```bash
./scripts/test.sh [site-name]
```

**What it does:**
1. Checks if the app is installed on the site
2. Runs migrations (loads fixtures automatically)
3. Clears cache
4. Builds assets
5. Optionally creates test data
6. Optionally runs unit tests

**Prerequisites:**
- The app must be installed first: `bench --site [site] install-app blkshp_os`

**Example:**
```bash
cd /Users/Eric/Development/BLKSHP/BLKSHP-DEV/apps/blkshp_os
./scripts/test.sh site1.local
```

---

### setup_test_data.py

Python script to create test data for the Departments and Permissions domains.

**Usage:**
```bash
bench --site [site-name] execute blkshp_os.scripts.setup_test_data.setup_all
```

**What it creates:**
- Test Restaurant company
- 5 departments (Kitchen, Bar, Catering, Office, Prep Kitchen)
- 3 test users (buyer@test.com, inventory@test.com, manager@test.com)
- Verifies standard roles are loaded

**Prerequisites:**
- The app must be installed first
- Run migrations before executing this script

**Example:**
```bash
bench --site site1.local execute blkshp_os.scripts.setup_test_data.setup_all
```

---

### sync_doctypes.py

Manual helper to re-import the BLKSHP OS DocTypes when working with fresh or reset sites.

**Location:** `blkshp_os/blkshp_os/scripts/sync_doctypes.py`

**Usage:**
```bash
bench --site [site-name] execute blkshp_os.scripts.sync_doctypes.sync_all
```

**What it does:**
- Imports the Department, Department Permission, Product Department, and Role Permission DocTypes from their JSON definitions
- Commits the transaction
- Verifies each DocType exists

**When to use:**
- After resetting or reinstalling a site
- When DocTypes were added to the app after the initial install

**Example:**
```bash
bench --site blkshp.local execute blkshp_os.scripts.sync_doctypes.sync_all
```

---

### dev_server.sh

Helper for starting, stopping, and monitoring the BLKSHP development stack (web, Socket.IO, workers, scheduler, Redis, asset watcher) in the background using `honcho`.

**Location:** `scripts/dev_server.sh`

**Usage:**
```bash
./scripts/dev_server.sh start    # launch bench start under honcho (nohup)
./scripts/dev_server.sh stop     # terminate bench + helpers and clean up pid file
./scripts/dev_server.sh restart  # convenience wrapper around stop + start
./scripts/dev_server.sh status   # show currently running bench helper processes
./scripts/dev_server.sh logs     # tail the aggregated background log output
```

**Notes:**
- Ensures the bench env bin directory is first on PATH so `honcho` is selected instead of Ruby `foreman`.
- Persists a pid file at `config/dev_server.pid` and writes combined output to `logs/dev-server.log`.
- `stop` also clears orphaned `frappe.utils.bench_helper` processes and the esbuild watcher to avoid stale schedulers.

**Add handy aliases** (append to `~/.zshrc` or run manually):
```bash
alias blkbench='cd /Users/Eric/Development/BLKSHP/BLKSHP-DEV && ./apps/blkshp_os/scripts/dev_server.sh'
alias blkstart='blkbench start'
alias blkstop='blkbench stop'
alias blkstatus='blkbench status'
alias blklogs='blkbench logs'
```

---

## First-Time Setup

If you're setting up BLKSHP OS for the first time, follow these steps:

```bash
# 1. Navigate to bench directory
cd /Users/Eric/Development/BLKSHP/BLKSHP-DEV

# 2. Install the app (REQUIRED FIRST STEP)
bench --site [your-site] install-app blkshp_os

# 3. Run the automated test script
cd apps/blkshp_os
./scripts/test.sh [your-site]
```

See `docs/FIRST-TIME-SETUP.md` for detailed instructions.

---

## Troubleshooting

### Error: "App blkshp_os is not installed"

**Solution:**
```bash
bench --site [your-site] install-app blkshp_os
```

### Error: "Permission denied" when running test.sh

**Solution:**
```bash
chmod +x scripts/test.sh
```

### Error: "Site [your-site] does not exist"

**Solution:**
```bash
# List all sites
ls sites/

# Use the correct site name
./scripts/test.sh [correct-site-name]
```

---

## Documentation

- **First-Time Setup**: `docs/FIRST-TIME-SETUP.md`
- **Quick Start**: `docs/QUICK-START.md`
- **Testing Guide**: `docs/TESTING-GUIDE.md`
- **Fixtures Info**: `docs/FIXTURES-INFO.md`

