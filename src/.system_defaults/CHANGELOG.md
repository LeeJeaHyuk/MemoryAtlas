# Changelog

All notable changes to Atlas are documented here.

## [Unreleased]

## [0.3.0] - 2026-01-28

### Added
- SSOT-first structure: `views/`, `adr/`, `drafts/`, `inbox/`, `archive/`
- New CLI command: `capture` (creates/updates REQ + View)
- New CLI command: `run` (creates RUN from REQ with step sequence)
- Templates: `VIEW.md`, `ADR.md`
- Doctor checks: view->REQ references and Implemented-Git presence

### Changed
- RUN IDs use `RUN-REQ-...-step-XX` (no date in ID)
- `finish` writes `Implemented-Git` and `Linked-RUN` to REQ
- `intake`/`plan` deprecated in favor of `capture`/`run`
- BRIEFs moved to `drafts/brief/`; ideas to `inbox/`
