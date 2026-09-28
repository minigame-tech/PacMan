# Security Policy

## Supported Versions

The following table lists the versions of PacMan currently receiving security updates:

| Version        | Supported          |
|----------------|--------------------|
| `main` (latest) | ✅ Yes             |
| Older releases  | ❌ No              |

> We recommend always using the latest version from the `main` branch.

## Reporting a Vulnerability

We take security seriously — even in a game project. If you discover a security vulnerability,
please report it **responsibly** so we can address it before it becomes public.

### How to Report

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please send a detailed report via email to:

📧 **[minigametech@proton.me](mailto:minigametech@proton.me)**

### What to Include

To help us understand and resolve the issue quickly, please provide:

- **Description**: A clear explanation of the vulnerability.
- **Reproduction steps**: Detailed steps to reproduce the issue.
- **Impact assessment**: What an attacker could potentially achieve.
- **Affected components**: Which files or modules are involved.
- **Suggested fix** (optional): If you have a proposed solution, we'd love to hear it.

### What to Expect

| Step                        | Timeframe         |
|-----------------------------|--------------------|
| Acknowledgment of report    | Within **48 hours** |
| Initial assessment          | Within **7 days**   |
| Fix or mitigation deployed  | Within **30 days**  |
| Public disclosure (if applicable) | After fix is released |

We will keep you informed about the progress of the fix and may ask for additional information
or guidance.

## Scope

The following areas are considered **in scope** for security reports:

- Arbitrary code execution through crafted game assets or save files
- Path traversal or file system access outside the intended project directory
- Dependency vulnerabilities in bundled libraries (`g2d.py`, Pygame)
- Vulnerabilities in the PyInstaller build pipeline or generated executables

The following are **out of scope**:

- Gameplay exploits or cheating (e.g., modifying score, clipping through walls)
- Denial of service through excessive resource usage on a local machine
- Issues requiring physical access to the machine running the game
- Vulnerabilities in upstream dependencies already reported to their maintainers

## Security Best Practices for Contributors

When contributing code, please keep these security practices in mind:

- **Never hardcode secrets** (API keys, credentials, tokens) in the source code.
- **Validate file paths** — use `resource_path()` and avoid constructing paths from user input.
- **Avoid `eval()` and `exec()`** — never execute dynamically constructed code.
- **Pin dependencies** — when adding dependencies, specify exact or minimum versions.
- **Review third-party assets** — ensure any added images, audio, or fonts are free of embedded payloads.

## Acknowledgments

We appreciate the security research community and will gladly credit reporters (with their
permission) in the project's release notes when a vulnerability is confirmed and fixed.

---

Thank you for helping keep PacMan and its users safe! 🔒
