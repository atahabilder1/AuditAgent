# AuditAgent Run Modes - Comparison Guide

Choose the right mode for your needs!

---

## 🎯 Quick Comparison

| Mode | Command | Output Level | Best For |
|------|---------|--------------|----------|
| **Detailed Logs** | `python examples/run_with_logging.py` | 📊 Maximum | Learning, debugging |
| **Standard** | `python examples/basic_usage.py` | 📋 Normal | Regular audits |
| **Silent** | `python examples/run_silent.py` | 🔇 Minimal | CI/CD, scripting |
| **Programmatic** | Import API | 💻 Custom | Integration |

---

## 1️⃣ Detailed Logs Mode (Maximum Detail)

### Command
```bash
cd /data/AuditAgent
source venv/bin/activate
python examples/run_with_logging.py
```

### Output Example
```
╭─────────────────────────────────────────────╮
│ AuditAgent v2.0                             │
│ AI-Powered Smart Contract Security Analysis │
╰─────────────────────────────────────────────╯

Contract: tests/contracts/VulnerableBank.sol
Output Directory: reports
Time: 2025-12-22 17:48:59

════════════════════════════════════════════════
PHASE 1: INITIALIZATION
Loading AuditAgent and checking environment...
════════════════════════════════════════════════

[17:48:59] DEBUG    connect_tcp.started host='127.0.0.1' port=11434
           DEBUG    connect_tcp.failed
           WARNING  Could not verify Ollama models
           INFO     AI Analyzer initialized with gpt-4
✅ AuditAgent initialized successfully
   • Configuration loaded
   • Analyzers ready: Slither, Pattern Detector, Advanced Detector
   • LLM Status: Disabled

════════════════════════════════════════════════
PHASE 2: CONTRACT LOADING
Reading and parsing the smart contract...
════════════════════════════════════════════════

📄 Reading contract from: tests/contracts/VulnerableBank.sol
   • File size: 2859 bytes
   • Lines of code: 88
✅ Contract loaded successfully

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

⠼ Running Slither static analysis... ━━━━━━━━ 0:00:00
⠼ Running pattern detectors...       ━━━━━━━━ 0:00:00
⠼ Running advanced detectors...      ━━━━━━━━ 0:00:00
✅ Analysis completed in 0.37 seconds

════════════════════════════════════════════════
PHASE 4: RESULTS AGGREGATION
Combining findings from all analyzers...
════════════════════════════════════════════════

   • Total vulnerabilities found: 30
   • Risk score: 100.0/100
   • Analyzers run: slither, mythril, ai

════════════════════════════════════════════════
PHASE 5: REPORT GENERATION
Creating detailed markdown report...
════════════════════════════════════════════════

📝 Report generated: reports/VulnerableBank_audit_20251222_174859.md
   • Report size: 11049 bytes
   • Format: Markdown
✅ Report saved successfully

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

### Features
- ✅ 5 phases clearly labeled
- ✅ Progress bars with spinners
- ✅ Color-coded output
- ✅ Visual charts and tables
- ✅ Timing information
- ✅ Debug logs visible
- ✅ Risk assessment
- ✅ Top vulnerabilities highlighted
- ✅ Next steps guidance

### Best For
- 🎓 **Learning**: Understanding what happens at each step
- 🐛 **Debugging**: Seeing detailed logs when something fails
- 📚 **Education**: Teaching others about the audit process
- 🔬 **Research**: Detailed analysis of the system behavior

---

## 2️⃣ Standard Mode (Normal Output)

### Command
```bash
cd /data/AuditAgent
source venv/bin/activate
python examples/basic_usage.py
```

### Output Example
```
================================================================================
AuditAgent - Basic Usage Example
================================================================================

Auditing contract: tests/contracts/VulnerableBank.sol


[AuditAgent] Starting security audit for: tests/contracts/VulnerableBank.sol
================================================================================

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

================================================================================
[AuditAgent] Audit complete! Total vulnerabilities: 30
  - Critical: 10
  - High: 8
  - Medium: 8
  - Low: 4
================================================================================


================================================================================
AUDIT SUMMARY
================================================================================
Total Vulnerabilities: 30
Risk Score: 100.0/100

Severity Breakdown:
  CRITICAL: 10
  HIGH: 8
  MEDIUM: 8
  LOW: 4

