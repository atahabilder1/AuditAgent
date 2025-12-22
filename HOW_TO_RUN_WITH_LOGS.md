# How to Run AuditAgent with Detailed Logging

This guide shows you how to run AuditAgent and see detailed logs of what's happening at each step.

---

## Quick Start (With Beautiful Logs)

```bash
cd /data/AuditAgent
source venv/bin/activate
python examples/run_with_logging.py
```

**What you'll see:**
- ✅ Phase-by-phase execution
- 📊 Progress bars and spinners
- 🎨 Color-coded output
- 📈 Detailed statistics
- ⏱️ Timing information
- 📝 Real-time status updates

---

## Different Running Modes

### 1. **Detailed Logging (Recommended for Learning)**

```bash
python examples/run_with_logging.py
```

**Shows:**
- Phase 1: Initialization
- Phase 2: Contract Loading
- Phase 3: Static Analysis (with progress bars)
- Phase 4: Results Aggregation
- Phase 5: Report Generation
- Beautiful summary tables
- Risk assessment
- Next steps

### 2. **Quiet Mode (Less Verbose)**

```bash
python examples/run_with_logging.py --quiet
```

**Shows:**
- Only important status messages
- Results summary
- Errors and warnings

### 3. **Custom Contract**

```bash
python examples/run_with_logging.py --contract path/to/YourContract.sol
```

### 4. **Debug Mode (Maximum Detail)**

```bash
# Set Python logging to DEBUG
PYTHONPATH=. python -m src.audit_agent tests/contracts/VulnerableBank.sol --verbose
```

---

## Understanding the Output

### Phase 1: Initialization
```
════════════════════════════════════════════════════════════════════════════════
PHASE 1: INITIALIZATION
Loading AuditAgent and checking environment...
════════════════════════════════════════════════════════════════════════════════

⠹ Initializing AuditAgent...
✅ AuditAgent initialized successfully
   • Configuration loaded
   • Analyzers ready: Slither, Pattern Detector, Advanced Detector
   • LLM Status: Disabled
```

**What's happening:**
- Loading configuration from `config/default_config.json`
- Initializing analyzers (Slither, pattern detectors)
- Checking for LLM availability (Ollama)
- Setting up report generators

### Phase 2: Contract Loading
```
════════════════════════════════════════════════════════════════════════════════
PHASE 2: CONTRACT LOADING
Reading and parsing the smart contract...
════════════════════════════════════════════════════════════════════════════════

📄 Reading contract from: tests/contracts/VulnerableBank.sol
   • File size: 2847 bytes
   • Lines of code: 89
✅ Contract loaded successfully
```

**What's happening:**
- Reading the Solidity source code
- Parsing contract structure
- Extracting metadata (size, lines of code)
- Validating file format

### Phase 3: Static Analysis
```
════════════════════════════════════════════════════════════════════════════════
PHASE 3: STATIC ANALYSIS
Running Slither and pattern-based detectors...
════════════════════════════════════════════════════════════════════════════════

⠹ Running Slither static analysis... ━━━━━━━━━━━━━━━━━━━━ 0:00:05
⠹ Running pattern detectors...      ━━━━━━━━━━━━━━━━━━━━ 0:00:02
⠹ Running advanced detectors...     ━━━━━━━━━━━━━━━━━━━━ 0:00:01
✅ Analysis completed in 8.50 seconds
```

**What's happening:**
1. **Slither Static Analysis**
   - Compiling contract with solc
   - Building AST (Abstract Syntax Tree)
   - Running 70+ built-in detectors
   - Finding code-level vulnerabilities

2. **Pattern Detection**
   - Regex-based pattern matching
   - Looking for known vulnerability patterns
   - Reentrancy, tx.origin, unchecked calls, etc.

3. **Advanced Detection**
   - Custom heuristics
   - Cross-function analysis
   - Advanced vulnerability detection

### Phase 4: Results Aggregation
```
════════════════════════════════════════════════════════════════════════════════
PHASE 4: RESULTS AGGREGATION
Combining findings from all analyzers...
════════════════════════════════════════════════════════════════════════════════

   • Total vulnerabilities found: 30
   • Risk score: 100.0/100
   • Analyzers run: slither, pattern_matcher, advanced_detector
```

**What's happening:**
- Merging results from all analyzers
- Deduplicating findings
- Normalizing severity levels
- Calculating risk score (0-100)

### Phase 5: Report Generation
```
════════════════════════════════════════════════════════════════════════════════
PHASE 5: REPORT GENERATION
Creating detailed markdown report...
════════════════════════════════════════════════════════════════════════════════

📝 Report generated: reports/VulnerableBank_audit_20251222_173008.md
   • Report size: 15384 bytes
   • Format: Markdown
✅ Report saved successfully
```

**What's happening:**
- Creating markdown report
- Formatting vulnerabilities
- Adding code snippets
- Including severity breakdown
- Saving to reports/ directory

### Final Summary
```
════════════════════════════════════════════════════════════════════════════════
FINAL SUMMARY
════════════════════════════════════════════════════════════════════════════════

                        Vulnerability Breakdown
┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Severity      ┃ Count ┃ Visual                                   ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ CRITICAL      │    10 │ ██████████                               │
│ HIGH          │     8 │ ████████                                 │
│ MEDIUM        │     8 │ ████████                                 │
│ LOW           │     4 │ ████                                     │
└───────────────┴───────┴──────────────────────────────────────────┘

Risk Assessment:
🔴 CRITICAL RISK - Immediate action required!
   Multiple critical vulnerabilities detected. Do NOT deploy this contract.

Next Steps:
1. Review the detailed report: reports/VulnerableBank_audit_20251222_173008.md
2. Fix critical and high severity issues
3. Run audit again to verify fixes
4. Consider professional manual audit for production contracts

Top 3 Critical Findings:

  1. Reentrancy
     Line 28: Potential reentrancy vulnerability detected...

  2. Arbitrary-Send-Eth
     Line 36: VulnerableBank.emergencyWithdraw(address,uint256) sends eth to arb...

  3. Controlled-Delegatecall
     Line 72: VulnerableBank.delegateExecute(address,bytes) uses delegatecall...
```

