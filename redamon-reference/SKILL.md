---
name: redamon-reference
description: Pointer to the RedAmon Offensive Security framework for automated penetration testing and vulnerability scanning.
---

# RedAmon Reference

RedAmon is a massive AI-driven Offensive Security framework (vulnerability scanning, penetration testing, automated exploitation).
The user has securely installed it at the absolute path: `I:\2_Do not touch\redamon`.

## When to use this skill
When the user asks you (Antigravity) or Codex to run security scans, look for vulnerabilities, or explicitly mentions "RedAmon".

## Instructions for Agents
1. **Location**: The framework is located at `I:\2_Do not touch\redamon`.
2. **Execution**: Do NOT try to run RedAmon tools directly on the host. It is fully containerized. You must use its Docker-based management scripts or instruct the user to do so.
3. **Usage**: To start or manage RedAmon, navigate to that directory and use its management script (e.g., `./redamon.sh up` or `./redamon.sh status`).
4. **Documentation**: If you need to know how to interact with its API, configure it, or understand its architecture, read `I:\2_Do not touch\redamon\README.md`.
