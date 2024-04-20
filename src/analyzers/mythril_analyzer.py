"""
Mythril symbolic execution integration.

Mythril uses symbolic execution and taint analysis to detect security
vulnerabilities in Ethereum smart contracts.
"""

import subprocess
import json
from typing import Dict, List, Optional


class MythrilAnalyzer:
    """Wrapper for Mythril symbolic execution tool."""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize Mythril analyzer.

        Args:
            config: Configuration dictionary for Mythril
        """
        self.config = config or {}
        self.timeout = self.config.get('timeout', 600)
        self.max_depth = self.config.get('max_depth', 128)
        self.execution_timeout = self.config.get('execution_timeout', 300)

    def analyze(self, contract_path: str) -> Dict:
        """
        Run Mythril analysis on a contract.

        Args:
            contract_path: Path to the Solidity contract

        Returns:
            Dictionary containing Mythril analysis results
        """
        try:
            # Build Mythril command
            cmd = [
                'myth',
                'analyze',
                contract_path,
                '--solv', '0.8.0',
                '--max-depth', str(self.max_depth),
                '--execution-timeout', str(self.execution_timeout),
                '-o', 'jsonv2'
            ]

            # Run Mythril
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            # Parse output
            mythril_output = self._parse_output(result.stdout, result.stderr)

            # Process results
            processed_results = self._process_results(mythril_output)

            return {
                'success': result.returncode == 0 or len(processed_results) > 0,
                'issues': processed_results,
                'raw_output': mythril_output
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Mythril analysis timed out after {self.timeout} seconds',
                'issues': []
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'Mythril not found. Please install with: pip install mythril',
                'issues': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Mythril analysis failed: {str(e)}',
                'issues': []
            }

    def _parse_output(self, stdout: str, stderr: str) -> Dict:
        """
        Parse Mythril output.

        Args:
            stdout: Standard output from Mythril
            stderr: Standard error from Mythril

        Returns:
            Parsed Mythril output
        """
        try:
            # Try to parse JSON output
            if stdout.strip():
                return json.loads(stdout)
            return {'raw': stderr}
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw output
            return {
                'raw': stdout if stdout else stderr,
                'issues': []
            }

    def _process_results(self, mythril_output: Dict) -> List[Dict]:
        """
        Process Mythril output into standardized format.

        Args:
            mythril_output: Raw Mythril output

        Returns:
            List of processed issue results
        """
        if not isinstance(mythril_output, dict):
            return []

        issues = mythril_output.get('issues', [])

        processed = []
        for issue in issues:
            processed.append({
                'title': issue.get('title', 'Unknown issue'),
                'swc_id': issue.get('swc-id', ''),
                'severity': self._map_severity(issue.get('severity', 'Low')),
                'description': issue.get('description', ''),
                'code': issue.get('code', ''),
                'filename': issue.get('filename', ''),
                'lineno': issue.get('lineno', 0),
                'source_mapping': issue.get('sourceMap', '')
            })

        return processed

    def _map_severity(self, mythril_severity: str) -> str:
        """
        Map Mythril severity to standard severity levels.

        Args:
            mythril_severity: Mythril severity level

        Returns:
            Standardized severity level
        """
        severity_map = {
            'High': 'critical',
            'Medium': 'high',
            'Low': 'medium'
        }
        return severity_map.get(mythril_severity, 'medium')

    def analyze_bytecode(self, bytecode: str) -> Dict:
        """
        Analyze compiled bytecode instead of source.

        Args:
            bytecode: Contract bytecode as hex string

        Returns:
            Analysis results
        """
        try:
            cmd = [
                'myth',
                'analyze',
                '--code', bytecode,
                '-o', 'jsonv2'
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            mythril_output = self._parse_output(result.stdout, result.stderr)
            processed_results = self._process_results(mythril_output)

            return {
                'success': result.returncode == 0,
                'issues': processed_results
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'issues': []
            }
