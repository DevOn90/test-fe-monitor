## Metadata

- **Project**: <name-of-project>
- **Status**: <Draft-In-Progress-Completed-Superseded>
- **Stage**: <discovery-delivery>
- **Owner**: <name-of-owner>
- **Last Updated**: <YYYY-MM-DD>

---

## Related Documents

- Business Problem
- Problem Discovery
- Problem Statement
- Solution Space Exploration
- Solution Concept Selection
- Assumptions List
- Assumptions Backlog

---

# Product Requirements Document (PRD)

## Purpose

<!--
Define the purpose of this PRD.

This document describes:
- What product will be built
- Why it will be built
- What requirements it must satisfy

It is the single source of truth for product scope and requirements.
-->

---

# Product Baseline

## Product Goal

<!-- What problem does this product solve and what outcome should it achieve? -->

---

## Target Users

<!-- Who will use this product? -->

- User segment 1: <!-- E.g.: "Small business owners who want to manage their finances more effectively" -->
- User segment 2: <!-- E.g.: "Freelancers who need to track their time and expenses" -->

---

## Desired User Outcome

<!-- What should users be able to achieve after using the product? -->
<!-- E.g.: "Users should be able to easily track their expenses and generate reports to manage their finances more effectively" -->

---

## MVP / Release Scope
<!-- What is the minimum set of features that must be delivered to achieve the product goal? -->

**Rule for MVP:**<br>
- Start from outcomes, not feature ideas.
- List only capabilities required to hit Success Criteria.
- Mark `Must` only if removing it would make goal failure likely.

***Priority:** Must / Should / Could<br>
***Release Decision:** Included / Excluded

| ID | Feature | User Outcome Supported | *Priority | *Release Decision | Reason | Validation Metric |
|----|---------|-----------------------|----------|-----------------|--------|------------------| 
| MVP-XXX | <Basic Onboarding Flow> | <First-time user can start without help> | Must | Included | <Removes first-use friction> | <activation rate> |

---

## Success Criteria
<!-- How will we know the product/release is successful? -->

| Metric | Current Baseline | Target |
|---|---|---|
| <!-- SC-XXX --> | <!-- Activation rate: 32% --> | <!-- Activation rate: 32% to 50% --> |
| <!--SC-XXX--> | <!-- Task completion: 58% --> | <!-- Task completion: 58% to 80% --> |

---

# Product Features

<!--
High-level capabilities/features.
Detailed requirements belong below.
-->

## Epics:

### Epic [ID]: [Name]

#### Purpose
<!-- Why does this epic exist? -->

#### User Value
<!-- What user problem does this epic solve? -->

#### Requirements
<!-- List of requirements that belong to this epic -->
- 

#### Acceptance Criteria
<!-- How will we know this epic is complete? -->
- 

#### Dependencies
<!-- What other epics, features, or systems does this epic depend on? -->

#### Risks
<!-- What are the risks associated with this epic? -->  

