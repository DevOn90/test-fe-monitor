# Git Commit Convention

This repository follows Conventional Commits.

Format:

<type>: <description>

Allowed types:

- feat     new functionality
- fix      bug fix
- docs     documentation
- chore    maintenance
- refactor code restructuring
- test     tests
- ci       CI/CD changes
- build    build tooling

Examples:

feat: add dashboard component

fix: resolve authentication redirect

chore: update npm dependencies

## Enforce Commit Message Convention

- `.githooks/commit-msg` is a Git hook that enforces the commit message convention.
