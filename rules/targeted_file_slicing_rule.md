---
name: targeted-file-slicing
description: "Enforce Surgical File Reading & Window Slicing to Prevent Context Bloat"
trigger: always_on
---

# 🎯 Rule: Targeted File Slicing & Surgical Code Inspection

## 📌 Context Window Protection Directive
Large codebases quickly overwhelm LLM working memory when files are ingested whole. Dumping thousands of lines into the context window causes:
1. **Severe Attention Degradation:** Key instructions and subtle types get lost in massive irrelevant code blocks.
2. **Quadratic Token Overhead:** Every subsequent turn re-processes all previous file dumps at increasing latency and cost.
3. **Slow Turnaround Times:** Large payloads saturate API bandwidth and model prefill computation.

---

## 📐 The Surgical Inspection Standard

### 1. Window Slicing Limit: 150–200 Lines
- When calling file inspection tools (e.g. `view_file`), always supply `StartLine` and `EndLine` parameters.
- Limit each read window to **150–200 lines maximum**.
- If a target module exceeds 200 lines, isolate the specific function, class, or method required for the task.

### 2. Search-Before-Read Workflow
Always follow the two-step reconnaissance pattern:
```
[Step 1: Reconnaissance]
Use grep, symbol search, or file structure outline to locate target line numbers.
        ⬇
[Step 2: Targeted Read]
Invoke view_file(StartLine = N - 15, EndLine = N + 150).
```

### 3. Prohibited Anti-Patterns
- ❌ **The Monolithic Ingestion:** Invoking file readers on an entire file of 1,000+ lines without line boundaries.
- ❌ **Sequential File Scanning:** Reading a file from line 1 to line 2,000 in 10 consecutive chunks just to find a string. (Use grep/search tools instead).
- ❌ **Dependency Ingestion:** Loading external vendor libraries (`node_modules`, minified bundles, compiled binaries) into prompt context.

### 4. Code Modification Guardrails
- Make contiguous, localized edits using exact search-and-replace blocks.
- Never output the entire file content just to change 3 lines of code.

---

## 💡 Practical Examples

### ❌ Bad (Monolithic Dump):
```json
// Antigravity / Agent Tool Call
{
  "tool": "view_file",
  "args": {
    "AbsolutePath": "/repo/src/core/payment_engine.ts"
    // No StartLine / EndLine specified -> 3,400 lines injected into prompt!
  }
}
```

### ✅ Good (Targeted Slice):
```json
// Step 1: Grep find
// Output: Line 412: export class InvoiceReconciler {

// Step 2: Surgical slice
{
  "tool": "view_file",
  "args": {
    "AbsolutePath": "/repo/src/core/payment_engine.ts",
    "StartLine": 405,
    "EndLine": 520
  }
}
```
