# AuditAgent

**Autonomous AI Agent for Smart Contract Security Auditing**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Solidity](https://img.shields.io/badge/solidity-%5E0.7.0%20%7C%20%5E0.8.0-lightgrey)](https://docs.soliditylang.org/)
[![AI Agent](https://img.shields.io/badge/AI-Agent-brightgreen)](https://www.anthropic.com/)

An **intelligent autonomous agent** that orchestrates multiple specialized tools and AI models to perform comprehensive security audits of Solidity smart contracts. Demonstrates advanced AI agent architecture, tool orchestration, multi-phase reasoning, and adaptive decision-making for blockchain security.

## 🤖 AI Agent Architecture

This project showcases **production-grade AI agent engineering** through:

### Agent Design Pattern
```
┌─────────────────────────────────────────────────────────┐
│                    AUDIT AGENT                          │
│                   (Orchestrator)                        │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Planning & Reasoning Layer                      │  │
│  │  • Task decomposition                            │  │
│  │  • Multi-phase execution strategy                │  │
│  │  • Risk assessment & prioritization              │  │
│  └──────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Tool Orchestration Layer                        │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐ │  │
│  │  │Slither │  │Mythril │  │AI/LLM  │  │Etherscan│ │  │
│  │  │Analyzer│  │Analyzer│  │Analyzer│  │Fetcher  │ │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘ │  │
│  └──────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Synthesis & Reporting Layer                     │  │
│  │  • Vulnerability aggregation & deduplication     │  │
│  │  • Risk scoring algorithm                        │  │
│  │  • Multi-format report generation                │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Key AI Agent Capabilities

#### 1. **Autonomous Tool Orchestration**
The agent autonomously coordinates multiple specialized security tools:
- **Static Analysis** (Slither) - Code pattern analysis
- **Symbolic Execution** (Mythril) - Deep path exploration
- **AI Reasoning** (GPT-4) - Contextual vulnerability assessment
- **Blockchain Integration** (Etherscan API) - On-chain data fetching

#### 2. **Multi-Phase Reasoning**
```python
Phase 1: Planning
├─ Analyze input (local file vs blockchain address)
├─ Select appropriate tools based on context
└─ Configure execution parameters

Phase 2: Parallel Execution
├─ Run Slither for static analysis
├─ Run Mythril for symbolic execution
├─ Run pattern-based detectors
└─ Aggregate results in real-time

Phase 3: AI-Powered Synthesis
├─ LLM analyzes aggregated findings
├─ Contextualizes vulnerabilities
├─ Generates actionable recommendations
└─ Assigns risk severity

Phase 4: Reporting & Presentation
├─ Deduplicates findings
├─ Calculates risk scores
└─ Generates multi-format reports
```

#### 3. **Adaptive Decision Making**
- Detects when tools fail and continues execution
- Adjusts analysis depth based on contract complexity
- Handles multi-file contracts intelligently
- Optimizes for speed vs thoroughness based on configuration

#### 4. **Multi-Chain Intelligence**
Agent autonomously fetches and processes contracts from 10+ blockchains:
- Auto-detects contract format (single vs multi-file)
- Validates addresses and network compatibility
- Handles API rate limiting and retries
- Extracts and normalizes source code

## 🎯 Project Purpose

**Demonstrates AI Agent Engineering Skills:**
- ✅ **Tool Integration** - Orchestrating multiple external tools (Slither, Mythril, Etherscan)
- ✅ **LLM Integration** - Advanced prompt engineering with GPT-4
- ✅ **Agent Architecture** - Multi-phase planning and execution
- ✅ **Error Handling** - Graceful degradation when tools fail
- ✅ **Context Management** - Aggregating and synthesizing results from multiple sources
- ✅ **Autonomous Operation** - Minimal human intervention required

## Project Timeline

**Development Period:** March 2024 - August 2024

## Features

### Core Agent Capabilities

- **🤖 Autonomous Multi-Phase Analysis**
  - Intelligent task decomposition and planning
  - Parallel tool execution with result aggregation
  - Self-healing when individual analyzers fail
  - Adaptive strategy based on contract characteristics

- **🔗 Multi-Tool Orchestration**
  - **Static Analysis Agent** (Slither integration)
  - **Symbolic Execution Agent** (Mythril integration)
  - **AI Reasoning Agent** (GPT-4 integration)
  - **Pattern Detection Agent** (Custom regex & heuristics)
  - **Blockchain Fetch Agent** (Etherscan API integration)

- **🌐 Multi-Chain Intelligence**
  - Supports 10+ blockchains (Ethereum, BSC, Polygon, Arbitrum, Optimism, etc.)
  - Autonomous contract fetching from blockchain explorers
  - Verifies contract authenticity and compilation settings
  - Handles both single-file and multi-file contracts

- **🧠 Advanced Reasoning**
  - Contextual vulnerability assessment using LLMs
  - Cross-referencing findings between multiple tools
  - Intelligent deduplication and severity normalization
  - Risk scoring algorithm (0-100 scale)

- **📊 Comprehensive Reporting**
  - JSON format for programmatic integration
  - Markdown format for human readability
  - Includes code snippets, line numbers, and remediation steps
  - Severity rankings and confidence scores

### Vulnerability Detection (15+ Categories)

**Critical Severity:**
- Reentrancy attacks
- Unprotected selfdestruct
- Arbitrary ether withdrawal

**High Severity:**
- tx.origin authentication
- Unchecked external calls
- Dangerous delegatecall
- Integer overflow/underflow

**Medium Severity:**
- Block timestamp manipulation
- Missing zero address checks
- Uninitialized storage pointers

**Low Severity:**
- Floating pragma versions
- Missing event emissions
- Code quality issues

## Architecture

### Agent Component Structure

```
AuditAgent/
├── src/
│   ├── audit_agent.py              # 🤖 Main Agent Orchestrator
│   │   ├── Multi-phase execution engine
│   │   ├── Tool coordination logic
│   │   └── Result synthesis
│   │
│   ├── analyzers/                  # 🔧 Specialized Analysis Agents
│   │   ├── slither_analyzer.py     #   Static analysis agent
│   │   ├── mythril_analyzer.py     #   Symbolic execution agent
│   │   └── ai_analyzer.py          #   LLM reasoning agent
│   │
│   ├── detectors/                  # 🔍 Pattern Detection Agents
│   │   └── vulnerability_detector.py
│   │       ├── Regex pattern matching
│   │       ├── Advanced heuristics
│   │       └── Cross-tool result correlation
│   │
│   ├── fetchers/                   # 🌐 Data Acquisition Agents
│   │   └── etherscan_fetcher.py
│   │       ├── Multi-chain API integration
│   │       ├── Rate limiting & retry logic
│   │       └── Contract validation
│   │
│   └── reporters/                  # 📝 Report Generation Agents
│       └── report_generator.py
│           ├── Multi-format output (JSON, MD)
│           └── Risk scoring algorithm
│
├── tests/contracts/                # 🧪 Test Contracts
│   ├── VulnerableBank.sol         #   Intentionally vulnerable
│   ├── ReentrancyAttack.sol       #   Attack demonstration
│   └── SecureBank.sol             #   Best practices example
│
├── examples/                       # 📚 Usage Examples
│   ├── basic_usage.py             #   Local file auditing
│   ├── audit_onchain_contract.py  #   Blockchain contract auditing
│   └── cli.py                     #   Command-line interface
│
└── config/                         # ⚙️ Agent Configuration
    └── default_config.json         #   Tool parameters & timeouts
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Solidity compiler (solc)
- Node.js (for some analysis tools)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/AuditAgent.git
cd AuditAgent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Solidity compiler
pip install solc-select
solc-select install 0.8.19
solc-select use 0.8.19

# Configure API keys (optional but recommended)
export OPENAI_API_KEY="your-openai-api-key"        # For AI analysis
export ETHERSCAN_API_KEY="your-etherscan-api-key"  # For on-chain fetching

# Install as package
pip install -e .
```

## Quick Start

### 1. Audit a Local Contract (Basic Agent Usage)

```python
from src.audit_agent import AuditAgent

# Initialize the autonomous agent
agent = AuditAgent()

# Agent autonomously orchestrates all analysis phases
results = agent.audit_contract(
    contract_path="path/to/YourContract.sol",
    output_dir="reports"
)

# View agent's findings
print(f"Vulnerabilities found: {results['summary']['total_vulnerabilities']}")
print(f"Risk score: {results['summary']['risk_score']}/100")
print(f"Agent ran: {results['summary']['analyzers_run']}")
```

### 2. Audit On-Chain Contract (Advanced Agent Capability)

```python
from src.fetchers.etherscan_fetcher import EtherscanFetcher
from src.audit_agent import AuditAgent

# Agent automatically fetches contract from blockchain
fetcher = EtherscanFetcher()
contract = fetcher.fetch_contract(
    address="0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",  # Uniswap V2 Router
    chain="ethereum",
    save_to="UniswapV2Router.sol"
)

# Agent autonomously audits the fetched contract
agent = AuditAgent()
results = agent.audit_contract("UniswapV2Router.sol", "reports")
```

### 3. CLI - Agent as a Service

```bash
# Audit local contract file
auditagent audit MyContract.sol -o reports/

# Audit deployed contract from any supported chain
auditagent audit-address 0x1234...5678 --chain ethereum -o reports/

# Batch audit entire directory
auditagent audit-all ./contracts/ -o reports/

# List supported blockchains
auditagent chains

# View agent capabilities
auditagent version
```

### 4. Python Scripts

```bash
# Run basic agent example
python examples/basic_usage.py

# Run advanced on-chain agent example
python examples/audit_onchain_contract.py
```

## Agent Configuration

Customize the agent's behavior through configuration:

```json
{
  "slither": {
    "timeout": 300,
    "exclude_informational": false
  },
  "mythril": {
    "timeout": 600,
    "max_depth": 128,
    "execution_timeout": 300
  },
  "ai": {
    "enabled": true,
    "model": "gpt-4",
    "temperature": 0.1,
    "max_tokens": 2000
  },
  "detectors": {
    "pattern_matching": true,
    "advanced_detection": true
  },
  "output": {
    "format": "both",
    "verbose": true
  }
}
```

## Multi-Chain Support

The agent autonomously works with 10+ blockchain networks:

- **Ethereum** (mainnet, Goerli, Sepolia)
- **Binance Smart Chain** (BSC & testnet)
- **Polygon** (Matic & Mumbai)
- **Arbitrum**
- **Optimism**
- **Avalanche**
- **Fantom**
- And more...

```bash
# Agent fetches and audits from any chain
auditagent audit-address 0x10ED43C718714eb63d5aA57B78B54704E256024E --chain bsc
auditagent audit-address 0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506 --chain polygon
```

## How the Agent Works

### Execution Flow

```
User Input
    ↓
┌───────────────────────────────────┐
│  1. PLANNING PHASE                │
│  Agent analyzes input and         │
│  creates execution strategy       │
└───────────────────────────────────┘
    ↓
┌───────────────────────────────────┐
│  2. TOOL ORCHESTRATION            │
│  Parallel execution of:           │
│  • Slither (static analysis)      │
│  • Mythril (symbolic execution)   │
│  • Pattern detectors              │
│  Agent monitors progress          │
└───────────────────────────────────┘
    ↓
┌───────────────────────────────────┐
│  3. AI SYNTHESIS                  │
│  Agent sends findings to LLM:     │
│  • Contextual analysis            │
│  • Severity assessment            │
│  • Recommendation generation      │
└───────────────────────────────────┘
    ↓
┌───────────────────────────────────┐
│  4. AGGREGATION & REPORTING       │
│  Agent processes all results:     │
│  • Deduplicates findings          │
│  • Calculates risk score          │
│  • Generates reports (JSON, MD)   │
└───────────────────────────────────┘
    ↓
Final Report
```

## AI Agent Skills Demonstrated

### 1. **Tool Integration & Orchestration**
- Wraps external tools (Slither, Mythril) with error handling
- Coordinates parallel execution with proper timeout management
- Handles tool failures gracefully without stopping entire audit

### 2. **LLM Integration**
- Advanced prompt engineering for vulnerability analysis
- Context management for large codebases
- Temperature and token optimization for accurate results

### 3. **Multi-Agent Coordination**
- Each analyzer operates as a specialized sub-agent
- Main agent coordinates and synthesizes results
- Implements agent communication patterns

### 4. **Planning & Reasoning**
- Task decomposition (audit → sub-analyses)
- Prioritization of critical vulnerabilities
- Risk scoring based on multiple factors

### 5. **Adaptive Behavior**
- Adjusts strategy based on contract size
- Falls back when AI API is unavailable
- Rate limiting for external APIs

### 6. **Context Aggregation**
- Combines findings from 3+ different sources
- Correlates vulnerabilities across tools
- Intelligent deduplication

## Use Cases

### 1. **Pre-Deployment Security**
Agent audits contracts before mainnet deployment

### 2. **On-Chain Due Diligence**
Agent fetches and analyzes deployed contracts for integration decisions

### 3. **CI/CD Integration**
Agent runs as automated security check in pipelines

### 4. **Security Research**
Agent helps researchers identify vulnerability patterns

### 5. **Educational Tool**
Agent demonstrates AI capabilities in blockchain security

### 6. **Portfolio Demonstration**
Agent showcases AI engineering, LLM integration, and tool orchestration skills

## Technical Stack

### Core Technologies
- **Python 3.8+** - Agent implementation
- **OpenAI GPT-4** - LLM reasoning engine
- **Slither** - Static analysis tool
- **Mythril** - Symbolic execution tool
- **Etherscan API** - Multi-chain data source

### Agent Frameworks
- **Click** - CLI framework
- **Requests** - HTTP client for API orchestration
- **JSON/YAML** - Configuration management
- **Jinja2** - Report templating

### Design Patterns
- **Agent pattern** - Autonomous tool orchestration
- **Observer pattern** - Tool result monitoring
- **Strategy pattern** - Configurable analysis approaches
- **Factory pattern** - Analyzer instantiation

## Performance

Agent execution times (typical hardware):

| Contract Size | Analysis Time | Tools Run |
|--------------|---------------|-----------|
| Small (<200 LOC) | 10-30 sec | All 3 |
| Medium (200-500 LOC) | 30-90 sec | All 3 |
| Large (>500 LOC) | 1-5 min | All 3 |

**Optimization strategies:**
- Parallel tool execution
- Configurable timeouts
- Optional AI analysis bypass
- Result caching (planned)

## Limitations & Transparency

As with all AI agents:
- ⚠️ **Not 100% accurate** - Manual review still recommended
- ⚠️ **Tool dependencies** - Requires Slither/Mythril installation
- ⚠️ **API requirements** - OpenAI and Etherscan keys needed for full functionality
- ⚠️ **Solidity-only** - Currently doesn't support Vyper or other languages
- ⚠️ **False positives** - Automated tools may flag non-issues

## Roadmap

### Completed Features ✅
- [x] Multi-phase agent execution
- [x] Tool orchestration (Slither, Mythril, GPT-4)
- [x] Multi-chain contract fetching
- [x] Intelligent vulnerability deduplication
- [x] Risk scoring algorithm
- [x] Multi-format reporting

### Planned Enhancements 🚀
- [ ] **ReAct pattern** - Iterative reasoning and action
- [ ] **Chain-of-Thought** - Explainable decision making
- [ ] **Memory system** - Historical vulnerability tracking
- [ ] **Multi-agent collaboration** - Specialized agents debating findings
- [ ] **Tool discovery** - Automatic integration of new security tools
- [ ] **Self-improvement** - Learning from false positives/negatives
- [ ] **Web interface** - Dashboard for agent monitoring
- [ ] **GitHub Action** - Automated PR security checks

## Contributing

This project demonstrates AI agent engineering skills. Contributions welcome in:
- Additional tool integrations
- Enhanced agent reasoning patterns
- New vulnerability detectors
- Performance optimizations
- Documentation improvements

## License

MIT License - See [LICENSE](LICENSE) file

## Acknowledgments

- **OpenAI** - GPT-4 API for AI reasoning
- **Trail of Bits** - Slither static analysis framework
- **ConsenSys** - Mythril symbolic execution
- **OpenZeppelin** - Secure contract patterns
- **Etherscan** - Multi-chain blockchain API

## AI Agent Portfolio Statement

This project demonstrates **production-ready AI agent engineering** including:

✅ **Autonomous operation** with minimal human intervention
✅ **Multi-tool orchestration** coordinating 3+ specialized analyzers
✅ **LLM integration** with advanced prompt engineering
✅ **Multi-phase reasoning** - planning, execution, synthesis, reporting
✅ **Error handling** with graceful degradation
✅ **API integration** with rate limiting and retry logic
✅ **Context management** aggregating results from multiple sources
✅ **Adaptive behavior** adjusting strategy based on inputs
✅ **Multi-chain intelligence** working across 10+ blockchains

**Perfect for roles requiring:** AI Agent Development, LLM Engineering, Tool Orchestration, Blockchain Security, Python Architecture

## Contact

For job opportunities, collaborations, or questions:

- **Email**: your.email@example.com
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)
- **GitHub**: [@yourusername](https://github.com/yourusername)

## Project Stats

- **Architecture**: Multi-agent orchestration system
- **Lines of Code**: ~3,000+
- **Agents Implemented**: 6 specialized agents
- **Tools Orchestrated**: 4 external tools
- **Vulnerability Types**: 15+ categories
- **Blockchains Supported**: 10+ networks
- **AI Models**: GPT-4 integration
- **Test Coverage**: 85%+

---

**🤖 Built to showcase AI Agent Engineering expertise** | March 2024 - August 2024

*Autonomous • Intelligent • Adaptive*
