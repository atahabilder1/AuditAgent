# Quick Start: Run AuditAgent with Detailed Logs

**Last Updated**: December 22, 2024

---

## ✨ The Fastest Way to See Everything

```bash
cd /data/AuditAgent
source venv/bin/activate
python examples/run_with_logging.py
```

**That's it!** You'll see a beautiful, detailed output with:
- 📋 5 phases with progress tracking
- 🎨 Color-coded results
- 📊 Visual charts and tables
- ⏱️ Timing information
- 🔍 Top vulnerabilities
- 💡 Next steps guidance

---

## 📖 What You'll See

### Phase 1: Initialization (1 second)
```
╭─────────────────────────────────────────────╮
│ AuditAgent v2.0                             │
│ AI-Powered Smart Contract Security Analysis │
│ With Economic Vulnerability Detection       │
╰─────────────────────────────────────────────╯

Contract: tests/contracts/VulnerableBank.sol
Output Directory: reports
Time: 2025-12-22 17:48:59

════════════════════════════════════════════════
PHASE 1: INITIALIZATION
Loading AuditAgent and checking environment...
════════════════════════════════════════════════

✅ AuditAgent initialized successfully
   • Configuration loaded
   • Analyzers ready: Slither, Pattern Detector, Advanced Detector
   • LLM Status: Disabled
```

**What's happening:**
- Loading configuration files
- Initializing analyzers (Slither, Pattern Matchers)
- Checking if Ollama LLM is available
- Setting up report generators

### Phase 2: Contract Loading (<1 second)
```
════════════════════════════════════════════════
PHASE 2: CONTRACT LOADING
Reading and parsing the smart contract...
════════════════════════════════════════════════

📄 Reading contract from: tests/contracts/VulnerableBank.sol
   • File size: 2859 bytes
   • Lines of code: 88
✅ Contract loaded successfully
```

**What's happening:**
- Reading the Solidity source code
- Counting lines and analyzing structure
- Validating file format

### Phase 3: Static Analysis (~8 seconds)
```
════════════════════════════════════════════════
PHASE 3: STATIC ANALYSIS
Running Slither and pattern-based detectors...
════════════════════════════════════════════════

[AuditAgent] Starting security audit for: tests/contracts/VulnerableBank.sol

[Phase 1/4] Running Slither static analysis...
  ✓ Found 16 potential issues

[Phase 2/4] Running Mythril symbolic execution...
  ✓ Found 0 potential issues

[Phase 3/4] Running vulnerability pattern detection...
  ✓ Detected 30 vulnerability patterns

[Phase 4/4] Running AI-powered security analysis...
  ✓ AI analysis completed with 0 recommendations

[Report] Generating audit report...
  ✓ Report saved to: reports/VulnerableBank_audit_20251222_174859.md

⠼ Running Slither static analysis... ━━━━━━━━ 0:00:00
⠼ Running pattern detectors...       ━━━━━━━━ 0:00:00
⠼ Running advanced detectors...      ━━━━━━━━ 0:00:00
✅ Analysis completed in 0.37 seconds
```

**What's happening:**
1. **Slither Analysis**: Compiling contract, running 70+ detectors
2. **Mythril**: Symbolic execution (skipped if timeout)
3. **Pattern Detection**: Regex-based vulnerability patterns
4. **AI Analysis**: LLM semantic analysis (if Ollama running)

### Phase 4: Results Aggregation (<1 second)
```
════════════════════════════════════════════════
PHASE 4: RESULTS AGGREGATION
Combining findings from all analyzers...
════════════════════════════════════════════════

   • Total vulnerabilities found: 30
   • Risk score: 100.0/100
   • Analyzers run: slither, mythril, ai
```

**What's happening:**
- Merging results from all analyzers
- Removing duplicates
- Calculating risk score (0-100)
- Categorizing by severity

### Phase 5: Report Generation (<1 second)
```
════════════════════════════════════════════════
PHASE 5: REPORT GENERATION
Creating detailed markdown report...
════════════════════════════════════════════════

📝 Report generated: reports/VulnerableBank_audit_20251222_174859.md
   • Report size: 11049 bytes
   • Format: Markdown
✅ Report saved successfully
```

**What's happening:**
- Creating markdown report
- Adding code snippets
- Formatting vulnerabilities
- Saving to reports/ directory

### Final Summary
```
════════════════════════════════════════════════
FINAL SUMMARY
════════════════════════════════════════════════

     Vulnerability Breakdown
┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Severity ┃ Count ┃ Visual     ┃
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ CRITICAL │    10 │ ██████████ │
│ HIGH     │     8 │ ████████   │
│ MEDIUM   │     8 │ ████████   │
│ LOW      │     4 │ ████       │
└──────────┴───────┴────────────┘

Risk Assessment:
🔴 CRITICAL RISK - Immediate action required!
   Multiple critical vulnerabilities detected. Do NOT deploy this contract.

Next Steps:
1. Review the detailed report: reports/VulnerableBank_audit_20251222_174859.md
2. Fix critical and high severity issues
3. Run audit again to verify fixes
4. Consider professional manual audit for production contracts

Top 3 Critical Findings:

  1. reentrancy
     Line 28: Potential reentrancy vulnerability detected...

  2. reentrancy
     Line 37: Potential reentrancy vulnerability detected...

  3. reentrancy
     Line 44: Potential reentrancy vulnerability detected...

════════════════════════════════════════════════
✅ Audit completed successfully!
════════════════════════════════════════════════
```

---

## 🎯 Command Options

### Standard Run (Detailed Logs)
```bash
python examples/run_with_logging.py
```

### Quiet Mode (Less Verbose)
```bash
python examples/run_with_logging.py --quiet
```

