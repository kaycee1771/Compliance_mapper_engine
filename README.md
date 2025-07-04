# Compliance Mapper Engine

The **Compliance Mapper Engine** is an AI-powered backend framework designed to automatically map organizational artifacts—such as policy documents, infrastructure configurations, and Git metadata—against industry-standard cybersecurity and digital resilience controls, including **NIS2**, **DORA**, and **ISO/IEC 27001**.

## Features

- **AI-Powered Semantic Matching** – Uses Sentence Transformers to match artifacts to controls.
- **Raw Input Ingestion** – Supports `.pdf`, `.docx`, `.txt`, infra config files, and Git commit metadata.
- **Ontology Builder** – Converts regulation text into structured, enriched control JSONs via summarization.
- **Gap Reporting** – Outputs a Markdown report showing covered vs. uncovered compliance items.
- **Watchdog Automation (Phase 5)** – Re-runs the pipeline on new changes in inputs.
- **NLP Entity Extraction** – Identifies named entities from inputs for categorization.

## Folder Structure

```
Compliance_mapper/
├── compliance_mapper.py          # Unified entry point (CLI)
├── core/                         # All core logic
│   ├── collector.py              # Phase 1: Ingest raw files
│   ├── ontology.py               # Phase 2: Build controls ontology
│   ├── mapper.py                 # Phase 3: Match inputs to controls
│   ├── reporter.py               # Phase 4: Gap report
│   ├── watcher.py                # Phase 5: Auto re-run on change
├── data/
│   ├── raw/                      # All input files go here
│   │   ├── policies/             # .pdf, .docx, .txt
│   │   ├── git_repos/           # Cloned Git repositories
│   │   └── infra_configs/       # YAML/JSON/Terraform configs
│   └── parsed/                  # Processed outputs
├── controls/                    # Enriched JSON controls
├── output/
│   └── gap_report.md            # Final report
└── README.md
```

## How It Works (5 Phases)

### Phase 1: Collector
Extracts text and metadata from:
- PDF/DOCX/TXT policies using `pdfplumber`, `python-docx`
- Infra config files using regex + NLP
- Git commit messages from repos

### Phase 2: Ontology Generator
- Generates enriched controls from NIS2, DORA, ISO27001 raw text using transformers summarizer
- Saves to `controls/*.json`

### Phase 3: AI Compliance Mapper
- Flattens all inputs
- Cleans and embeds with `all-MiniLM-L6-v2`
- Finds semantic similarity with controls using cosine similarity

### Phase 4: Gap Reporter
- Counts coverage
- Displays matched/unmatched controls in `output/gap_report.md`

### Phase 5: Continuous Watchdog (optional)
- Watches `data/raw/` for changes
- Re-triggers Phases 1-4 automatically

## Input Requirements

- **Policies:** `.pdf`, `.docx`, `.txt`
- **Infra Configs:** Any `.yaml`, `.json`, `.tf`, `.conf` files
- **Git Repos:** Clone repos inside `data/raw/git_repos`

## Intelligence

- Transformer-based summarization of regulation sections
- Sentence-BERT embeddings for semantic similarity
- NLP entity recognition for advanced mapping
- Auto-updated controls with summaries as `title` field

## Output

- **Semantic Matches** – `data/parsed/phase3_matches.yaml`
- **Gap Report** – `output/gap_report.md` with full list of uncovered controls

## Future Improvements

- Add UI for interactive exploration

## Installation

```bash
pip install -r requirements.txt
python compliance_mapper.py --full
```

## Start Watchdog (Optional)

```bash
python compliance_mapper.py --phase5
```

---

MIT License © 2025  
Built for security compliance teams.
