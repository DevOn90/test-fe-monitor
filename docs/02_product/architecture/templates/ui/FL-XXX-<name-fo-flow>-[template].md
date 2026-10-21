## Metadata

- **Project**: <name-of-project>
- **Status**: <Draft-In-Progress-Completed-Superseded>
- **Stage**: <discovery-delivery>
- **Owner**: <name-of-owner>
- **Last Updated**: <YYYY-MM-DD>

---

## Related Documents

- User Story: [US-XXX](<link-to-user-story>)

---

# User Flow [FL-XXX]: <Name of Flow>

## Purpose
<!-- One sentence why this flow exists. -->

## Trigger
<!-- What event or action initiates this flow? -->
<!-- Example: User clicks on "Sign Up" button. -->

## Steps Flow Diagram
<!-- Use the flow diagram template to create a flow diagram for this user flow. -->
**Complexity Guard:**<br>
If `Max-steps` > 8 or `Max-decision-points` > 3, split into second flow diagram and link to it in the references section.


```mermaid
flowchart TB
  %% ====== STYLE ======
  classDef step fill:#E8F1FF,stroke:#2F5FA8,stroke-width:1px,color:#0F2A4A;
  classDef decision fill:#FFF4D6,stroke:#B7791F,stroke-width:1px,color:#4A2D00;
  classDef variant fill:#E6FFFA,stroke:#0F766E,stroke-width:1px,color:#063B37;
  classDef exception fill:#FFE8E8,stroke:#B42318,stroke-width:1px,color:#5C1111;
  classDef terminal fill:#EAFBEA,stroke:#2E7D32,stroke-width:1px,color:#123015;
  classDef handoff fill:#F3E8FF,stroke:#6B21A8,stroke-width:1px,color:#2E1065;

  %% ====== MAIN FLOW ======
  START([Start]):::terminal --> S1[Step 1: USER_ACTION]:::step
  S1 --> S2[Step 2: SYSTEM_RESPONSE]:::step
  S2 --> D1{Decision 1: CONDITION?}:::decision

  %% Happy path
  D1 -->|Yes| S3[Step 3: CONTINUE]:::step
  S3 --> S4[Step 4: COMPLETE]:::step
  S4 --> STOP([Stop / Success]):::terminal

  %% Variant path
  D1 -->|Variant A| V1[Variant: ALTERNATE_STEP]:::variant
  V1 --> V2[Variant: RETURN_TO_MAIN]:::variant
  V2 --> S3

  %% Exception path
  D1 -->|No / Error| E1[Exception: SHOW_ERROR]:::exception
  E1 --> E2{Retry allowed?}:::decision
  E2 -->|Retry| S1
  E2 -->|Abort| STOP_ERR([Stop / Failed]):::terminal

  %% ====== SPLIT TO NEXT FLOW (if > 8 steps or > 3 decisions) ======
  S3 --> D_SPLIT{More steps needed?}:::decision
  D_SPLIT -->|No| S4
  D_SPLIT -->|Yes| H1[[Go to next flow: FL-002]]:::handoff
```

## Sequence Diagram (Optional)
<!--Use sequence diagram only for edge technical cases. -->

```mermaid
sequenceDiagram
  participant User
  participant System
  User->>System: Action 1
  System-->>User: Response 1
  User->>System: Action 2
  System-->>User: Response 2
```

## Success Criteria
<!-- Define 1-X measurable success criteria for this flow. -->
<!-- Example: 
1. User completes the flow in less than 3 minutes. 
2. User successfully completes the flow without errors. 
3. Exception case transfers the user to a support page with a contact form.
X. ...
-->

1. ...
2. ...
3. ...

## References
- Issue: <!--e.g. #123-->
- PR: <!--e.g. #456-->
- Wireframes: <!--e.g. [link-to-wireframes]-->
- Parrent Flow: <!--e.g. [FL-001](link-to-parent-flow)-->
- Child Flow: <!--e.g. [FL-002](link-to-child-flow)-->