---

## Log Files

### Where Logs Are Saved

By default, logs are displayed in the console. To save to a file:

```bash
# Save all output to file
python examples/run_with_logging.py 2>&1 | tee audit_log.txt

# Save only errors
python examples/run_with_logging.py 2> errors.log

# Save everything (stdout + stderr)
python examples/run_with_logging.py &> full_log.txt
```

---

## Enabling LLM Logging (If Ollama Installed)

If you've installed Ollama, you can see LLM analysis logs:

```bash
# Start Ollama with logging
ollama serve 2>&1 | tee ollama.log &

# Run audit (will now include LLM analysis)
python examples/run_with_logging.py
```

**LLM logs will show:**
- Prompt sent to Qwen model
- Model thinking/reasoning
- Generated analysis
- Parsed JSON response
- Fallback strategies (if needed)

---

## Understanding Log Levels

### DEBUG Level (Maximum Detail)
```python
# In run_with_logging.py, edit:
setup_logging(verbose=True)
```

**Shows:**
- Every function call
- Internal state changes
- Slither internal operations
- Pattern matching details
- Parser operations

### INFO Level (Normal)
```python
setup_logging(verbose=False)
```

**Shows:**
- Phase transitions
- Important events
- Results summaries
- Warnings

### WARNING Level (Errors Only)
```bash
# Set environment variable
export LOG_LEVEL=WARNING
python examples/run_with_logging.py
```

**Shows:**
- Errors
- Critical warnings
- Failures

---

## Monitoring System Resources

### See GPU Usage (If Using LLM)

```bash
# In another terminal
watch -n 1 nvidia-smi
```

**Shows:**
- GPU memory usage
- GPU utilization %
- Running processes

### See CPU/Memory Usage

```bash
# In another terminal
htop

# Or watch specific process
watch -n 1 'ps aux | grep python'
```

---

## Real-Time Progress Tracking

The `run_with_logging.py` script includes:

1. **Spinners** - Shows activity during long operations
2. **Progress Bars** - Visual indication of progress
3. **Time Elapsed** - How long each phase takes
4. **Color Coding**:
   - 🟢 Green = Success
   - 🔴 Red = Critical/Error
   - 🟡 Yellow = Warning/Medium
   - 🔵 Blue = Info
   - ⚪ White/Dim = Debug

---

## Debugging Tips

### 1. **Contract Not Found**
```
❌ Error: Contract not found
💡 Tip: Make sure you're running from the project root directory.
Current directory: /home/user/somewhere
```

**Fix:**
```bash
cd /data/AuditAgent
python examples/run_with_logging.py
```

### 2. **Slither Compilation Error**
```
Error: Solidity version mismatch
```

**Fix:**
```bash
source venv/bin/activate
solc-select use 0.7.6  # Match contract pragma
python examples/run_with_logging.py
```

### 3. **LLM Not Available**
```
✅ AuditAgent initialized successfully
   • LLM Status: Disabled
```

**This is normal** if Ollama isn't installed. The system still works with Slither + pattern detection.

**To enable LLM:**
```bash
ollama serve &
python examples/run_with_logging.py
```

---

## Example Full Run

```bash
cd /data/AuditAgent
source venv/bin/activate

# Run with full logging
python examples/run_with_logging.py

# Expected output:
# 1. Beautiful header
# 2. 5 phases with progress indicators
# 3. Results table
# 4. Risk assessment
# 5. Top vulnerabilities
# 6. Next steps
# Total time: 8-10 seconds
```

---

## Comparing Log Outputs

### Basic Example (Less Detail)
```bash
python examples/basic_usage.py
```
Output:
```
================================================================================
AuditAgent - Basic Usage Example
================================================================================

Auditing contract: tests/contracts/VulnerableBank.sol

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

Detailed report saved to: reports/VulnerableBank_audit_20251222_173008.md
```

### Enhanced Example (More Detail)
```bash
python examples/run_with_logging.py
```
Output: *(See full example above with phases, progress bars, tables, etc.)*

---

## Command Reference

```bash
# Standard run with logging
python examples/run_with_logging.py

# Quiet mode
python examples/run_with_logging.py --quiet

# Custom contract
python examples/run_with_logging.py --contract MyContract.sol

# Save output to file
python examples/run_with_logging.py 2>&1 | tee audit.log

# Show help
python examples/run_with_logging.py --help
```

---

## Next Steps

After running the audit:

1. **Review the report**: `cat reports/VulnerableBank_audit_*.md`
2. **Understand vulnerabilities**: Check each finding in detail
3. **Fix issues**: Modify the contract
4. **Re-run audit**: Verify fixes worked
5. **Iterate**: Repeat until risk score is acceptable

---

## Tips for Learning

1. **Start with the test contract** - It's intentionally vulnerable so you can see all features
2. **Run multiple times** - Observe consistency
3. **Try different contracts** - See how results vary
4. **Enable LLM** - Compare with/without AI analysis
5. **Read the reports** - Learn about each vulnerability type

---

**Questions?** Check the main documentation: [README_COMPLETE.md](README_COMPLETE.md)
