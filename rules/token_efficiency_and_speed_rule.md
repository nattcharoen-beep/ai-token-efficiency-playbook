---
name: token-efficiency-and-speed
description: "Universal 5-Lever Token Efficiency, Speed Optimization, and Context Window Management Rule"
trigger: always_on
---

# ⚡ Universal Rule: 5-Lever Token Efficiency, Speed Optimization, and Context Window Management

## 📌 Core Philosophy & Objective
The LLM context window is a finite, high-cost working memory with strict latency and attention boundaries. Unchecked context growth triggers the **Quadratic Context Accumulation Law** ($O(N^2)$ token re-reading), leading to exponential latency, inflated token consumption, and catastrophic attention drift (needle-in-a-haystack degradation).

To maximize execution velocity, maintain pinpoint agent accuracy, and minimize token overhead across all engineering workflows, every AI agent (Lead Orchestrators, Subagents, Reviewers) must strictly execute the **5-Lever Optimization Protocol**.

---

### 1. 🎯 Lever 1: Strict Targeted File Slicing (Surgical Inspection)
- **Maximum Reading Window:** Never inspect more than **150–200 lines per read command** (`StartLine` to `EndLine`).
- **Search-Before-Read Pattern:** Always utilize grep, symbol discovery, or targeted search tools to pinpoint target line numbers before opening a file.
- **🚫 Prohibited Actions:**
  - Never dump monolithic files (1,000+ lines) into the context window without slice parameters.
  - Never load unreferenced dependencies, massive bundle outputs, or binary minified files into context.
- **✅ Mandatory Pattern:**
  - Pinpoint target function or class definition.
  - Read only the target range with 10–20 lines of context padding.
  - Edit or analyze surgically based on precise offsets.

---

### 2. ⏱️ Lever 2: Milestone Handoff & Compact Cadence
- **Compaction Threshold:** Proactively trigger context compaction or session handoff every **20–25 interaction turns** or when context reaches **70,000–80,000 tokens**.
- **State Externalization via Artifacts:**
  - Persist active runtime state, completed milestones, pending backlog items, and architectural decisions into dedicated Markdown artifacts or session state files.
  - Clear transient logs, intermediate exploratory steps, and dead hypotheses before handing off.
- **Resumption Readiness:**
  - When starting a resumed session or issuing `/compact`, load only the persistent state artifact. Do not re-ingest entire conversational histories.

---

### 3. 🧠 Lever 3: 3-Tier Cognitive Model Routing
Match cognitive horsepower to task complexity to optimize speed, accuracy, and token economics:
- **⚡ Tier 1: High-Speed Scouts (`flash` / `flash-lite`)**
  - **Workloads:** File discovery, glob scanning, regex searching, raw data extraction, scraping, large log file grepping.
  - **Objective:** Maximum throughput, sub-second latency, near-zero cost.
- **🛠️ Tier 2: General Workhorses (`pro`)**
  - **Workloads:** Core feature development, REST API design, UI component authoring, unit test implementation, standard bug fixes.
  - **Objective:** High-precision engineering with balanced token expenditure.
- **👑 Tier 3: Frontier Architects (`frontier` / `opus` / `inherit`)**
  - **Workloads:** Multi-service system architecture, mission-critical financial/cryptographic algorithms, zero-defect concurrency engines.
  - **Objective:** Maximum reasoning depth and verification rigor.

---

### 4. 📝 Lever 4: Scratchpad Output Redirection
- **High-Volume Command Handling:**
  - Any terminal command, build tool, test suite, or migration script generating **>50 lines of output** MUST be redirected to an external scratchpad file (e.g. `scratch/build.log` or temporary run artifacts).
- **Context Summarization:**
  - Never allow raw build dumps or multi-thousand line stack traces into the conversational context.
  - In context, inspect only the exit code, high-level summary (e.g. `Tests: 48 passed, 0 failed`), and isolated failure traces (last 10–20 lines of error).

---

### 5. 🐝 Lever 5: Ephemeral Swarm Execution & Concise Return Contracts
- **Scoped Micro-Prompts:**
  - Subagents must be invoked with isolated, single-responsibility prompts defining strict inputs, outputs, and constraints.
- **Concise Return Contracts:**
  - Subagents must communicate back using standardized, low-footprint payload summaries:
    1. **Summary of Action:** Concise bullet points of what was executed.
    2. **Modified Files:** Exact relative paths of touched files.
    3. **Verification Evidence:** Deterministic test pass status and exit codes.
    4. **Attention Flags:** Critical warnings or `Clean (100%)`.
  - **Strictly Prohibited:** Returning full execution traces, raw file copies, or chat logs back to the parent orchestrator.
- **Context Isolation:**
  - Parent orchestrator context remains pristine, fast, and responsive for high-level decision making.

---

## 🔒 Enforcement & Verification
Every autonomous agent workflow must maintain compliance with these 5 levers. Workflows violating Lever 1 (unbounded reads) or Lever 4 (unbounded command dumps) must be immediately halted and refactored into surgical operations.
