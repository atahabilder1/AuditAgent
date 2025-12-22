# How to Run AuditAgent v2.0

## Quick Start (5 Minutes)

### Step 1: Setup

```bash
cd /data/AuditAgent
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh
```

Wait 10-30 minutes for installation to complete.

### Step 2: Activate

```bash
source venv/bin/activate
ollama serve &
```

### Step 3: Run Your First Audit

```bash
python examples/basic_usage.py
```

Done! View the report in `reports/`

---

## Full Documentation

**Complete book-style documentation is in the `docs/` folder:**

📚 **START HERE**: [docs/README.md](docs/README.md)

### Quick Links

- **Installation**: [docs/chapters/02-installation.md](docs/chapters/02-installation.md)
- **Quick Start**: [docs/chapters/03-quickstart.md](docs/chapters/03-quickstart.md)
- **References**: [docs/references/citations.md](docs/references/citations.md)

### Documentation Features

✅ **20 Chapters** - Complete coverage of all features
✅ **Book-Style** - Professional structure with hyperlinks
✅ **40+ References** - Academic papers and technical docs
✅ **Step-by-Step** - Tutorials and workflows
✅ **Greatest Detail** - Over 150,000 words planned
✅ **Update Tracking** - Changes logged in DOC_UPDATES.md

---

## For Research

See [docs/chapters/12-research.md](docs/chapters/12-research.md) for:
- Research methodology
- Experimental design
- Evaluation framework
- Statistical analysis

---

**Questions?** Read the full documentation in `docs/`
