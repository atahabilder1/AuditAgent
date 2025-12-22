# AuditAgent v2.0 - Complete Documentation

**The Definitive Guide to AI-Powered Smart Contract Security Analysis**

---

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![GPU](https://img.shields.io/badge/GPU-NVIDIA%20Required-red.svg)

*A comprehensive research-grade system for detecting economic vulnerabilities in smart contracts using local AI models*

**Author**: Anik, PhD Student
**Institution**: Wayne State University
**Last Updated**: December 2024
**Documentation Version**: 1.0

</div>

---

## 📚 Table of Contents

### [Preface](#preface)
- [About This Documentation](#about-this-documentation)
- [Who Should Read This](#who-should-read-this)
- [How to Use This Guide](#how-to-use-this-guide)
- [Conventions Used](#conventions-used)

### Part I: Getting Started

#### [Chapter 1: Introduction](chapters/01-introduction.md)
- 1.1 [What is AuditAgent v2.0?](chapters/01-introduction.md#11-what-is-auditagent-v20)
- 1.2 [Research Motivation](chapters/01-introduction.md#12-research-motivation)
- 1.3 [Novel Contributions](chapters/01-introduction.md#13-novel-contributions)
- 1.4 [Comparison with Existing Tools](chapters/01-introduction.md#14-comparison-with-existing-tools)
- 1.5 [Key Features](chapters/01-introduction.md#15-key-features)
- 1.6 [System Requirements](chapters/01-introduction.md#16-system-requirements)

#### [Chapter 2: Installation & Setup](chapters/02-installation.md)
- 2.1 [Hardware Requirements](chapters/02-installation.md#21-hardware-requirements)
- 2.2 [Software Prerequisites](chapters/02-installation.md#22-software-prerequisites)
- 2.3 [Step-by-Step Installation](chapters/02-installation.md#23-step-by-step-installation)
  - 2.3.1 [Automated Setup (Recommended)](chapters/02-installation.md#231-automated-setup)
  - 2.3.2 [Manual Installation](chapters/02-installation.md#232-manual-installation)
- 2.4 [Verification & Testing](chapters/02-installation.md#24-verification-testing)
- 2.5 [Troubleshooting](chapters/02-installation.md#25-troubleshooting)
- 2.6 [Docker Installation](chapters/02-installation.md#26-docker-installation)

#### [Chapter 3: Quick Start Guide](chapters/03-quickstart.md)
- 3.1 [Your First Audit](chapters/03-quickstart.md#31-your-first-audit)
- 3.2 [Understanding the Output](chapters/03-quickstart.md#32-understanding-the-output)
- 3.3 [Basic Commands](chapters/03-quickstart.md#33-basic-commands)
- 3.4 [Common Workflows](chapters/03-quickstart.md#34-common-workflows)

### Part II: Architecture & Design

#### [Chapter 4: System Architecture](chapters/04-architecture.md)
- 4.1 [High-Level Overview](chapters/04-architecture.md#41-high-level-overview)
- 4.2 [Module Breakdown](chapters/04-architecture.md#42-module-breakdown)
  - 4.2.1 [LLM Integration Module](chapters/04-architecture.md#421-llm-integration)
  - 4.2.2 [Economic Analysis Module](chapters/04-architecture.md#422-economic-analysis)
  - 4.2.3 [Exploit Generation Module](chapters/04-architecture.md#423-exploit-generation)
  - 4.2.4 [Sandbox Validation Module](chapters/04-architecture.md#424-sandbox-validation)
- 4.3 [Data Flow](chapters/04-architecture.md#43-data-flow)
- 4.4 [Design Patterns](chapters/04-architecture.md#44-design-patterns)
- 4.5 [Technology Stack](chapters/04-architecture.md#45-technology-stack)

#### [Chapter 5: LLM Integration](chapters/05-llm-integration.md)
- 5.1 [Why Local LLM?](chapters/05-llm-integration.md#51-why-local-llm)
- 5.2 [Ollama Architecture](chapters/05-llm-integration.md#52-ollama-architecture)
- 5.3 [Qwen2.5-Coder-32B Model](chapters/05-llm-integration.md#53-qwen-model)
- 5.4 [Prompt Engineering](chapters/05-llm-integration.md#54-prompt-engineering)
  - 5.4.1 [Vulnerability Analysis Prompts](chapters/05-llm-integration.md#541-vulnerability-prompts)
  - 5.4.2 [Exploit Generation Prompts](chapters/05-llm-integration.md#542-exploit-prompts)
  - 5.4.3 [Economic Analysis Prompts](chapters/05-llm-integration.md#543-economic-prompts)
- 5.5 [Response Parsing](chapters/05-llm-integration.md#55-response-parsing)
- 5.6 [Performance Optimization](chapters/05-llm-integration.md#56-performance-optimization)

#### [Chapter 6: Economic Vulnerability Detection](chapters/06-economic-analysis.md)
- 6.1 [Introduction to Economic Exploits](chapters/06-economic-analysis.md#61-introduction)
- 6.2 [Price Fetching from DEXes](chapters/06-economic-analysis.md#62-price-fetching)
  - 6.2.1 [PancakeSwap Integration](chapters/06-economic-analysis.md#621-pancakeswap)
  - 6.2.2 [Uniswap Integration](chapters/06-economic-analysis.md#622-uniswap)
  - 6.2.3 [Web3 Implementation](chapters/06-economic-analysis.md#623-web3)
- 6.3 [Price Comparison Algorithm](chapters/06-economic-analysis.md#63-price-comparison)
- 6.4 [Arbitrage Detection](chapters/06-economic-analysis.md#64-arbitrage-detection)
  - 6.4.1 [Simple Arbitrage](chapters/06-economic-analysis.md#641-simple-arbitrage)
  - 6.4.2 [Triangular Arbitrage](chapters/06-economic-analysis.md#642-triangular-arbitrage)
  - 6.4.3 [Flash Loan Arbitrage](chapters/06-economic-analysis.md#643-flash-loan)
- 6.5 [Real-World Examples](chapters/06-economic-analysis.md#65-examples)

#### [Chapter 7: Exploit Generation](chapters/07-exploit-generation.md)
- 7.1 [Exploit Generation Pipeline](chapters/07-exploit-generation.md#71-pipeline)
- 7.2 [Template-Based Generation](chapters/07-exploit-generation.md#72-templates)
- 7.3 [LLM-Based Generation](chapters/07-exploit-generation.md#73-llm-generation)
- 7.4 [Exploit Templates Deep Dive](chapters/07-exploit-generation.md#74-templates-deepdive)
  - 7.4.1 [Reentrancy Exploits](chapters/07-exploit-generation.md#741-reentrancy)
  - 7.4.2 [Flash Loan Exploits](chapters/07-exploit-generation.md#742-flash-loan)
  - 7.4.3 [Price Manipulation](chapters/07-exploit-generation.md#743-price-manipulation)
  - 7.4.4 [Access Control](chapters/07-exploit-generation.md#744-access-control)
- 7.5 [Code Quality & Safety](chapters/07-exploit-generation.md#75-safety)

#### [Chapter 8: Sandbox Validation](chapters/08-sandbox.md)
- 8.1 [Why Sandbox Testing?](chapters/08-sandbox.md#81-why-sandbox)
- 8.2 [Foundry Framework](chapters/08-sandbox.md#82-foundry)
  - 8.2.1 [Forge - Smart Contract Testing](chapters/08-sandbox.md#821-forge)
  - 8.2.2 [Anvil - Local Blockchain](chapters/08-sandbox.md#822-anvil)
  - 8.2.3 [Cast - Ethereum CLI](chapters/08-sandbox.md#823-cast)
- 8.3 [Blockchain Forking](chapters/08-sandbox.md#83-forking)
- 8.4 [Exploit Execution](chapters/08-sandbox.md#84-execution)
- 8.5 [Profit Calculation](chapters/08-sandbox.md#85-profit)
- 8.6 [Safety Considerations](chapters/08-sandbox.md#86-safety)

### Part III: Usage & Examples

#### [Chapter 9: Basic Usage](chapters/09-basic-usage.md)
- 9.1 [Auditing a Local Contract](chapters/09-basic-usage.md#91-local-contract)
- 9.2 [Auditing On-Chain Contracts](chapters/09-basic-usage.md#92-onchain)
- 9.3 [Batch Auditing](chapters/09-basic-usage.md#93-batch)
- 9.4 [Configuration Options](chapters/09-basic-usage.md#94-configuration)
- 9.5 [Output Formats](chapters/09-basic-usage.md#95-output)

#### [Chapter 10: Advanced Usage](chapters/10-advanced-usage.md)
- 10.1 [Custom Economic Analysis](chapters/10-advanced-usage.md#101-custom-economic)
- 10.2 [Fine-Tuning the LLM](chapters/10-advanced-usage.md#102-finetuning)
- 10.3 [Creating Custom Exploit Templates](chapters/10-advanced-usage.md#103-custom-templates)
- 10.4 [Integration with CI/CD](chapters/10-advanced-usage.md#104-cicd)
- 10.5 [API Integration](chapters/10-advanced-usage.md#105-api)

#### [Chapter 11: Tutorials](chapters/11-tutorials.md)
- 11.1 [Tutorial 1: Detecting a Reentrancy Vulnerability](chapters/11-tutorials.md#111-reentrancy)
- 11.2 [Tutorial 2: Finding Economic Exploits](chapters/11-tutorials.md#112-economic)
- 11.3 [Tutorial 3: Generating and Testing Exploits](chapters/11-tutorials.md#113-exploits)
- 11.4 [Tutorial 4: Running Full Research Pipeline](chapters/11-tutorials.md#114-research)

### Part IV: Research & Methodology

#### [Chapter 12: Research Methodology](chapters/12-research.md)
- 12.1 [Research Questions](chapters/12-research.md#121-questions)
- 12.2 [Experimental Design](chapters/12-research.md#122-design)
- 12.3 [Data Collection](chapters/12-research.md#123-data)
- 12.4 [Metrics & Evaluation](chapters/12-research.md#124-metrics)
- 12.5 [Statistical Analysis](chapters/12-research.md#125-statistics)

#### [Chapter 13: Evaluation Framework](chapters/13-evaluation.md)
- 13.1 [Detection Accuracy](chapters/13-evaluation.md#131-accuracy)
- 13.2 [False Positive Analysis](chapters/13-evaluation.md#132-false-positives)
- 13.3 [Economic Analysis Validation](chapters/13-evaluation.md#133-economic-validation)
- 13.4 [Exploit Generation Success Rate](chapters/13-evaluation.md#134-exploit-success)
- 13.5 [Performance Benchmarks](chapters/13-evaluation.md#135-performance)

#### [Chapter 14: Case Studies](chapters/14-case-studies.md)
- 14.1 [Case Study 1: Reentrancy in DeFi Protocol](chapters/14-case-studies.md#141-reentrancy-case)
- 14.2 [Case Study 2: Price Manipulation Exploit](chapters/14-case-studies.md#142-price-case)
- 14.3 [Case Study 3: Flash Loan Attack](chapters/14-case-studies.md#143-flashloan-case)
- 14.4 [Case Study 4: Real $4.6M Exploit Recreation](chapters/14-case-studies.md#144-anthropic-case)

### Part V: API Reference

#### [Chapter 15: Python API Reference](api/python-api.md)
- 15.1 [Core Modules](api/python-api.md#151-core)
- 15.2 [LLM Module API](api/python-api.md#152-llm)
- 15.3 [Economic Module API](api/python-api.md#153-economic)
- 15.4 [Exploiter Module API](api/python-api.md#154-exploiter)
- 15.5 [Sandbox Module API](api/python-api.md#155-sandbox)

#### [Chapter 16: CLI Reference](api/cli-reference.md)
- 16.1 [Command Overview](api/cli-reference.md#161-overview)
- 16.2 [Audit Commands](api/cli-reference.md#162-audit)
- 16.3 [Economic Analysis Commands](api/cli-reference.md#163-economic)
- 16.4 [Configuration Commands](api/cli-reference.md#164-config)

### Part VI: Deployment & Operations

#### [Chapter 17: Docker Deployment](chapters/17-docker.md)
- 17.1 [Docker Architecture](chapters/17-docker.md#171-architecture)
- 17.2 [Building Images](chapters/17-docker.md#172-building)
- 17.3 [Running Containers](chapters/17-docker.md#173-running)
- 17.4 [GPU Configuration](chapters/17-docker.md#174-gpu)
- 17.5 [Volume Management](chapters/17-docker.md#175-volumes)
- 17.6 [Production Deployment](chapters/17-docker.md#176-production)

#### [Chapter 18: Performance Tuning](chapters/18-performance.md)
- 18.1 [GPU Optimization](chapters/18-performance.md#181-gpu)
- 18.2 [LLM Inference Speed](chapters/18-performance.md#182-llm)
- 18.3 [Batch Processing](chapters/18-performance.md#183-batch)
- 18.4 [Caching Strategies](chapters/18-performance.md#184-caching)
- 18.5 [Memory Management](chapters/18-performance.md#185-memory)

### Part VII: Contributing & Extending

#### [Chapter 19: Contributing Guide](chapters/19-contributing.md)
- 19.1 [Code of Conduct](chapters/19-contributing.md#191-conduct)
- 19.2 [Development Setup](chapters/19-contributing.md#192-setup)
- 19.3 [Coding Standards](chapters/19-contributing.md#193-standards)
- 19.4 [Testing Guidelines](chapters/19-contributing.md#194-testing)
- 19.5 [Documentation Standards](chapters/19-contributing.md#195-docs)
- 19.6 [Pull Request Process](chapters/19-contributing.md#196-pr)

#### [Chapter 20: Extending AuditAgent](chapters/20-extending.md)
- 20.1 [Adding New Analyzers](chapters/20-extending.md#201-analyzers)
- 20.2 [Custom Vulnerability Detectors](chapters/20-extending.md#202-detectors)
- 20.3 [New Exploit Templates](chapters/20-extending.md#203-templates)
- 20.4 [Plugin System](chapters/20-extending.md#204-plugins)

### Part VIII: Appendices

#### [Appendix A: References & Citations](references/citations.md)
- A.1 [Academic Papers](references/citations.md#a1-papers)
- A.2 [Technical Documentation](references/citations.md#a2-docs)
- A.3 [Tools & Frameworks](references/citations.md#a3-tools)
- A.4 [Datasets](references/citations.md#a4-datasets)

#### [Appendix B: Glossary](references/glossary.md)
- B.1 [Smart Contract Terms](references/glossary.md#b1-smart-contracts)
- B.2 [DeFi Terms](references/glossary.md#b2-defi)
- B.3 [AI/ML Terms](references/glossary.md#b3-ai)
- B.4 [Security Terms](references/glossary.md#b4-security)

#### [Appendix C: Troubleshooting](references/troubleshooting.md)
- C.1 [Installation Issues](references/troubleshooting.md#c1-installation)
- C.2 [Runtime Errors](references/troubleshooting.md#c2-runtime)
- C.3 [GPU Issues](references/troubleshooting.md#c3-gpu)
- C.4 [Docker Issues](references/troubleshooting.md#c4-docker)
- C.5 [FAQ](references/troubleshooting.md#c5-faq)

#### [Appendix D: Change Log](references/changelog.md)
- D.1 [Version 2.0.0](references/changelog.md#d1-v200)
- D.2 [Version 1.0.0](references/changelog.md#d2-v100)

#### [Appendix E: License](references/license.md)

---

## Preface

### About This Documentation

This documentation is designed to be a complete, self-contained reference for AuditAgent v2.0. Whether you're a researcher, developer, security auditor, or student, this guide will take you from installation through advanced usage and research methodology.

### Who Should Read This

- **Researchers**: Working on smart contract security, AI in security, or DeFi
- **Developers**: Building security tools or integrating AuditAgent
- **Security Auditors**: Using AI to enhance manual audits
- **Students**: Learning about smart contract security and AI applications
- **PhD Candidates**: Looking for reproducible research systems

### How to Use This Guide

**If you're new to AuditAgent:**
1. Read Chapter 1 (Introduction)
2. Follow Chapter 2 (Installation)
3. Complete Chapter 3 (Quick Start)
4. Explore tutorials in Chapter 11

**If you're a researcher:**
1. Review Chapters 1, 4-8 for architecture
2. Study Chapter 12 (Research Methodology)
3. Follow Chapter 13 (Evaluation)
4. Examine Chapter 14 (Case Studies)

**If you're a developer:**
1. Read Chapters 4-8 for architecture
2. Study Chapter 15 (API Reference)
3. Review Chapter 20 (Extending)
4. Check Chapter 19 (Contributing)

### Conventions Used

Throughout this documentation:

- `Code blocks` - Commands, code, or file paths
- **Bold** - Important terms or emphasis
- *Italic* - File names, variables, or gentle emphasis
- 💡 **Tip** - Helpful suggestions
- ⚠️ **Warning** - Important cautions
- 📝 **Note** - Additional information
- ✅ **Success** - Indicates successful completion
- ❌ **Error** - Common error scenarios

### Documentation Versioning

This documentation follows semantic versioning:
- **Major version** (1.x.x) - Significant content reorganization
- **Minor version** (x.1.x) - New chapters or major updates
- **Patch version** (x.x.1) - Corrections and clarifications

**Current Version**: 1.0.0
**Last Updated**: December 22, 2024
**Applies to AuditAgent**: v2.0.0

---

## Quick Navigation

### 🚀 Getting Started
- [Installation Guide →](chapters/02-installation.md)
- [Quick Start →](chapters/03-quickstart.md)
- [First Tutorial →](chapters/11-tutorials.md#111-reentrancy)

### 📖 Core Concepts
- [System Architecture →](chapters/04-architecture.md)
- [Economic Analysis →](chapters/06-economic-analysis.md)
- [LLM Integration →](chapters/05-llm-integration.md)

### 🔬 Research
- [Research Methodology →](chapters/12-research.md)
- [Evaluation Framework →](chapters/13-evaluation.md)
- [Case Studies →](chapters/14-case-studies.md)

### 💻 Development
- [API Reference →](api/python-api.md)
- [Contributing →](chapters/19-contributing.md)
- [Extending →](chapters/20-extending.md)

---

## Community & Support

- **GitHub**: [Repository](https://github.com/yourusername/AuditAgent)
- **Issues**: [Bug Reports & Feature Requests](https://github.com/yourusername/AuditAgent/issues)
- **Email**: anik@wayne.edu
- **Office Hours**: By appointment

---

## Acknowledgments

This project builds upon the groundbreaking work of:

- **Anthropic** - Smart contract security research
- **Ollama Team** - Local LLM inference
- **Foundry Team** - Blockchain development tools
- **Trail of Bits** - Slither static analyzer
- **OpenZeppelin** - Smart contract security patterns

Special thanks to my advisor and the Wayne State University Computer Science Department for supporting this research.

---

<div align="center">

**AuditAgent v2.0**
*Detecting Economic Vulnerabilities Through AI-Powered Analysis*

[Start Reading →](chapters/01-introduction.md)

</div>