Detailed report saved to: reports/VulnerableBank_audit_20251222_174859.md
```

### Features
- ✅ Clean, readable output
- ✅ Phase progress indicators
- ✅ Essential information only
- ✅ Summary at the end
- ✅ Report location
- ❌ No debug logs
- ❌ No detailed phase descriptions
- ❌ No visual charts

### Best For
- 🚀 **Regular Use**: Daily auditing tasks
- 📊 **Quick Checks**: Fast vulnerability scanning
- 💼 **Professional**: Clean output for reports
- ⚡ **Speed**: Minimal overhead

---

## 3️⃣ Silent Mode (Minimal Output)

### Command
```bash
cd /data/AuditAgent
source venv/bin/activate
python examples/run_silent.py
```

### Output Example
```
[AuditAgent] Starting security audit for: tests/contracts/VulnerableBank.sol
================================================================================

[Phase 1/4] Running Slither static analysis...
  ✓ Found 16 potential issues

[Phase 2/4] Running Mythril symbolic execution...
  ✓ Found 0 potential issues

[Phase 3/4] Running vulnerability pattern detection...
  ✓ Detected 30 vulnerability patterns

[Phase 4/4] Running AI-powered security analysis...
  ✓ AI analysis completed with 0 recommendations

[Report] Generating audit report...
  ✓ Report saved to: reports/VulnerableBank_audit_20251222_175458.md

================================================================================
[AuditAgent] Audit complete! Total vulnerabilities: 30
  - Critical: 10
  - High: 8
  - Medium: 8
  - Low: 4
================================================================================

Vulnerabilities: 30
Risk Score: 100/100
Report: reports/VulnerableBank_audit_20251222_175458.md
```

### Completely Silent (Errors Only)
```bash
python examples/run_silent.py 2>/dev/null
```
Output:
```
Vulnerabilities: 30
Risk Score: 100/100
Report: reports/VulnerableBank_audit_20251222_175458.md
```

### Features
- ✅ Minimal output
- ✅ Just the results
- ✅ No debug logs
- ✅ Fast execution
- ❌ No phase descriptions
- ❌ No visual elements
- ❌ No warnings/info

### Best For
- 🤖 **CI/CD Pipelines**: Automated testing
- 📜 **Scripting**: Batch processing contracts
- 🔄 **Integration**: Calling from other tools
- 📈 **Monitoring**: Log aggregation systems

---

## 4️⃣ Programmatic Mode (Python API)

### Code Example
```python
from src.audit_agent import AuditAgent

# Initialize (silent)
agent = AuditAgent()

# Run audit
results = agent.audit_contract(
    contract_path="tests/contracts/VulnerableBank.sol",
    output_dir="reports"
)

# Access results programmatically
print(f"Total vulnerabilities: {results['summary']['total_vulnerabilities']}")
print(f"Risk score: {results['summary']['risk_score']}")

# Access individual vulnerabilities
for vuln in results['vulnerabilities']:
    if vuln['severity'] == 'critical':
        print(f"Critical: {vuln['type']} at line {vuln['line']}")

# Get report path
report = results.get('report_path')
```

### Output
```python
# You control what's printed
Total vulnerabilities: 30
Risk score: 100.0
Critical: reentrancy at line 28
Critical: reentrancy at line 37
Critical: reentrancy at line 44
...
```

### Features
- ✅ Full programmatic control
- ✅ Custom output format
- ✅ Access to raw data
- ✅ Integration-friendly
- ✅ Exception handling
- ✅ Flexible logging

### Best For
- 🔧 **Custom Tools**: Building your own security tools
- 🌐 **Web APIs**: Creating REST/GraphQL endpoints
- 📊 **Data Analysis**: Processing many contracts
- 🏗️ **Integration**: Embedding in larger systems

---

## 📊 Feature Comparison Table

| Feature | Detailed Logs | Standard | Silent | Programmatic |
|---------|--------------|----------|--------|--------------|
| **Phases shown** | 5 detailed | 4 simple | 4 simple | Custom |
| **Progress bars** | ✅ Yes | ❌ No | ❌ No | Custom |
| **Color output** | ✅ Yes | ⚠️ Basic | ❌ No | Custom |
| **Visual charts** | ✅ Yes | ❌ No | ❌ No | Custom |
| **Debug logs** | ✅ Yes | ❌ No | ❌ No | Custom |
| **Timing info** | ✅ Yes | ❌ No | ❌ No | Custom |
| **Risk assessment** | ✅ Detailed | ⚠️ Basic | ⚠️ Score only | Custom |
| **Top vulns** | ✅ Yes | ❌ No | ❌ No | Custom |
| **Next steps** | ✅ Yes | ❌ No | ❌ No | Custom |
| **File size** | Medium | Small | Smallest | Depends |
| **Speed** | Normal | Normal | Fastest | Fastest |
| **Learning curve** | Easy | Easy | Easy | Medium |

---

## 🎯 Which Mode Should I Use?

### Use **Detailed Logs** (`run_with_logging.py`) if:
- 🎓 You're learning how the system works
- 🐛 You're debugging issues
- 📚 You want to understand each phase
- 🔍 You need to see what's happening in real-time

### Use **Standard** (`basic_usage.py`) if:
- 🚀 You want clean, professional output
- ⚡ You're running regular audits
- 📊 You need essential information
- 💼 You're sharing results with others

### Use **Silent** (`run_silent.py`) if:
- 🤖 You're automating audits (CI/CD)
- 📜 You're processing many contracts
- 🔄 You're integrating with other tools
- 📈 You only need final results

### Use **Programmatic** (Python API) if:
- 🔧 You're building custom tools
- 🌐 You're creating an API/web interface
- 📊 You need to process results programmatically
- 🏗️ You're embedding in a larger system

---

## 🔧 Advanced Options

### Suppress Specific Logs

#### Hide Warnings Only
```bash
python examples/basic_usage.py 2>&1 | grep -v WARNING
```

#### Hide All Stderr (Warnings + Errors)
```bash
python examples/basic_usage.py 2>/dev/null
```

#### Save to File Without Displaying
```bash
python examples/run_with_logging.py > audit.log 2>&1
```

#### Show Only Errors
```bash
export LOG_LEVEL=ERROR
python examples/basic_usage.py
```

### Custom Python Script with Logging Control

```python
import logging