#### Github Milestones
- <!-- [MILESTONE-NAME-XXX](https://github.com/repo-owner/repo-name/milestone/#number) -->

---

## Features

### Feature [ID]: [Name]

#### Purpose
<!-- Why does this feature exist? -->

#### User Value
<!-- What user problem does this feature solve? -->

#### Requirements

| ID | Requirement | Priority |
|---|---|---|
| REQ-XXX | | Must / Should / Could |


#### Acceptance Criteria
<!-- How will we know this feature is complete? -->
- 

#### Dependencies
<!-- What other features, epics, User stories, or systems does this feature depend on? -->

#### Risks
<!-- What are the risks associated with this feature? -->  

#### Github Issue
- <!-- [ISSUE-NAME-XXX](https://github.com/repo-owner/repo-name/issues/#number) -->

---

# User Stories
<!-- Convert requirements into user-focused scenarios -->
<!--Process:
1. Copy `BL-product-backlog-[template]_v0.0.0.ods` to `docs/product/discovery/requirements/` and rename it appropriately.
2. Copy `BL-product-backlog-log-[template].md` to `docs/product/discovery/requirements/` and rename it appropriately.
3. Revision control described in the log file.
-->

- Reference: [BL-product-backlog_v0.0.0.ods](<link-to-product-backlog>)<br>
- Reference: [BL-product-backlog-log.md](<link-to-product-backlog-log>)


---

# User Experience

## User Flows
<!-- 
1. Describe only the main/core user flows:
- Onboarding
- Purchase
- Settings
- Account Management 
  
2. Use the User flow diagram template `docs/product/architecture/templates/ui/FL-XXX-<name-flow>-[template].md` to create a flow diagram and store it in the dedicated folder `docs/product/architecture/ui/ui-flows/`.

3. Update the flow diagram links in the `BL-product-backlog_v0.0.0.ods` file.
  -->

### Core User Flows:
1. FL-XXX: [Name of Flow]
   - Description: 
   - Steps:
     1. Step 1
     2. Step 2
     3. Step 3
   - References:
     - [FL-XXX-<name-of-flow>.md](<link-to-flow-diagram>)

---

**Flow Types:**
- **Core**: Main user flows that are essential to the product
- **Variant**: Alternative flows based on different conditions
- **Exception**: Flows that handle errors or exceptional cases

### Flows Lists:
| ID | Flow Name | Description | Type| Reference |
|----|-----------|-------------|-----------|-----|
| FL-XXX | Flow Name XYZ | Description of the flow | <Core-Variant-Exception> | [FL-XXX-<name-of-flow>.md](<link-to-flow-diagram>) |

---

## Wireframes / Mockups
<!-- Add links or references -->

### Wireframes
<!--Process for adding wireframes:
1. Open Figma and load the wireframe file template.
2. Update name and version in Figma.
3. Create or update content in the wireframe.
4. Export the wireframe as a .fig file and upload it to the appropriate location in the repository.
5. Update the reference link in this PRD to point to the wireframe file 
6. Update wireframe log with the new version and changes.
-->

#### Lo-fi Wireframe (status: Active | Inactive)
Reference: [lo-fi-wireframe-<name-of-wireframe>.fig](<link-to-wireframe>)

#### Hi-fi Wireframe (status: Active | Inactive)
Reference: [hi-fi-wireframe-<name-of-wireframe>.fig](<link-to-wireframe>)

---

# Requirements
<!--Process steps for adding requirements:
1. Copy `RR-requirements-register-[template]_v0.0.0.ods` to `docs/product/discovery/requirements/` and rename it appropriately.
2. Copy `RR-requirements-register-log-[template].md` to `docs/product/discovery/requirements/` and rename it appropriately.
3. Revision control described in the log file.  
-->

## Functional Requirements
<!-- System behaviour requirements -->
<!-- In PRD keep only stable, product-defining requirements. Keep evolving requirements in the requirements register. -->

Reference: [RR-requirements-register.ods](<link-to-requirements-register>)<br>
Reference: [RR-requirements-register-log.md](<link-to-requirements-register-log>)

***Priority:** Must / Should / Could

| ID     | Requirement | *Priority              |
| ------ | ----------- | --------------------- |
| FR-XXX | Example requirement | Must |

---

## Non-Functional Requirements
<!-- Quality attributes -->
<!-- In PRD keep only stable, product-defining requirements. Keep evolving requirements in the requirements register. -->

Reference: [RR-requirements-register.ods](<link-to-requirements-register>)<br>
Reference: [RR-requirements-register-log.md](<link-to-requirements-register-log>)

***Priority:** Must / Should / Could<br>
***Type:** Performance / Security / Reliability / Scalability / Other

| ID     | Requirement | *Type | *Priority              |
| ------ | ----------- | ----- | --------------------- |  
| NFR-XXX | Example requirement | Performance | Must |

---

## Technical Requirements
<!-- Technical constraints or implementation requirements or platform requirements -->
<!-- In PRD keep only stable, product-defining requirements. Keep evolving requirements in the requirements register. -->

Reference: [RR-requirements-register.ods](<link-to-requirements-register>)<br>
Reference: [RR-requirements-register-log.md](<link-to-requirements-register-log>)

***Priority:** Must / Should / Could<br>

| ID     | Requirement | *Priority              |
| ------ | ----------- | --------------------- |
| TR-XXX | Example requirement | Must |

---

# Assumptions
<!--Assumptions backlog lives in `docs/product/discovery/assumptions/ART-XXX-assumptions-backlog.md`-->

Reference: [ART-XXX-assumptions-backlog.md](<link-to-assumptions-list>)

---

# Decisions
<!-- Product decisions records lives in `docs/product/discovery/decisions/PDR-XXX-product-decision-record.md` -->

Reference: [PDR-XXX-product-decision-record.md](<link-to-decision-record>)

---

# Open Questions
<!-- Dedicated for decision-blocking unknowns that affect scope, release, implementation, architecture or user behavior -->
<!--Limit to 3-7 questions, don't include trivial or non-blocking questions-->

***Impact:** High / Medium / Low<br>
***Status:** Open / Answered / Closed<br>
**Note:** Remove completed questions from this section and move them to the decision record.

| ID | Question | *Impact | *Status |
|----|----------|--------|--------|
| Q-XXX | Example question | High | Open |

---

# Dependencies and Risks

## Dependencies
<!-- What other products, teams, or systems does this product depend on? -->

***Type:** Product / Team / System<br>
***Status:** Open / In Progress / Completed / Blocked

| ID | Dependency | *Type | Owner | Why it matters | *Status |
|----|------------|------|-------|----------------|--------|
| Dep-XXX | Example dependency | Product / Team / System | <name-of-owner> | <why-it-matters> | Open |  

---

## Risks and Mitigations
<!--Process for risks management:
1. Copy `RSK-XXX-risk-register-[template]_v0.0.0.ods` to `docs/risk/` and rename it appropriately.
2. Copy `RSK-XXX-risk-register-log-[template].md` to `docs/risk/` and rename it appropriately.
3. Revision control described in the log file.
-->

Reference: [RSK-XXX-risk-register.ods](<link-to-risk-register>)<br>
Reference: [RSK-XXX-risk-register-log.md](<link-to-risk-register-log>)

---

# Release Plan
<!-- How will this product be released to users? -->
<!--Process:
1. Define the release plan and rollback values
2. Monitor after release
3. If success, close PRD else rollback -->

## Release Version
- <!-- E.g. v1.1.0 -->

## Release Goal
<!-- What is the goal of this release? -->
- <!--E.g.: Deploy core onboarding flow to reduce user drop-off from 45% to 30% -->

## Validation After Release
<!-- How will we measure learning after users start using it? -->

1. <!--E.g.: Service uptime above 99% over 7 days-->
2. <!--E.g.: Error rate below 1% over 7 days-->
3. <!-- Onboarding completion increases by at least 10 percentage points within 14 days -->

## Rollback Criteria
<!-- Define exact conditions that trigger rollback -->

1. <!-- Crash loop persists over 10 minutes -->
2. <!-- Error rate above 5% for more than 30 minutes -->
3. <!-- Critical user path unavailable for more than 15 minutes -->

---

# Release Runbook
<!--Execution, monitoring and recovery of the release-->
<!--Process:  
1. Create a dedicated release runbook file in `docs/product/delivery/releases/v<release-version>/` using the template `RRB-XXX-release-runbook-[template].md`.
2. Update the reference link in this PRD to point to the release runbook file. 
-->

Release runbook is a step-by-step guide for executing, monitoring, and recovering from the release.

Reference: [RRB-XXX-release-runbook.md](<link-to-release-runbook>)

---

## References
- Business Problem: <!-- Link to the business problem document -->
- Problem Statement: <!-- Link to the problem statement document -->
- Solution Discovery: <!-- Link to the solution discovery document -->
- Assumptions: <!-- Link to the assumptions document -->
- Experiments: <!-- Link to the experiments document -->
- Research: <!-- Link to the research document -->
- Issues: <!-- e.g. #123 -->
- PRs: <!-- e.g. #125 -->
