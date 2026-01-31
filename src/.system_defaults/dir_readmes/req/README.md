# Requirements (REQ)
    
    Requirements define **what** the system must do. They are the authoritative Source of Truth (SSOT).
    
    ## Naming Convention
    - **File**: `REQ-{Domain}-{Number}.md` (e.g., `REQ-CORE-001.md`)
    - **ID Pattern**: `^REQ-([A-Z]+)-(\d{3})$`
    
    ## Required Metadata
    - `ID`: Must match filename.
    - `Domain`: Project domain (e.g., `CORE`, `API`, `UI`).
    - `Status`: `Draft` | `Active` | `Implemented` | `Rejected`.
    - `Must-Read`: Comma-separated list of dependent `RULE` IDs (or `None`).
    - `Implemented-Git`: Git commit hash (Required if Status is Implemented).
    - `Linked-RUN`: executing RUN ID (Required if Status is Implemented).
    
    ## Rules
    1. **Atomic**: Each REQ should be small enough to be implemented and verified in one go.
    2. **Testable**: Must have clear Acceptance Criteria.
    3. **Immutable**: Once Implemented, do not change without a new RUN.
    