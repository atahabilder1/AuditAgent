# Where AuditAgent Gets Smart Contracts

**Quick Answer:** AuditAgent gets contracts from **two sources**:

1. **Local files** (on your computer) ← Most common
2. **Blockchain** (downloads from Etherscan/BSCscan/etc.)

---

## 📂 Source 1: Local Files (Your Computer)

### How It Works
You have a `.sol` file → You tell AuditAgent where it is

### Example Files Already Available

```bash
ls tests/contracts/
```

Output:
```
VulnerableBank.sol       ← Intentionally vulnerable (for testing)
SecureBank.sol           ← Secure version (best practices)
ReentrancyAttack.sol     ← Attack contract example
```

### Usage: Analyze Local File

```python
from src.audit_agent import AuditAgent

agent = AuditAgent()
results = agent.audit_contract(
    contract_path="tests/contracts/VulnerableBank.sol",  # ← Local file
    output_dir="reports"
)

print(f"Found {results['summary']['total_vulnerabilities']} vulnerabilities")
```

Or command line:
```bash
cd /data/AuditAgent
source venv/bin/activate
python examples/basic_usage.py
```

### Your Own Contracts

```python
# Analyze YOUR contract file
agent.audit_contract(
    contract_path="/home/you/projects/MyToken.sol",  # ← Your file
    output_dir="reports"
)
```

### When to Use Local Files:
- ✅ You're developing a new contract
- ✅ You downloaded someone's code
- ✅ You have contracts in your project
- ✅ You're doing research with a dataset
- ✅ **This is the most common use case**

---

## 🌐 Source 2: Blockchain (Fetch On-Chain)

### How It Works
Contract is deployed → You provide address → AuditAgent downloads source code

### Requirements
1. Contract must be **verified** on blockchain explorer
2. You need an **Etherscan API key** (free)

### Get Free API Key

1. Go to: https://etherscan.io/myapikey
2. Sign up (free)
3. Create API key
4. Set environment variable:
   ```bash
   export ETHERSCAN_API_KEY="your-key-here"
   ```

### Example: Fetch & Audit Uniswap Router

```python
from src.fetchers.etherscan_fetcher import EtherscanFetcher
from src.audit_agent import AuditAgent

# Step 1: Fetch from Ethereum blockchain
fetcher = EtherscanFetcher()
contract = fetcher.fetch_contract(
    address="0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",  # Uniswap V2 Router
    chain="ethereum",
    save_to="UniswapRouter.sol"
)

print(f"Fetched: {contract['name']}")
print(f"Compiler: {contract['compiler']}")
print(f"License: {contract['license']}")

# Step 2: Audit the downloaded contract
agent = AuditAgent()
results = agent.audit_contract("UniswapRouter.sol", "reports")
```

### Supported Blockchains

AuditAgent can fetch from **11 blockchains**:

| Blockchain | Chain Name | Explorer |
|------------|------------|----------|
| Ethereum Mainnet | `ethereum` | etherscan.io |
| Ethereum Goerli | `goerli` | goerli.etherscan.io |
| Ethereum Sepolia | `sepolia` | sepolia.etherscan.io |
| Binance Smart Chain | `bsc` | bscscan.com |
| BSC Testnet | `bsc_testnet` | testnet.bscscan.com |
| Polygon | `polygon` | polygonscan.com |
| Polygon Mumbai | `polygon_mumbai` | mumbai.polygonscan.com |
| Arbitrum | `arbitrum` | arbiscan.io |
| Optimism | `optimism` | optimistic.etherscan.io |
| Avalanche | `avalanche` | snowtrace.io |
| Fantom | `fantom` | ftmscan.com |

### Example: Fetch from BSC

```python
fetcher = EtherscanFetcher()

# PancakeSwap Router on BSC
contract = fetcher.fetch_contract(
    address="0x10ED43C718714eb63d5aA57B78B54704E256024E",
    chain="bsc",  # ← Different chain
    save_to="PancakeRouter.sol"
)
```

### Command Line Example

```bash
cd /data/AuditAgent
source venv/bin/activate

# Set API key
export ETHERSCAN_API_KEY="your-key"

# Run the on-chain example
python examples/audit_onchain_contract.py
```

### What Gets Downloaded

When you fetch a contract, you get:

```python
{
    'address': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
    'chain': 'ethereum',
    'name': 'UniswapV2Router02',
    'compiler': 'v0.6.6+commit.6c089d02',
    'optimization': True,
    'runs': 999999,
    'source_code': '// SPDX-License-Identifier: GPL-3.0\npragma solidity...',
    'abi': '[{"inputs":[],"name":"WETH",...}]',
    'license': 'GPL-3.0',
    'is_multifile': False
}
```

The `source_code` is saved to a `.sol` file, then analyzed.

### When to Use On-Chain Fetching:
- ✅ Contract is already deployed
- ✅ You want to audit a live DeFi protocol
- ✅ Checking deployed contracts before interacting
- ✅ Research on deployed contracts
- ✅ Security due diligence

### Important Notes

⚠️ **Limitations:**
- Contract must be **verified** (source code published)
- Needs API key (free, but rate-limited)
- Multi-file contracts supported but complex
- Only works for contracts on supported chains

❌ **Won't work if:**
- Contract is not verified
- Contract is on unsupported chain
- API key is invalid/expired
- Network issues

