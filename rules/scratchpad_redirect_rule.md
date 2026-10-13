---
name: scratchpad-output-redirect
description: "Mandatory Terminal and Build Output Redirection to Prevent Context Flooding"
trigger: always_on
---

# 📝 Rule: Scratchpad Output Redirection & Log Hygiene

## 📌 Context Window Protection Directive
Terminal execution outputs, compilation logs, package manager installs, and full test suites frequently emit hundreds or thousands of lines of output. Dumping these directly into the agent conversational context causes instant context bloat, degrades token efficiency, and slows down subsequent turns.

---

## 🛠️ The Redirection Standard

### 1. The 50-Line Threshold
- Any command expected or observed to generate **more than 50 lines of output** must redirect stdout and stderr to a scratchpad file.
- Recommended scratch directory: `scratch/` or `.temp/` located in workspace or agent scratch storage.

### 2. High-Volume Command List
Always redirect output for:
- Package managers: `npm install`, `pnpm install`, `cargo build`, `pip install`
- Test runners: `npm test`, `pytest`, `cargo test`, `vitest run`
- Compilers / Bundlers: `tsc`, `webpack`, `vite build`, `esbuild`, `make`
- Version control logs: `git log` (always limit with `-n 10` or redirect)
- Container / infrastructure tools: `docker build`, `terraform apply`

### 3. Context Log Hygiene (Summary-Only in Context)
- Do not read back the full log into context.
- Instead:
  1. Check the command **Exit Code**.
  2. Extract the high-level summary line (e.g. `Tests: 34 passed, 34 total`).
  3. If failure occurs, extract only the specific stack trace or failing assertion (last 10–25 lines).

---

## 💡 Practical Examples

### ❌ Bad (Context Flooding):
```bash
# Running test suite directly into terminal buffer
pytest tests/ -v
# Result: 850 lines of passed test names flooded directly into context window!
```

### ✅ Good (Redirect & Surgical Inspection):
```bash
# Step 1: Redirect to scratchpad
pytest tests/ -v > scratch/pytest_results.log 2>&1

# Step 2: Inspect summary only
tail -n 15 scratch/pytest_results.log
# Result: "====== 42 passed in 2.14s ======" (Clean 1-line verification in context)
```

### PowerShell Example:
```powershell
# Redirect long command
npm test *> scratch/test_output.log; Get-Content scratch/test_output.log -Tail 15
```
