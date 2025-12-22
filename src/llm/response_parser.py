"""
Parser for LLM responses.

Handles parsing and validation of JSON responses from the LLM,
including error handling and fallback strategies.
"""

import json
import re
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class ResponseParser:
    """Parser for LLM JSON responses with robust error handling."""

    @staticmethod
    def parse_vulnerability_analysis(response: str) -> Dict[str, Any]:
        """
        Parse vulnerability analysis response from LLM.

        Args:
            response: Raw LLM response

        Returns:
            Parsed vulnerability analysis dictionary
        """
        try:
            # Try direct JSON parsing
            data = json.loads(response)
            return ResponseParser._validate_vulnerability_schema(data)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    return ResponseParser._validate_vulnerability_schema(data)
                except json.JSONDecodeError:
                    pass

            # Fallback: return structured error
            logger.warning("Failed to parse vulnerability analysis response")
            return {
                'critical_vulnerabilities': [],
                'recommendations': [],
                'risk_score': 0,
                'overall_assessment': 'Failed to parse LLM response',
                'parse_error': True,
                'raw_response': response[:500]
            }

    @staticmethod
    def parse_exploit_code(response: str) -> Dict[str, Any]:
        """
        Parse exploit generation response.

        Args:
            response: Raw LLM response containing Solidity code

        Returns:
            Dictionary with parsed exploit code
        """
        # Extract Solidity code from response
        solidity_match = re.search(
            r'```solidity\s*(.*?)\s*```',
            response,
            re.DOTALL | re.IGNORECASE
        )

        if solidity_match:
            code = solidity_match.group(1).strip()
        else:
            # Try without language specifier
            code_match = re.search(r'```\s*(.*?)\s*```', response, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
            else:
                # Use entire response if no code blocks found
                code = response.strip()

        # Validate it looks like Solidity
        has_pragma = 'pragma solidity' in code.lower()
        has_contract = 'contract ' in code

        return {
            'exploit_code': code,
            'is_valid_solidity': has_pragma and has_contract,
            'has_verify_function': 'function verify()' in code,
            'code_length': len(code),
            'raw_response': response
        }

    @staticmethod
    def parse_fix_suggestion(response: str) -> Dict[str, Any]:
        """
        Parse fix suggestion response.

        Args:
            response: Raw LLM response

        Returns:
            Parsed fix suggestions
        """
        try:
            # Try direct JSON parsing
            data = json.loads(response)
            return ResponseParser._validate_fix_schema(data)
        except json.JSONDecodeError:
            # Try to extract JSON from code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    return ResponseParser._validate_fix_schema(data)
                except json.JSONDecodeError:
                    pass

            # Fallback
            logger.warning("Failed to parse fix suggestion response")
            return {
                'vulnerability_summary': 'Parse error',
                'fix_approach': response[:200],
                'code_changes': [],
                'additional_recommendations': [],
                'testing_strategy': 'Unknown',
                'gas_impact': 'Unknown',
                'parse_error': True
            }

    @staticmethod
    def parse_economic_analysis(response: str) -> Dict[str, Any]:
        """
        Parse economic vulnerability analysis.

        Args:
            response: Raw LLM response

        Returns:
            Parsed economic analysis
        """
        try:
            data = json.loads(response)
            return ResponseParser._validate_economic_schema(data)
        except json.JSONDecodeError:
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    return ResponseParser._validate_economic_schema(data)
                except json.JSONDecodeError:
                    pass

            logger.warning("Failed to parse economic analysis response")
            return {
                'economic_vulnerabilities': [],
                'price_analysis': {},
                'recommendations': [],
                'profit_estimate': '$0',
                'parse_error': True,
                'raw_response': response[:500]
            }

    @staticmethod
    def _validate_vulnerability_schema(data: Dict) -> Dict[str, Any]:
        """Validate and normalize vulnerability analysis schema."""
        return {
            'critical_vulnerabilities': data.get('critical_vulnerabilities', []),
            'recommendations': data.get('recommendations', []),
            'risk_score': min(100, max(0, data.get('risk_score', 0))),
            'overall_assessment': data.get('overall_assessment', ''),
            'parse_error': False
        }

    @staticmethod
    def _validate_fix_schema(data: Dict) -> Dict[str, Any]:
        """Validate and normalize fix suggestion schema."""
        return {
            'vulnerability_summary': data.get('vulnerability_summary', ''),
            'fix_approach': data.get('fix_approach', ''),
            'code_changes': data.get('code_changes', []),
            'additional_recommendations': data.get('additional_recommendations', []),
            'testing_strategy': data.get('testing_strategy', ''),
            'gas_impact': data.get('gas_impact', 'Unknown'),
            'parse_error': False
        }

    @staticmethod
    def _validate_economic_schema(data: Dict) -> Dict[str, Any]:
        """Validate and normalize economic analysis schema."""
        return {
            'economic_vulnerabilities': data.get('economic_vulnerabilities', []),
            'price_analysis': data.get('price_analysis', {}),
            'recommendations': data.get('recommendations', []),
            'profit_estimate': data.get('profit_estimate', '$0'),
            'parse_error': False
        }

    @staticmethod
    def extract_dollar_amount(text: str) -> Optional[float]:
        """
        Extract dollar amount from text.

        Args:
            text: Text containing dollar amount

        Returns:
            Extracted amount as float, or None
        """
        # Match patterns like $1,234.56 or $1.2M or $5K
        patterns = [
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',  # $1,234.56
            r'\$\s*(\d+(?:\.\d+)?)\s*M',  # $1.2M
            r'\$\s*(\d+(?:\.\d+)?)\s*K',  # $5K
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(',', '')
                amount = float(value)

                # Handle M and K suffixes
                if 'M' in text[match.start():match.end()+2]:
                    amount *= 1_000_000
                elif 'K' in text[match.start():match.end()+2]:
                    amount *= 1_000

                return amount

        return None

    @staticmethod
    def calculate_severity_score(vulnerabilities: List[Dict]) -> int:
        """
        Calculate overall severity score from vulnerabilities.

        Args:
            vulnerabilities: List of vulnerability dictionaries

        Returns:
            Severity score (0-100)
        """
        severity_weights = {
            'critical': 25,
            'high': 10,
            'medium': 5,
            'low': 2
        }

        score = 0
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'low').lower()
            weight = severity_weights.get(severity, 1)
            score += weight

        return min(100, score)