---

## 🎯 Complete Workflow Diagram

### Local File Workflow
```
Your Contract File (.sol)
         ↓
    AuditAgent
         ↓
      Analysis
         ↓
       Report
```

### On-Chain Workflow
```
Deployed Contract Address (0x...)
         ↓
   EtherscanFetcher
         ↓
  Downloads Source Code
         ↓
   Saves as .sol file
         ↓
    AuditAgent
         ↓
      Analysis
         ↓
       Report
```

---

## 📝 Practical Examples

### Example 1: Analyze Your Development Contract

```bash
cd /data/AuditAgent
source venv/bin/activate

# Your contract is at: /home/you/myproject/Token.sol
python -c "
from src.audit_agent import AuditAgent
agent = AuditAgent()
results = agent.audit_contract('/home/you/myproject/Token.sol', 'reports')
print(f'Vulnerabilities: {results[\"summary\"][\"total_vulnerabilities\"]}')
"
```

### Example 2: Audit a Famous DeFi Contract

```bash
cd /data/AuditAgent
source venv/bin/activate
export ETHERSCAN_API_KEY="your-key"

# Fetch and audit Uniswap
python examples/audit_onchain_contract.py
```

### Example 3: Batch Audit All Contracts in Folder

```python
from src.audit_agent import AuditAgent
from pathlib import Path

agent = AuditAgent()

# Find all .sol files
contracts = Path("my_contracts/").glob("*.sol")

for contract in contracts:
    print(f"\nAuditing {contract.name}...")
    results = agent.audit_contract(str(contract), "reports")
    print(f"  Found {results['summary']['total_vulnerabilities']} issues")
```

### Example 4: Fetch Multiple On-Chain Contracts

```python
from src.fetchers.etherscan_fetcher import EtherscanFetcher

fetcher = EtherscanFetcher()

addresses = [
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",  # Uniswap Router
    "0x10ED43C718714eb63d5aA57B78B54704E256024E",  # PancakeSwap Router
]

contracts = fetcher.fetch_multiple_contracts(
    addresses=addresses,
    chain='ethereum',
    save_dir='fetched_contracts'
)

# Now audit them
from src.audit_agent import AuditAgent
agent = AuditAgent()

for contract in contracts:
    if 'error' not in contract:
        file_path = f"fetched_contracts/{contract['name']}.sol"
        results = agent.audit_contract(file_path, 'reports')
```

---

## 🔍 How to Check If Contract is Verified

Before fetching, check if contract is verified:

```python
from src.fetchers.etherscan_fetcher import EtherscanFetcher

fetcher = EtherscanFetcher()

# Check contract info
info = fetcher.get_contract_info(
    address="0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    chain="ethereum"
)

print(f"Name: {info['name']}")
print(f"Verified: {info['is_verified']}")
print(f"Compiler: {info['compiler']}")
```

Or visit the explorer directly:
- Ethereum: https://etherscan.io/address/0x...
- BSC: https://bscscan.com/address/0x...
- Look for green checkmark ✓ next to contract

---

## 💡 Best Practices

### For Local Files:
1. ✅ Keep contracts in organized folders
2. ✅ Use version control (git)
3. ✅ Test on sample contracts first
4. ✅ Save reports with meaningful names

### For On-Chain:
1. ✅ Get free Etherscan API key
2. ✅ Verify contract is verified before fetching
3. ✅ Save fetched contracts for reuse
4. ✅ Respect API rate limits (5 req/sec free tier)
5. ✅ Handle multi-file contracts carefully

---

## ❓ FAQ

### Q: Can I audit a contract without the source code?
**A:** No. AuditAgent analyzes source code. Bytecode-only analysis is not supported.

### Q: What if the contract is not verified on Etherscan?
**A:** You need to get the source code another way (from developers, GitHub, etc.) and save it locally.

### Q: Can I fetch from testnets?
**A:** Yes! Supported testnets: Goerli, Sepolia, BSC Testnet, Polygon Mumbai

### Q: Is there a size limit?
**A:** No hard limit, but very large contracts (>10,000 lines) may be slow to analyze.

### Q: Can I audit Vyper contracts?
**A:** Currently only Solidity (.sol) is supported. Vyper support is planned.

### Q: Do I need to compile contracts first?
**A:** No! AuditAgent handles compilation automatically using solc.

---

## 🚀 Quick Start

### Analyze Test Contract (Local)
```bash
cd /data/AuditAgent
source venv/bin/activate
python examples/basic_usage.py
```

### Analyze Your Contract (Local)
```python
from src.audit_agent import AuditAgent
agent = AuditAgent()
agent.audit_contract("path/to/YourContract.sol", "reports")
```

### Fetch & Analyze On-Chain
```bash
export ETHERSCAN_API_KEY="your-key"
python examples/audit_onchain_contract.py
```

---

## 📚 Summary

**Two sources:**

1. **Local Files** 📂
   - Most common
   - You provide the file path
   - Works offline
   - No API key needed

2. **Blockchain** 🌐
   - For deployed contracts
   - Downloads from explorer
   - Needs API key
   - Contract must be verified

**Both methods** → Same analysis → Same quality reports!

---

**Questions?** See [README_COMPLETE.md](README_COMPLETE.md) for full documentation.
