---
name: testuj-e2e
description: "Generates end-to-end tests for the selected code"
argument-hint: Select a piece of code to generate end-to-end tests for.
disable-model-invocation: true
---

Generate end-to-end tests using the project's existing E2E framework.

If none is apparent, use Cypress.

Cover:

- happy path
- user validation
- error scenarios
- boundary conditions
