# Project guidance

- This is a small, public workshop demo of the OpenAI Decisions API. Keep examples synthetic.
- Use Python 3 standard library; avoid adding dependencies for routine changes.
- Preserve `.gitignore` coverage for `.env` files, credentials, and generated files. Never print or commit API keys.
- Run `python3 -m py_compile decisions_demo.py` and `python3 decisions_demo.py --sample --dry-run` after changing request construction.
- For API-facing changes, also verify one live synthetic request when a personal key and network access are available. Report separately when live verification is unavailable.
- Keep the three decision types (`predicate`, `choice`, `score`) visible in the example, and handle refusals or low-confidence results without treating them as an automatic action.
- Work in a branch and present reviewable changes before merging or publishing a new version.
