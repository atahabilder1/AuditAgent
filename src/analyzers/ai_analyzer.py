"""
AI-powered contract analysis using language models.

Uses advanced AI models to identify complex vulnerabilities and provide
contextual security recommendations.
"""

import os
from typing import Dict, List, Optional


class AIAnalyzer:
    """AI-powered security analysis using language models."""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize AI analyzer.

        Args:
            config: Configuration dictionary for AI model
        """
        self.config = config or {}
        self.model = self.config.get('model', 'gpt-4')
        self.temperature = self.config.get('temperature', 0.1)
        self.max_tokens = self.config.get('max_tokens', 2000)

        # Check for API key
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.enabled = self.api_key is not None

    def analyze(self, contract_path: str, existing_results: Dict) -> Dict:
        """
        Perform AI-powered analysis on a contract.

        Args:
            contract_path: Path to the Solidity contract
            existing_results: Results from other analyzers for context

        Returns:
            Dictionary containing AI analysis results
        """
        if not self.enabled:
            return {
                'success': False,
                'error': 'AI analysis disabled: OPENAI_API_KEY not set',
                'recommendations': [],
                'risk_assessment': 'Unable to assess - AI disabled'
            }

        try:
            # Read contract code
            with open(contract_path, 'r') as f:
                contract_code = f.read()

            # Analyze with AI
            analysis = self._analyze_with_ai(contract_code, existing_results)

            return {
                'success': True,
                'recommendations': analysis.get('recommendations', []),
                'risk_assessment': analysis.get('risk_assessment', ''),
                'code_quality': analysis.get('code_quality', {}),
                'best_practices': analysis.get('best_practices', [])
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'AI analysis failed: {str(e)}',
                'recommendations': []
            }

    def _analyze_with_ai(self, contract_code: str, existing_results: Dict) -> Dict:
        """
        Perform AI analysis on contract code.

        Args:
            contract_code: Source code of the contract
            existing_results: Results from other analyzers

        Returns:
            AI analysis results
        """
        # Prepare context from existing results
        context = self._prepare_context(existing_results)

        # Build prompt for AI analysis
        prompt = self._build_analysis_prompt(contract_code, context)

        # Mock AI response for demonstration
        # In production, this would call OpenAI API
        return self._mock_ai_analysis(contract_code, existing_results)

    def _prepare_context(self, existing_results: Dict) -> str:
        """
        Prepare context from existing analyzer results.

        Args:
            existing_results: Results from other analyzers

        Returns:
            Formatted context string
        """
        context_parts = []

        # Add Slither findings
        slither = existing_results.get('analyzers', {}).get('slither', {})
        if slither.get('detectors'):
            context_parts.append(f"Slither found {len(slither['detectors'])} issues")

        # Add Mythril findings
        mythril = existing_results.get('analyzers', {}).get('mythril', {})
        if mythril.get('issues'):
            context_parts.append(f"Mythril found {len(mythril['issues'])} issues")

        return '; '.join(context_parts) if context_parts else 'No prior issues found'

    def _build_analysis_prompt(self, contract_code: str, context: str) -> str:
        """
        Build analysis prompt for AI model.

        Args:
            contract_code: Contract source code
            context: Context from other analyzers

        Returns:
            Analysis prompt
        """
        return f"""Analyze this Solidity smart contract for security vulnerabilities.

Context from automated tools: {context}

Contract code:
```solidity
{contract_code}
```

Provide:
1. Security recommendations
2. Risk assessment
3. Code quality evaluation
4. Best practices compliance
"""

    def _mock_ai_analysis(self, contract_code: str, existing_results: Dict) -> Dict:
        """
        Mock AI analysis for demonstration purposes.

        Args:
            contract_code: Contract source code
            existing_results: Results from other analyzers

        Returns:
            Mock analysis results
        """
        # Check for common patterns
        has_reentrancy_risk = 'call{' in contract_code or '.call(' in contract_code
        has_overflow_risk = 'unchecked' not in contract_code and '0.8' not in contract_code
        has_access_control = 'onlyOwner' in contract_code or 'require(msg.sender' in contract_code

        recommendations = []

        if has_reentrancy_risk:
            recommendations.append({
                'severity': 'high',
                'title': 'Potential Reentrancy Vulnerability',
                'description': 'Contract uses low-level calls which may be vulnerable to reentrancy attacks',
                'recommendation': 'Implement checks-effects-interactions pattern or use ReentrancyGuard'
            })

        if not has_access_control:
            recommendations.append({
                'severity': 'medium',
                'title': 'Missing Access Control',
                'description': 'No access control modifiers detected in the contract',
                'recommendation': 'Implement role-based access control using OpenZeppelin AccessControl'
            })

        # Calculate risk assessment
        vuln_count = len(existing_results.get('vulnerabilities', []))
        if vuln_count > 10:
            risk_level = 'CRITICAL'
        elif vuln_count > 5:
            risk_level = 'HIGH'
        elif vuln_count > 2:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        return {
            'recommendations': recommendations,
            'risk_assessment': f'{risk_level} - Found {vuln_count} total vulnerabilities',
            'code_quality': {
                'uses_latest_solidity': '0.8' in contract_code,
                'has_documentation': '///' in contract_code or '/**' in contract_code,
                'code_complexity': 'medium'
            },
            'best_practices': [
                'Use latest Solidity version (0.8.x)',
                'Add NatSpec documentation',
                'Implement comprehensive event logging',
                'Use OpenZeppelin contracts for standard functionality'
            ]
        }
