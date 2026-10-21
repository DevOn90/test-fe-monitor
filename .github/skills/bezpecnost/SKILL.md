---
name: bezpecnost
description: "Analyze the security of a piece of code and provide recommendations for improvement."
argument-hint: Select a piece of code to analyze for security issues.
disable-model-invocation: true
---

Analyze the selected code for security issues including:

- XSS
- SQL Injection
- NoSQL Injection
- Command Injection
- SSRF
- CSRF
- Path Traversal
- Authentication
- Authorization
- Sensitive data exposure
- Secrets
- Unsafe deserialization
- Input validation

For every finding include:

- severity
- explanation
- recommendation