# Completely silent
logging.basicConfig(level=logging.CRITICAL)

# Or only errors
logging.basicConfig(level=logging.ERROR)

# Or warnings and above
logging.basicConfig(level=logging.WARNING)

# Or info and above (default)
logging.basicConfig(level=logging.INFO)

# Or everything including debug
logging.basicConfig(level=logging.DEBUG)

from src.audit_agent import AuditAgent
agent = AuditAgent()
results = agent.audit_contract("contract.sol", "reports")
```

---

## ⏱️ Performance Comparison

| Mode | Execution Time | Output Size | CPU Usage | Best Use Case |
|------|----------------|-------------|-----------|---------------|
| Detailed Logs | ~10 sec | ~50 KB | Normal | Learning |
| Standard | ~10 sec | ~5 KB | Normal | Daily use |
| Silent | ~10 sec | ~1 KB | Normal | Automation |
| Programmatic | ~10 sec | Custom | Normal | Integration |

**Note**: Execution time is similar across all modes. The difference is only in output formatting.

---

## 📝 Examples for Different Scenarios

### Scenario 1: Learning the System
```bash
# Use detailed logs
python examples/run_with_logging.py
```

### Scenario 2: Quick Daily Audit
```bash
# Use standard mode
python examples/basic_usage.py
```

### Scenario 3: CI/CD Pipeline
```bash
# Use silent mode, check exit code
python examples/run_silent.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Audit completed"
else
    echo "Audit failed"
    exit 1
fi
```

### Scenario 4: Batch Processing 100 Contracts
```python
# Use programmatic mode
from src.audit_agent import AuditAgent
import logging

logging.basicConfig(level=logging.ERROR)  # Silent
agent = AuditAgent()

contracts = glob.glob("contracts/*.sol")
for contract in contracts:
    results = agent.audit_contract(contract, "reports")
    print(f"{contract}: {results['summary']['total_vulnerabilities']} vulns")
```

### Scenario 5: Web API
```python
# Flask API example
from flask import Flask, jsonify
from src.audit_agent import AuditAgent
import logging

logging.basicConfig(level=logging.ERROR)
app = Flask(__name__)
agent = AuditAgent()

@app.route('/audit/<contract_name>')
def audit(contract_name):
    results = agent.audit_contract(f"contracts/{contract_name}", "reports")
    return jsonify(results['summary'])
```

---

## 🎓 Summary

**Quick Reference:**

```bash
# Maximum detail (learning)
python examples/run_with_logging.py

# Normal output (regular use)
python examples/basic_usage.py

# Minimal output (automation)
python examples/run_silent.py

# Custom control (integration)
python -c "from src.audit_agent import AuditAgent; ..."
```

Choose the mode that fits your needs! All modes perform the same analysis - only the output differs.

---

**Questions?** Check [README_COMPLETE.md](README_COMPLETE.md) for full documentation.