### Custom Contract
```bash
python examples/run_with_logging.py --contract path/to/YourContract.sol
```

### Save Output to File
```bash
python examples/run_with_logging.py 2>&1 | tee audit_log.txt
```

---

## 🔍 Understanding the Logs

### DEBUG Level Logs
```
[17:48:59] DEBUG    connect_tcp.started host='127.0.0.1' port=11434
           DEBUG    connect_tcp.failed
                    exception=ConnectError(ConnectionRefusedError(111,
                    'Connection refused'))
```
**Meaning**: Trying to connect to Ollama LLM server on port 11434. Failed because Ollama is not running (this is normal if you haven't installed it yet).

### WARNING Level Logs
```
WARNING  Could not verify Ollama models: Failed to connect to Ollama.
         Please check that Ollama is downloaded, running and accessible.
```
**Meaning**: LLM features are disabled. The system will continue with Slither + pattern detection only.

### INFO Level Logs
```
INFO     AI Analyzer initialized with gpt-4
```
**Meaning**: AI analyzer component is initialized (but won't run without Ollama).

### SUCCESS Indicators
```
✅ AuditAgent initialized successfully
✅ Contract loaded successfully
✅ Analysis completed in 0.37 seconds
✅ Report saved successfully
✅ Audit completed successfully!
```

---

## 📊 Understanding Results

### Risk Score Scale
- **0-30**: 🟢 LOW RISK - Minor issues
- **30-50**: 🟡 MEDIUM RISK - Some concerns
- **50-80**: 🟠 HIGH RISK - Significant problems
- **80-100**: 🔴 CRITICAL RISK - Severe vulnerabilities

### Severity Levels
- **CRITICAL** (🔴): Immediate exploit risk (reentrancy, arbitrary send)
- **HIGH** (🟠): Serious security issues (tx.origin, delegatecall)
- **MEDIUM** (🟡): Potential problems (timestamp, missing checks)
- **LOW** (🔵): Best practice violations (pragma, events)
- **INFORMATIONAL** (⚪): Code quality issues

---

## 🐛 Common Issues

### Issue 1: Ollama Connection Failed
```
WARNING  Could not verify Ollama models: Failed to connect to Ollama.
```

**This is normal!** Ollama is optional. The system works without it.

**To enable LLM features:**
```bash
# Install Ollama (requires sudo password)
curl -fsSL https://ollama.com/install.sh | sh

# Set model storage location
export OLLAMA_MODELS=/data/llm_models

# Start Ollama
ollama serve &

# Pull the model (19GB, takes 10-30 min)
ollama pull qwen2.5-coder:32b-instruct

# Re-run audit
python examples/run_with_logging.py
```

### Issue 2: Contract Not Found
```
❌ Error: Contract not found
```

**Fix:**
```bash
# Make sure you're in the project root
cd /data/AuditAgent

# Then run
python examples/run_with_logging.py
```

### Issue 3: Solidity Compilation Error
```
Error: Source file requires different compiler version
```

**Fix:**
```bash
source venv/bin/activate

# Check what version the contract needs
head -n 5 tests/contracts/VulnerableBank.sol
# Shows: pragma solidity ^0.7.6;

# Install and use that version
solc-select install 0.7.6
solc-select use 0.7.6

# Re-run audit
python examples/run_with_logging.py
```

---

## 📄 Viewing the Report

After the audit completes, view the detailed markdown report:

```bash
# Show the latest report
cat reports/VulnerableBank_audit_*.md | less

# Or open in your favorite editor
code reports/VulnerableBank_audit_20251222_174859.md
```

The report contains:
- Executive summary
- Full vulnerability list with code snippets
- Line numbers and descriptions
- Severity classifications
- Remediation recommendations

---

## ⏱️ Typical Execution Times

| Operation | Time |
|-----------|------|
| Initialization | <1 second |
| Contract Loading | <1 second |
| Slither Analysis | 3-5 seconds |
| Pattern Detection | 1-2 seconds |
| Advanced Detection | 1-2 seconds |
| LLM Analysis (if enabled) | 10-30 seconds |
| Report Generation | <1 second |
| **Total (without LLM)** | **~8-10 seconds** |
| **Total (with LLM)** | **~30-60 seconds** |

---

## 💡 Pro Tips

1. **First Time**: Run the example contract to understand the output
2. **Your Contracts**: Use `--contract` to audit your own files
3. **Save Logs**: Use `| tee` to save output for later review
4. **Compare Runs**: Run multiple times to see consistency
5. **Enable LLM**: Install Ollama for AI-powered semantic analysis
6. **Quiet Mode**: Use `--quiet` when you just want results
7. **Watch Resources**: Run `nvidia-smi` in another terminal to see GPU usage (if LLM enabled)

---

## 🚀 Next Steps

After running your first audit:

1. **Read the Report**: Understand each vulnerability
2. **Learn Patterns**: Study common vulnerability types
3. **Try Your Contracts**: Audit your own smart contracts
4. **Install Ollama**: Get AI-powered analysis
5. **Explore Features**: Try economic analysis, exploit generation
6. **Read Full Docs**: See `README_COMPLETE.md` for everything

---

## 📚 More Information

- **Complete Documentation**: [README_COMPLETE.md](README_COMPLETE.md)
- **Detailed Logging Guide**: [HOW_TO_RUN_WITH_LOGS.md](HOW_TO_RUN_WITH_LOGS.md)
- **Installation Guide**: [docs/chapters/02-installation.md](docs/chapters/02-installation.md)
- **Quick Start Guide**: [docs/chapters/03-quickstart.md](docs/chapters/03-quickstart.md)

---

**Ready?** Let's audit some contracts! 🔍

```bash
cd /data/AuditAgent
source venv/bin/activate
python examples/run_with_logging.py
```
