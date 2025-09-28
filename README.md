# GitAct: GitHub Activity Feed

## Overview
GitAct is a lightweight CLI tool that highlights the latest public GitHub events for any user, wrapping each entry in a colorful, easy-to-scan layout.

## Quick Start
1. **Create/activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install requests
   ```
3. **Run the feed for any GitHub username:**
   ```bash
   python gitactiv.py <github-username>
   ```

## Example
```
┌───────────────────┐
│ GitAct • @octocat │
└───────────────────┘
⬆ Pushed 3 commits
   octocat/Hello-World • Sep 28, 2024 14:03 UTC
```

## Notes
- GitHub’s unauthenticated API allows ~60 requests per hour per IP; add authentication if you need higher limits.
- Empty histories simply report “No recent activity,” so the tool is safe to run against inactive accounts.
