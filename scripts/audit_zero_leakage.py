#!/usr/bin/env python3
"""
Zero-Leakage Security Verification Audit
Scans all repository files to guarantee zero occurrences of private tokens or credentials.
All check signatures are base64-encoded to prevent false-positives in source code.
"""

import sys
import base64
import re
from pathlib import Path

# Configure stdout for UTF-8 regardless of platform default
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Base64-encoded forbidden signatures
ENCODED_SIGNATURES = [
    "bmF0dA==",                         # token 1
    "4Lie4Li14LmI4LiZ4Lix4LiX",         # token 2
    "4LiE4Li44LiT4LiZ4Lix4LiX",         # token 3
    "Ymx1Y2hlcg==",                     # token 4
    "4Lia4Lil4Li54LmA4LiE4Lit4Lij4LmM", # token 5
    "ZnRl",                             # token 6
    "YXF1YXNoaWVsZA==",                 # token 7
    "b21lbg==",                         # token 8
    "eGlhb21p",                         # token 9
    "dWx0aW1lYQ==",                     # token 10
    "c2VubmhlaXNlcg==",                 # token 11
    "4KSF4KSs4KWN4KSm4KWB4KSy",         # token 12
    "4Lit4Lix4Lia4LiU4Li44Lil",         # token 13
    "VXNlcnNcbmF0dGM=",                 # token 14
    "VXNlcnMvbmF0dGM=",                 # token 15
]

def load_signatures():
    return [base64.b64decode(sig).decode("utf-8") for sig in ENCODED_SIGNATURES]

def audit_repository(root_dir: Path):
    raw_signatures = load_signatures()
    this_script = Path(__file__).resolve()
    violations = []
    inspected_files = 0

    print(f"Scanning repository for private data leakage: {root_dir}")

    for file_path in root_dir.rglob("*"):
        if not file_path.is_file():
            continue

        resolved = file_path.resolve()
        # Skip this audit script itself and git internal files
        if resolved == this_script:
            continue
        if ".git" in file_path.parts:
            continue

        inspected_files += 1
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"Warning: could not read {file_path}: {e}")
            continue

        for sig in raw_signatures:
            # If token is purely ASCII alphanumeric, use word boundary check to avoid substring false positives (e.g. 'fte' inside 'after')
            if sig.isalnum() and sig.isascii():
                pattern = rf"\b{re.escape(sig)}\b"
                match = re.search(pattern, content, re.IGNORECASE)
            else:
                pattern = re.escape(sig)
                match = re.search(pattern, content, re.IGNORECASE)

            if match:
                token_hash = base64.b64encode(sig.encode("utf-8")).decode("utf-8")
                violations.append((file_path, token_hash))

    print(f"Total files audited: {inspected_files}")

    if violations:
        print("\n[!] SECURITY AUDIT FAILED! Prohibited tokens detected:")
        for path, token_hash in violations:
            print(f"  - File: {path.relative_to(root_dir)} (Signature Ref: {token_hash})")
        return False
    else:
        print("\n[+] ZERO-LEAKAGE AUDIT PASSED: 100% clean across all repository files.")
        return True

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    success = audit_repository(repo_root)
    sys.exit(0 if success else 1)
