# Views (VIEW)
    
    Views provide High-Level context, summaries, or specific angles on Requirements. They are **not** SSOT, but point to SSOT.
    
    ## Naming Convention
    - **File**: `VIEW-{Referenced_ID}.md` (e.g., `VIEW-REQ-CORE-001.md`)
    - **ID Pattern**: `^VIEW-(.*)$`
    
    ## Required Metadata
    - `Refs`: The primary ID this view discusses.
    
    ## Structure Rules
    - **References (SSOT index)**: Must list ALL `REQ` or `RULE` IDs mentioned in the text.
    - **Normative Keywords**: If you use "MUST", "SHOULD", etc., you must cite a specific ID (e.g. `... must be fast (@REQ-PERF-001)`).
    
    ## Usage
    Use Views to write human-readable design docs, usage guides, or technical specs that aggregate multiple Requirements.
    