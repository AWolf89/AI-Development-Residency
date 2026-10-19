#!/usr/bin/env python3
"""Print the next ADR number (4 digits) for a docs/adr folder.

Usage: python3 next_adr.py docs/adr
A missing folder is treated as empty (prints 0001).
Exit codes: 0 = success, 2 = bad input (path exists but is not a folder).
"""
import os
import re
import sys


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 2 else 2)
    path = sys.argv[1]
    if os.path.exists(path) and not os.path.isdir(path):
        print(f"ERROR: {path} is not a folder", file=sys.stderr)
        sys.exit(2)
    nums = []
    if os.path.isdir(path):
        for name in os.listdir(path):
            m = re.match(r"^(\d{4})-.+\.md$", name)
            if m:
                nums.append(int(m.group(1)))
    print(f"{max(nums, default=0) + 1:04d}")


if __name__ == "__main__":
    main()
