# Appendix A: References & Citations

[← Back to Documentation Home](../README.md)

---

This page contains all references, citations, and resources used in building AuditAgent v2.0.

## Table of Contents
- [A.1 Academic Papers](#a1-academic-papers)
- [A.2 Technical Documentation](#a2-technical-documentation)
- [A.3 Tools & Frameworks](#a3-tools--frameworks)
- [A.4 Datasets](#a4-datasets)
- [A.5 Blog Posts & Articles](#a5-blog-posts--articles)
- [A.6 Videos & Tutorials](#a6-videos--tutorials)

---

## A.1 Academic Papers

### Smart Contract Security

1. **Luu, L., Chu, D. H., Olickel, H., Saxena, P., & Hobor, A. (2016)**
   *Making Smart Contracts Smarter*
   Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security
   DOI: 10.1145/2976749.2978309
   [PDF](https://eprint.iacr.org/2016/633.pdf)

   **Key contribution**: Introduced systematic analysis of Ethereum smart contracts, identified common vulnerability patterns

2. **Atzei, N., Bartoletti, M., & Cimoli, T. (2017)**
   *A Survey of Attacks on Ethereum Smart Contracts (SoK)*
   Principles of Security and Trust
   DOI: 10.1007/978-3-662-54455-6_8
   [PDF](https://eprint.iacr.org/2016/1007.pdf)

   **Key contribution**: Comprehensive taxonomy of smart contract vulnerabilities

3. **Perez, D., & Livshits, B. (2021)**
   *Smart Contract Vulnerabilities: Vulnerable Does Not Imply Exploited*
   USENIX Security Symposium
   [PDF](https://www.usenix.org/system/files/sec21-perez.pdf)

   **Key contribution**: Analysis of 23,327 vulnerable contracts, only 1.98% exploited in practice

### DeFi & Economic Exploits

4. **Qin, K., Zhou, L., & Gervais, A. (2021)**
   *Quantifying Blockchain Extractable Value: How dark is the forest?*
   IEEE Symposium on Security and Privacy (S&P)
   DOI: 10.1109/SP40001.2021.00065
   [PDF](https://arxiv.org/pdf/2101.05511.pdf)

   **Key contribution**: Analyzed MEV and front-running attacks, $540K profit from one sandwich attack

5. **Zhou, L., Qin, K., Torres, C. F., Le, D. V., & Gervais, A. (2021)**
   *High-Frequency Trading on Decentralized On-Chain Exchanges*
   IEEE Symposium on Security and Privacy (S&P)
   [PDF](https://arxiv.org/pdf/2009.14021.pdf)

   **Key contribution**: Flash loan arbitrage detection, economic vulnerability patterns

6. **Wang, D., Wu, S., Lin, Z., Wu, L., Yuan, X., Zhou, Y., Wang, H., & Ren, K. (2021)**
   *Towards a First Step to Understand Flash Loan and Its Applications in DeFi Ecosystem*
   IMC '21: ACM Internet Measurement Conference
   DOI: 10.1145/3487552.3487811

   **Key contribution**: First comprehensive study of flash loans, analyzed 0.2M transactions

### AI for Security

7. **Anthropic. (2024)**
   *Finding Smart Contract Exploits with AI: A $4.6M Case Study*
   Anthropic AI Safety Blog
   [Link](https://red.anthropic.com/2025/smart-contracts/)

   **Key contribution**: Demonstrated AI agents finding real economic exploits, inspired this project

8. **Pearce, H., Tan, B., Ahmad, B., Karri, R., & Dolan-Gavitt, B. (2022)**
   *Examining Zero-Shot Vulnerability Repair with Large Language Models*
   IEEE Symposium on Security and Privacy (S&P)
   [PDF](https://arxiv.org/pdf/2112.02125.pdf)

   **Key contribution**: LLMs can fix vulnerabilities with 80%+ success rate

9. **Thapa, C., Jang, K., Ahmed, M. I., Camtepe, S., Pieprzyk, J., & Nepal, S. (2023)**
   *Transformer-based Language Models for Software Vulnerability Detection*
   ACM Computing Surveys
   DOI: 10.1145/3624747

   **Key contribution**: Survey of LLMs for vulnerability detection, compared GPT-4, CodeBERT, GraphCodeBERT

### Static Analysis

10. **Feist, J., Grieco, G., & Groce, A. (2019)**
    *Slither: A Static Analysis Framework For Smart Contracts*
    WETSEB '19: Workshop on Emerging Trends in Software Engineering for Blockchain
    DOI: 10.1109/WETSEB.2019.00008
    [PDF](https://arxiv.org/pdf/1908.09878.pdf)

    **Key contribution**: Slither framework, 80+ detectors, used by this project

11. **Brent, L., Grech, N., Lagouvardos, S., Scholz, B., & Smaragdakis, Y. (2020)**
    *Ethainter: A Smart Contract Security Analyzer for Composite Vulnerabilities*
    PLDI '20: Programming Language Design and Implementation
    DOI: 10.1145/3385412.3385990

    **Key contribution**: Taint analysis for smart contracts

---

## A.2 Technical Documentation

### Solidity & EVM

12. **Ethereum Foundation**
    *Solidity Documentation*
    Version 0.8.20
    [Link](https://docs.soliditylang.org/)

    **Usage**: Solidity language reference, used for exploit generation

13. **Ethereum Foundation**
    *Ethereum Yellow Paper*
    Dr. Gavin Wood
    [PDF](https://ethereum.github.io/yellowpaper/paper.pdf)

    **Usage**: EVM specification, opcodes, gas costs

14. **ConsenSys**
    *Smart Contract Security Best Practices*
    [Link](https://consensys.github.io/smart-contract-best-practices/)

    **Usage**: Security patterns, common pitfalls

### DeFi Protocols

15. **Uniswap Labs**
    *Uniswap V2 Core*
    Whitepaper
    [PDF](https://uniswap.org/whitepaper.pdf)

    **Usage**: AMM mechanics, price calculation for economic analysis

16. **PancakeSwap**
    *PancakeSwap V2 Documentation*
    [Link](https://docs.pancakeswap.finance/)

    **Usage**: BSC DEX integration, price queries

17. **Aave**
    *Aave Protocol Whitepaper V2*
    [PDF](https://github.com/aave/protocol-v2/blob/master/aave-v2-whitepaper.pdf)

    **Usage**: Flash loan mechanics for exploit templates

### LLM & AI

18. **Alibaba Cloud**
    *Qwen2.5-Coder Technical Report*
    November 2024
    [Link](https://qwenlm.github.io/blog/qwen2.5-coder/)

    **Usage**: Model used by AuditAgent, 32B parameters, code-specialized

19. **Ollama**
    *Ollama Documentation*
    [Link](https://github.com/ollama/ollama)

    **Usage**: Local LLM inference server

20. **Hugging Face**
    *PEFT: Parameter-Efficient Fine-Tuning*
    [Link](https://huggingface.co/docs/peft/)

    **Usage**: LoRA fine-tuning for security specialization

---

## A.3 Tools & Frameworks

### Security Analysis Tools

21. **Trail of Bits**
    *Slither - Solidity Static Analyzer*
    Version 0.9.x
    [GitHub](https://github.com/crytic/slither)

    **Usage**: Primary static analysis engine
    **License**: AGPL-3.0

22. **ConsenSys**
    *Mythril - Security Analysis Tool*
    [GitHub](https://github.com/ConsenSys/mythril)

    **Usage**: Symbolic execution (optional)
    **License**: MIT

23. **OpenZeppelin**
    *OpenZeppelin Contracts*
    Version 4.9.x
    [GitHub](https://github.com/OpenZeppelin/openzeppelin-contracts)

    **Usage**: Secure contract patterns, reference implementations
    **License**: MIT

### Blockchain Development

24. **Foundry**
    *Foundry Book - Forge, Cast, Anvil*
    [Link](https://book.getfoundry.sh/)

    **Usage**: Smart contract testing, blockchain forking
    **License**: MIT/Apache-2.0

25. **Web3.py**
    *Web3.py Documentation*
    Version 6.0+
    [Link](https://web3py.readthedocs.io/)

    **Usage**: Ethereum/BSC/Polygon interaction
    **License**: MIT

26. **Etherscan**
    *Etherscan API Documentation*
    [Link](https://docs.etherscan.io/)

    **Usage**: Contract source code fetching
    **License**: Proprietary (free tier available)

### Python Libraries

27. **Python Software Foundation**
    *Python 3.10/3.11 Documentation*
    [Link](https://docs.python.org/3/)

    **Usage**: Core programming language
    **License**: PSF

28. **Textualize**
    *Rich - Terminal Formatting*
    [GitHub](https://github.com/Textualize/rich)

    **Usage**: Beautiful terminal output
    **License**: MIT

29. **Pallets**
    *Click - Command Line Interface*
    [Link](https://click.palletsprojects.com/)

    **Usage**: CLI framework
    **License**: BSD-3-Clause

---

## A.4 Datasets

### Vulnerability Datasets

30. **SmartBugs**
    *SmartBugs: A Framework for Analyzing Ethereum Smart Contracts*
    Dataset of 47,398 contracts
    [GitHub](https://github.com/smartbugs/smartbugs)

    **Usage**: Test contracts for evaluation
    **License**: MIT

31. **DeFi Security Database**
    *Rekt.news - DeFi Exploit Database*
    [Link](https://rekt.news/)

    **Usage**: Real-world exploit examples for case studies

32. **Ethereum Signature Database**
    *4byte.directory*
    [Link](https://www.4byte.directory/)

    **Usage**: Function signature lookup

### Code Datasets

33. **GitHub**
    *Solidity Smart Contracts (Public Repositories)*
    ~500K contracts

    **Usage**: Fine-tuning data collection
    **License**: Various (check individual repos)

34. **Etherscan Verified Contracts**
    *Verified Source Code Database*
    ~1M contracts
    [API](https://etherscan.io/apis)

    **Usage**: Real-world contract analysis

---

## A.5 Blog Posts & Articles

35. **samczsun**
    *So you want to use a price oracle*
    2020
    [Link](https://samczsun.com/so-you-want-to-use-a-price-oracle/)

    **Key insight**: Price manipulation vulnerabilities

36. **OpenZeppelin Blog**
    *Reentrancy After Istanbul*
    2019
    [Link](https://blog.openzeppelin.com/reentrancy-after-istanbul/)

    **Key insight**: Modern reentrancy patterns

37. **Paradigm Research**
    *MEV and Me*
    2020
    [Link](https://research.paradigm.xyz/MEV)

    **Key insight**: Maximal Extractable Value

38. **Trail of Bits Blog**
    *Building Secure Smart Contracts*
    [Link](https://blog.trailofbits.com/)

    **Key insight**: Security engineering practices

---

## A.6 Videos & Tutorials

39. **Secureum**
    *RACE (Readiness Assessment for Certified Evaluators)*
    2021-2024
    [YouTube](https://www.youtube.com/c/Secureum)

    **Usage**: Smart contract security training

40. **Smart Contract Programmer**
    *Solidity Security Tutorials*
    [YouTube](https://www.youtube.com/c/SmartContractProgrammer)

    **Usage**: Practical vulnerability demonstrations

---

## Citation Guidelines

### For Academic Papers

If you use AuditAgent v2.0 in your research, please cite as:

```bibtex
@software{auditagent2024,
  author = {Anik},
  title = {AuditAgent v2.0: AI-Powered Smart Contract Security with Economic Exploit Detection},
  year = {2024},
  institution = {Wayne State University},
  url = {https://github.com/yourusername/AuditAgent},
  version = {2.0.0}
}
```

### For Blog Posts / Articles

**APA Style**:
```
Anik. (2024). AuditAgent v2.0: AI-Powered Smart Contract Security Analysis.
Wayne State University. Retrieved from https://github.com/yourusername/AuditAgent
```

**Chicago Style**:
```
Anik. "AuditAgent v2.0: AI-Powered Smart Contract Security Analysis."
Wayne State University, 2024. https://github.com/yourusername/AuditAgent.
```

---

## License Compliance

AuditAgent v2.0 uses these open-source projects:

| Project | License | Requirement |
|---------|---------|-------------|
| Slither | AGPL-3.0 | Must disclose source if distributed |
| Foundry | MIT/Apache-2.0 | Attribution required |
| Web3.py | MIT | Attribution required |
| Qwen | Apache-2.0 | Attribution required |
| Ollama | MIT | Attribution required |
| Rich | MIT | Attribution required |
| Click | BSD-3-Clause | Attribution required |

**AuditAgent v2.0 License**: MIT
**Implication**: You can use, modify, and distribute freely with attribution

---

## Acknowledgments

This research was made possible by:

1. **Wayne State University** - Institutional support
2. **Anthropic** - Inspiration from AI red team research
3. **Trail of Bits** - Slither framework
4. **Foundry Team** - Blockchain development tools
5. **Alibaba Cloud** - Qwen model
6. **Ollama Team** - Local LLM inference
7. **Open-source community** - All contributors to dependencies

---

## Staying Updated

New papers and tools are published regularly. Check:

- **arXiv.org** - cs.CR (Cryptography & Security)
- **IEEE S&P, USENIX Security** - Top security conferences
- **rekt.news** - Latest DeFi exploits
- **Trail of Bits Blog** - Security research
- **Paradigm Research** - MEV and DeFi

**Last Updated**: December 22, 2024
**Maintainer**: Anik (anik@wayne.edu)

---

[← Back to Documentation Home](../README.md)
