"""
Prompt templates for LLM-based security analysis.

Contains carefully crafted prompts for vulnerability detection,
exploit generation, and fix recommendations.
"""

from typing import Dict, List, Optional
import json


class PromptBuilder:
    """Builder for security analysis prompts."""

    @staticmethod
    def vulnerability_analysis_prompt(
        contract_code: str,
        slither_findings: List[Dict],
        context: Optional[str] = None
    ) -> str:
        """
        Build prompt for vulnerability analysis.

        Args:
            contract_code: Solidity source code
            slither_findings: Findings from Slither
            context: Additional context

        Returns:
            Formatted prompt string
        """
        slither_summary = "\n".join([
            f"- {finding.get('check', 'unknown')}: {finding.get('description', '')[:100]}"
            for finding in slither_findings[:10]  # Top 10 findings
        ])

        prompt = f"""You are a smart contract security expert. Analyze this Solidity contract for vulnerabilities.

CONTRACT CODE:
```solidity
{contract_code[:4000]}  # Limit to avoid token overflow
```

STATIC ANALYSIS FINDINGS (Slither):
{slither_summary if slither_summary else "No findings from Slither"}

{f"ADDITIONAL CONTEXT: {context}" if context else ""}

TASK:
Perform a comprehensive security analysis focusing on:

1. **Reentrancy vulnerabilities**: Check for state changes after external calls
2. **Access control**: Verify proper authentication and authorization
3. **Integer overflow/underflow**: Check arithmetic operations
4. **Front-running**: Identify transaction ordering dependencies
5. **Price manipulation**: Look for oracle issues and DEX price dependencies
6. **Economic exploits**: Identify arbitrage opportunities and economic attacks
7. **Logic errors**: Find business logic vulnerabilities

Return your analysis in JSON format:
{{
    "critical_vulnerabilities": [
        {{
            "type": "vulnerability type",
            "severity": "critical|high|medium|low",
            "location": "function or line reference",
            "description": "detailed description",
            "exploitation_scenario": "how this can be exploited",
            "impact": "potential damage in dollar terms if possible"
        }}
    ],
    "recommendations": [
        {{
            "priority": "high|medium|low",
            "issue": "what to fix",
            "solution": "how to fix it"
        }}
    ],
    "risk_score": 0-100,
    "overall_assessment": "summary of the contract's security posture"
}}

Focus on exploitable vulnerabilities that could lead to financial loss.
"""
        return prompt

    @staticmethod
    def exploit_generation_prompt(
        contract_code: str,
        vulnerability: Dict,
        chain: str = 'bsc'
    ) -> str:
        """
        Build prompt for generating exploit code.

        Args:
            contract_code: Target contract code
            vulnerability: Vulnerability details
            chain: Target blockchain

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert smart contract security researcher. Generate a working Solidity exploit for educational and defensive purposes.

TARGET CONTRACT:
```solidity
{contract_code[:3000]}
```

VULNERABILITY DETAILS:
Type: {vulnerability.get('type', 'unknown')}
Location: {vulnerability.get('location', 'unknown')}
Description: {vulnerability.get('description', '')}

CHAIN: {chain.upper()}

TASK:
Generate a complete Solidity exploit contract that demonstrates this vulnerability. The exploit should:

1. Be a standalone Solidity contract (FlawVerifier.sol pattern)
2. Include a `verify()` function that executes the exploit
3. Return true if exploit succeeds, false otherwise
4. Calculate actual profit in the chain's native token (BNB for BSC, ETH for Ethereum)
5. Include detailed comments explaining each step
6. Handle all edge cases properly

TEMPLATE STRUCTURE:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ITarget {{
    // Interface for target contract
}}

contract FlawVerifier {{
    address public target;

    constructor(address _target) {{
        target = _target;
    }}

    function verify() external returns (bool) {{
        // Exploit logic here
        // Return true if exploit succeeds
    }}

    // Helper functions
}}
```

Generate the complete exploit code with:
- All necessary interfaces and imports
- Detailed comments explaining the attack vector
- Profit calculation logic
- Safety checks

Return ONLY the Solidity code, no additional explanation.
"""
        return prompt

    @staticmethod
    def fix_suggestion_prompt(
        contract_code: str,
        vulnerability: Dict
    ) -> str:
        """
        Build prompt for fix suggestions.

        Args:
            contract_code: Vulnerable code
            vulnerability: Vulnerability details

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert smart contract developer. Provide a secure fix for this vulnerability.

VULNERABLE CODE:
```solidity
{contract_code[:3000]}
```

VULNERABILITY:
Type: {vulnerability.get('type', 'unknown')}
Location: {vulnerability.get('location', 'unknown')}
Description: {vulnerability.get('description', '')}
Severity: {vulnerability.get('severity', 'medium')}

TASK:
Provide a detailed fix recommendation in JSON format:

{{
    "vulnerability_summary": "brief summary of the issue",
    "fix_approach": "high-level approach to fixing this",
    "code_changes": [
        {{
            "location": "function or contract name",
            "change_type": "add|modify|remove",
            "original_code": "code snippet to change",
            "fixed_code": "corrected code snippet",
            "explanation": "why this fix works"
        }}
    ],
    "additional_recommendations": [
        "other improvements to consider"
    ],
    "testing_strategy": "how to test this fix",
    "gas_impact": "estimated gas cost change"
}}

Focus on:
- Security best practices (CEI pattern, reentrancy guards, etc.)
- OpenZeppelin contracts where applicable
- Gas optimization
- Code clarity and maintainability
"""
        return prompt

    @staticmethod
    def economic_analysis_prompt(
        contract_code: str,
        price_data: Dict
    ) -> str:
        """
        Build prompt for economic vulnerability analysis.

        Args:
            contract_code: Contract source code
            price_data: Price information from DEX

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a DeFi security expert specializing in economic exploits. Analyze this contract for economic vulnerabilities.

CONTRACT CODE:
```solidity
{contract_code[:3000]}
```

PRICE DATA:
{json.dumps(price_data, indent=2)}

TASK:
Analyze for economic vulnerabilities:

1. **Price Manipulation**: Can prices be manipulated?
2. **Arbitrage Opportunities**: Are there profitable arbitrage paths?
3. **Oracle Issues**: Are price oracles secure?
4. **Slippage Exploits**: Can slippage be exploited?
5. **Flash Loan Attacks**: Is the contract vulnerable to flash loans?
6. **MEV (Miner Extractable Value)**: What MEV opportunities exist?

Look for discrepancies between:
- Contract's internal price vs DEX price
- Different DEX prices
- Buy vs sell prices
- Expected vs actual slippage

Return analysis in JSON format:
{{
    "economic_vulnerabilities": [
        {{
            "type": "arbitrage|price_manipulation|oracle_manipulation|mev",
            "severity": "critical|high|medium|low",
            "description": "detailed description",
            "profit_potential": "estimated profit in USD",
            "execution_steps": ["step 1", "step 2", ...],
            "requirements": ["what's needed to exploit this"]
        }}
    ],
    "price_analysis": {{
        "contract_price": "price from contract",
        "market_price": "price from DEX",
        "discrepancy_percent": 0.0,
        "is_exploitable": true/false
    }},
    "recommendations": ["how to fix economic issues"],
    "profit_estimate": "total potential profit in USD"
}}

Focus on REAL exploitable economic vulnerabilities that were profitable.
"""
        return prompt

    @staticmethod
    def exploit_validation_prompt(
        exploit_code: str,
        test_results: Dict
    ) -> str:
        """
        Build prompt for analyzing exploit test results.

        Args:
            exploit_code: The exploit code that was tested
            test_results: Results from Foundry test

        Returns:
            Formatted prompt string
        """
        prompt = f"""Analyze these exploit test results and determine if the exploit is valid.

EXPLOIT CODE:
```solidity
{exploit_code[:2000]}
```

TEST RESULTS:
{json.dumps(test_results, indent=2)}

TASK:
Determine if the exploit successfully demonstrated the vulnerability:

1. Did the exploit execute without reverting?
2. Was there a measurable profit?
3. Did the exploit demonstrate the claimed vulnerability?
4. What was the actual dollar value of the exploit?

Return analysis in JSON format:
{{
    "is_valid_exploit": true/false,
    "profit_extracted": "amount in native token",
    "profit_usd": "estimated USD value",
    "success_criteria_met": {{
        "executed": true/false,
        "profitable": true/false,
        "demonstrates_vulnerability": true/false
    }},
    "summary": "brief summary of test results",
    "confidence": 0-100
}}
"""
        return prompt

    @staticmethod
    def system_prompt_for_security() -> str:
        """
        Get the system prompt for security analysis.

        Returns:
            System prompt string
        """
        return """You are an elite smart contract security researcher with expertise in:

- Solidity and EVM internals
- DeFi protocols and economic exploits
- Common vulnerability patterns (reentrancy, access control, etc.)
- Exploit development and proof-of-concept creation
- Secure coding practices and remediation

Your goal is to identify REAL, EXPLOITABLE vulnerabilities that could lead to financial loss.
Focus on vulnerabilities that have been proven in the wild, not theoretical issues.

Be precise, technical, and provide actionable insights.
Always include dollar amounts when discussing potential exploits.
"""
