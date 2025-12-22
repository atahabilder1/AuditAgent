# Chapter 3: Quick Start Guide

[← Previous: Installation](02-installation.md) | [Home](../README.md) | [Next: Architecture →](04-architecture.md)

---

## Table of Contents
- [3.1 Your First Audit](#31-your-first-audit)
- [3.2 Understanding the Output](#32-understanding-the-output)
- [3.3 Basic Commands](#33-basic-commands)
- [3.4 Common Workflows](#34-common-workflows)

---

## 3.1 Your First Audit

Let's run your first smart contract security audit in under 5 minutes!

### Prerequisites

Make sure you've completed [Chapter 2: Installation](02-installation.md).

**Quick check**:
```bash
cd /data/AuditAgent
source venv/bin/activate
ollama serve &  # Start Ollama in background
```

### Step 1: Audit a Test Contract

We've included vulnerable test contracts for demonstration.

```bash
# Audit the vulnerable bank contract
python examples/basic_usage.py
```

### Step 2: What Happens

You'll see output like this:

```
[AuditAgent] Starting security audit for: tests/contracts/VulnerableBank.sol
================================================================================

[Phase 1/4] Running Slither static analysis...
  Analyzing contract structure...
  Running 80+ detectors...
  ✓ Found 3 potential issues

[Phase 2/4] Running Mythril symbolic execution...
  Exploring execution paths...
  Checking for vulnerabilities...
  ✓ Found 2 potential issues

[Phase 3/4] Running vulnerability pattern detection...
  Checking for common patterns...
  Cross-referencing with Slither results...
  ✓ Detected 2 vulnerability patterns

[Phase 4/4] Running AI-powered security analysis...
  Analyzing with LLM...
  🤖 Qwen2.5-Coder-32B analyzing contract... (this may take 30-60 seconds)
  ✓ AI analysis completed with 3 recommendations

[Report] Generating audit report...
  ✓ Report saved to: reports/VulnerableBank_20241222_153045/

================================================================================
[AuditAgent] Audit complete! Total vulnerabilities: 5
  - Critical: 1
  - High: 2
  - Medium: 2
  - Low: 0
================================================================================

Risk Score: 65/100 (HIGH RISK)
```

### Step 3: View the Report

```bash
# Navigate to the report directory
cd reports/VulnerableBank_20241222_153045/

# You'll find:
# - audit_report.json    (machine-readable)
# - audit_report.md      (human-readable)
# - slither_output.txt   (raw Slither output)

# View the markdown report
cat audit_report.md
```

**Report excerpt**:
```markdown
# Security Audit Report

**Contract**: VulnerableBank.sol
**Audit Date**: 2024-12-22 15:30:45
**Risk Score**: 65/100 (HIGH RISK)

## Executive Summary

This contract contains **5 vulnerabilities**:
- 1 Critical severity
- 2 High severity
- 2 Medium severity

## Critical Issues

### 1. Reentrancy Vulnerability

**Location**: `withdraw()` function, line 42
**Severity**: CRITICAL
**Impact**: Attacker can drain all contract funds

**Vulnerable Code**:
```solidity
function withdraw() public {
    uint256 amount = balances[msg.sender];
    (bool success,) = msg.sender.call{value: amount}("");  // ❌ External call before state update
    require(success);
    balances[msg.sender] = 0;  // ❌ State updated AFTER call
}
```

**Exploit Scenario**:
1. Attacker deposits 1 ETH
2. Attacker calls withdraw()
3. In the callback, attacker calls withdraw() again (reentrancy)
4. Step 3 repeats until contract is drained

**Recommended Fix**:
```solidity
function withdraw() public {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;  // ✅ Update state FIRST
    (bool success,) = msg.sender.call{value: amount}("");
    require(success);
}
```

... (more vulnerabilities)
```

Congratulations! You've completed your first audit! 🎉

---

## 3.2 Understanding the Output

### Audit Phases Explained

AuditAgent runs in **4 phases**:

#### Phase 1: Static Analysis (Slither)
```
What: Pattern-based code analysis
Time: 5-30 seconds
Finds: Code-level vulnerabilities
Example: Unprotected functions, dangerous calls
```

**What Slither detects**:
- Reentrancy
- Unprotected functions
- Dangerous delegatecall
- Timestamp dependence
- Integer overflow (pre-0.8.0)
- 75+ other patterns

#### Phase 2: Symbolic Execution (Mythril) - Optional
```
What: Explore all possible execution paths
Time: 1-5 minutes
Finds: Complex logic bugs
Example: Unreachable code, assertion violations
```

**Note**: Mythril is optional and can be disabled for faster audits.

#### Phase 3: Pattern Detection
```
What: Custom vulnerability detectors
Time: 1-5 seconds
Finds: Project-specific patterns
Example: Missing access control, unvalidated inputs
```

#### Phase 4: AI Analysis (Qwen 32B)
```
What: Semantic understanding with LLM
Time: 30-90 seconds
Finds: Context-aware issues
Example: Business logic flaws, economic issues
```

**What the LLM does**:
1. Reads the entire contract
2. Understands the business logic
3. Contextualizes Slither findings
4. Generates recommendations
5. Prioritizes issues by severity

### Severity Levels

| Level | Description | Example | Action |
|-------|-------------|---------|--------|
| **CRITICAL** | Can lead to total loss of funds | Reentrancy, Arbitrary send | Fix immediately |
| **HIGH** | Can lead to significant loss | Access control bypass | Fix before deployment |
| **MEDIUM** | Can lead to unexpected behavior | Block timestamp use | Review and fix |
| **LOW** | Code quality or gas optimization | Missing events | Address in next version |
| **INFORMATIONAL** | Best practice violations | Floating pragma | Optional improvement |

### Risk Score Calculation

Risk score (0-100) is calculated as:

```python
score = (critical * 25) + (high * 10) + (medium * 5) + (low * 2)
score = min(score, 100)  # Cap at 100
```

**Interpretation**:
- **0-20**: Low Risk (safe to deploy)
- **21-40**: Medium Risk (review recommended)
- **41-60**: High Risk (fixes required)
- **61-100**: Critical Risk (DO NOT DEPLOY)

---

## 3.3 Basic Commands

### Command Line Interface

```bash
# Activate environment
source venv/bin/activate

# Start Ollama (in background)
ollama serve &
```

### Audit a Local File

```bash
# Basic audit
python -m src.audit_agent path/to/Contract.sol

# With custom output directory
python -m src.audit_agent path/to/Contract.sol --output reports/my_audit

# Skip AI analysis (faster)
python -m src.audit_agent path/to/Contract.sol --no-ai

# Verbose mode
python -m src.audit_agent path/to/Contract.sol --verbose
```

### Audit a Deployed Contract

```bash
# From Ethereum mainnet
python -c "
from src.fetchers.etherscan_fetcher import EtherscanFetcher
from src.audit_agent import AuditAgent

# Fetch contract
fetcher = EtherscanFetcher()
contract = fetcher.fetch_contract(
    address='0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',  # Uniswap V2 Router
    chain='ethereum',
    save_to='UniswapV2Router.sol'
)

# Audit it
agent = AuditAgent()
results = agent.audit_contract('UniswapV2Router.sol', 'reports/uniswap')
"
```

### Batch Audit Multiple Contracts

```bash
# Audit all contracts in a directory
python -m src.audit_agent --directory contracts/ --output reports/batch_audit
```

### Economic Analysis

```bash
# Audit with economic vulnerability detection
python -c "
from src.audit_agent import AuditAgent
from src.economic.dex_price_fetcher import DEXPriceFetcher
from src.economic.price_comparator import PriceComparator

# Audit contract
agent = AuditAgent()
results = agent.audit_contract('path/to/Contract.sol')

# Check for economic issues
fetcher = DEXPriceFetcher(chain='bsc')
token_address = '0x...'  # Token address
prices = fetcher.get_token_price_in_usd(token_address)

comparator = PriceComparator()
contract_code = open('path/to/Contract.sol').read()
analysis = comparator.analyze_contract_for_economic_exploits(
    contract_code,
    token_address,
    prices
)

print(f'Economic vulnerabilities: {analysis[\"has_economic_vulnerabilities\"]}')
print(f'Profit potential: ${analysis[\"total_profit_potential_usd\"]}')
"
```

---

## 3.4 Common Workflows

### Workflow 1: Pre-Deployment Audit

**Goal**: Audit before deploying to mainnet

```bash
# 1. Audit the contract
python -m src.audit_agent MyContract.sol --output reports/pre_deploy

# 2. Review the report
cat reports/pre_deploy/audit_report.md

# 3. Fix critical and high severity issues

# 4. Re-audit after fixes
python -m src.audit_agent MyContract_fixed.sol --output reports/post_fix

# 5. Compare results
diff reports/pre_deploy/audit_report.json reports/post_fix/audit_report.json
```

### Workflow 2: Research on Deployed Contracts

**Goal**: Analyze real contracts for research

```bash
# 1. Create a list of contract addresses
cat > contracts_to_audit.txt << EOF
0x10ED43C718714eb63d5aA57B78B54704E256024E  # PancakeSwap Router
0x13f4EA83D0bd40E75C8222255bc855a974568Dd4  # PancakeSwap Factory
0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D  # Uniswap V2 Router
EOF

# 2. Fetch and audit each contract
python scripts/evaluate.py \
    --contracts contracts_to_audit.txt \
    --chain bsc \
    --output evaluation_results

# 3. Analyze results
python -c "
import json
with open('evaluation_results/metrics.json') as f:
    metrics = json.load(f)
    print(f'Total audited: {metrics[\"total_contracts\"]}')
    print(f'Vulnerabilities found: {metrics[\"total_vulnerabilities\"]}')
    print(f'Economic exploits: {metrics[\"economic_exploits\"]}')
"
```

### Workflow 3: Generate and Test Exploit

**Goal**: Create a working exploit PoC

```bash
python << 'EOF'
from src.audit_agent import AuditAgent
from src.exploiter.exploit_generator import ExploitGenerator
from src.sandbox.chain_forker import ChainForker
from src.sandbox.exploit_runner import ExploitRunner
from src.sandbox.profit_calculator import ProfitCalculator

# 1. Audit to find vulnerability
agent = AuditAgent()
results = agent.audit_contract('VulnerableContract.sol')

# Get first critical vulnerability
vuln = next(v for v in results['vulnerabilities'] if v['severity'] == 'critical')

# 2. Generate exploit
generator = ExploitGenerator(llm_client=agent.ai_analyzer.llm_client)
exploit = generator.generate_exploit(
    vulnerability=vuln,
    contract_code=open('VulnerableContract.sol').read(),
    chain='bsc'
)

print(f"✅ Exploit generated: {exploit['method']}")

# 3. Save exploit
generator.save_exploit(
    exploit['exploit_code'],
    'exploits/reentrancy_exploit.sol',
    metadata={'vulnerability': vuln['type']}
)

# 4. Fork blockchain
forker = ChainForker(chain='bsc')
fork = forker.fork_at_block()

print(f"✅ Forked BSC at: {fork['fork_url']}")

# 5. Run exploit in sandbox
runner = ExploitRunner()
runner.compile_exploit(exploit['exploit_code'])
test_results = runner.run_exploit(
    contract_name='FlawVerifier',
    fork_url=fork['fork_url'],
    target_address='0x...'  # Vulnerable contract address
)

# 6. Calculate profit
calculator = ProfitCalculator(chain='bsc')
profit = calculator.calculate_from_test_results(test_results)

print(f"\n🎯 Exploit Results:")
print(f"Success: {test_results['success']}")
print(f"Profit: {profit['profit_native']:.4f} BNB")
print(f"Profit: ${profit['profit_usd']:,.2f} USD")
print(f"ROI: {profit['roi_percent']:.2f}%")

# Cleanup
forker.stop_fork()
EOF
```

### Workflow 4: Fine-Tune for Your Domain

**Goal**: Specialize LLM for your specific contracts

```bash
# 1. Collect training data
python scripts/create_training_data.py \
    --contracts contracts/ \
    --output data/training_data.json

# 2. Fine-tune with LoRA
python scripts/finetune_lora.py \
    --base_model qwen2.5-coder:32b-instruct \
    --dataset data/training_data.json \
    --output models/qwen-defi-lora \
    --epochs 3

# 3. Test fine-tuned model
python -c "
from src.llm.ollama_client import OllamaClient

client = OllamaClient(config={'model': 'qwen-defi-lora'})
response = client.analyze_vulnerability(
    contract_code=open('TestContract.sol').read(),
    slither_findings=[],
    context='DeFi yield farming contract'
)

print(response['content'])
"
```

---

## Quick Reference Card

```bash
# ESSENTIAL COMMANDS

# Activate environment
source venv/bin/activate && ollama serve &

# Audit a file
python -m src.audit_agent <contract.sol>

# Audit from blockchain
python examples/audit_onchain_contract.py

# Run tests
python examples/basic_usage.py

# View reports
cat reports/*/audit_report.md

# Check GPU
nvidia-smi

# Stop Ollama
pkill ollama
```

---

## Next Steps

Now that you can run basic audits, dive deeper:

1. **[Chapter 4: Architecture →](04-architecture.md)** - Understand how AuditAgent works
2. **[Chapter 6: Economic Analysis →](06-economic-analysis.md)** - Learn about novel economic detection
3. **[Chapter 11: Tutorials →](11-tutorials.md)** - Step-by-step detailed examples
4. **[Chapter 15: API Reference →](../api/python-api.md)** - Full API documentation

---

## Troubleshooting Quick Fixes

**Issue**: "Ollama connection refused"
**Fix**: `ollama serve &`

**Issue**: "CUDA out of memory"
**Fix**: `pkill ollama && ollama serve &`

**Issue**: "Module not found"
**Fix**: `source venv/bin/activate`

**Issue**: "Slither not found"
**Fix**: `pip install slither-analyzer`

---

[← Previous: Installation](02-installation.md) | [Home](../README.md) | [Next: Architecture →](04-architecture.md)
