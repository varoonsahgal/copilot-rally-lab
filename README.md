# Rally Lab: Microsoft 365 Copilot Level 2 (baseball-themed labs)

Hands-on labs for **Enhancing Productivity with Microsoft 365 Copilot, Level 2: Investigate, Innovate, and Make Smarter Decisions**.

Participants join the fictional **Riverfront Rally Weekend Task Force** and work through two sessions:

| Section | Innings | Tools |
|---|---|---|
| **Game 1: The Investigation** (`session-1/`) | 5 labs | Copilot Chat, Outlook, Teams, Researcher, Analyst, Excel |
| **Game 2: The Innovation Lab** (`session-2/`) | 6 labs + reference simulator | Notebooks, Agent Builder, Pages, PowerPoint, Word, Scheduled Prompts |

All people, sponsors, emails, documents and numbers are **fictional training data**.

## Structure
- `index.html`, `session-1/`, `session-2/`, `case-file.html`, `resources.html`: the generated static site
- `data/`: Excel and Word lab files, plus a zip kit for each session
- `_build/`: generators (`story.py` is the single source of truth for the scenario)

## Rebuild
```bash
pip install openpyxl python-docx
python _build/gen_excel.py
cd _build && python gen_docs.py && python build_site.py
```
