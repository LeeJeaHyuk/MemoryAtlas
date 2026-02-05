# MemoryAtlas

> Document-Driven Development with Atlas CLI

Quick flow (Capture -> Run -> Finish):
1) `python atlas.py init` (first time)
2) `python atlas.py capture "..." --domain GEN`
3) `python atlas.py run REQ-GEN-001`
4) `python atlas.py finish RUN-REQ-GEN-001-step-01 --git <hash|no-commit> --success true`
5) `python atlas.py doctor`

Top docs: FRONT.md, BOARD.md, CONVENTIONS.md, GOALS.md  
Reference: README.md
