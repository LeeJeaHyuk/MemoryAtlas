# Runs (RUN)
    
    Runs are **Execution Plans**. They track the "work" done to implement a Requirement.
    
    ## Naming Convention
    - **File**: `RUN-{Target_ID}-step-{NN}.md` (e.g. `RUN-REQ-CORE-001-step-01.md`)
    - **ID Pattern**: `^RUN-(BRIEF|REQ)-([A-Z]+)-(\d{3})-step-(\d{2})$`
    
    ## Workflow
    1. **Plan**: `atlas run REQ-XXX-001` (Creates RUN doc).
    2. **Execute**: Write code, run tests. Check off items in `## Plan` and `## Verification`.
    3. **Finish**: `atlas finish RUN-... --success true` (Updates REQ status & logs Git hash).
    
    ## Rules
    - Never implement a REQ without a RUN.
    - Verification steps are mandatory.
    