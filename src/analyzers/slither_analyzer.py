"""
Slither static analysis integration.

Slither is a Solidity static analysis framework that detects vulnerabilities
and provides detailed information about smart contract code quality.
"""

import subprocess
import json
from typing import Dict, List, Optional
from pathlib import Path


class SlitherAnalyzer:
    """Wrapper for Slither static analysis tool."""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize Slither analyzer.

        Args:
            config: Configuration dictionary for Slither
        """
        self.config = config or {}
        self.timeout = self.config.get('timeout', 300)
        self.exclude_informational = self.config.get('exclude_informational', False)

    def analyze(self, contract_path: str) -> Dict:
        """
        Run Slither analysis on a contract.

        Args:
            contract_path: Path to the Solidity contract

        Returns:
            Dictionary containing Slither analysis results
        """
        try:
            # Build Slither command
            cmd = [
                'slither',
                contract_path,
                '--json', '-',
                '--exclude-informational' if self.exclude_informational else '--exclude-dependencies'
            ]

            # Run Slither
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            # Parse JSON output
            if result.stdout:
                try:
                    slither_output = json.loads(result.stdout)
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    slither_output = {'raw_output': result.stdout}
            else:
                slither_output = {'raw_output': result.stderr}

            # Process and categorize results
            processed_results = self._process_results(slither_output)

            return {
                'success': result.returncode == 0,
                'detectors': processed_results,
                'raw_output': slither_output
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Slither analysis timed out after {self.timeout} seconds',
                'detectors': []
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'Slither not found. Please install with: pip install slither-analyzer',
                'detectors': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Slither analysis failed: {str(e)}',
                'detectors': []
            }

    def _process_results(self, slither_output: Dict) -> List[Dict]:
        """
        Process Slither output into standardized format.

        Args:
            slither_output: Raw Slither output

        Returns:
            List of processed detector results
        """
        if not isinstance(slither_output, dict):
            return []

        results = slither_output.get('results', {})
        detectors = results.get('detectors', [])

        processed = []
        for detector in detectors:
            processed.append({
                'check': detector.get('check', 'unknown'),
                'impact': detector.get('impact', 'unknown'),
                'confidence': detector.get('confidence', 'unknown'),
                'description': detector.get('description', ''),
                'elements': detector.get('elements', []),
                'first_markdown_element': detector.get('first_markdown_element', ''),
                'severity': self._map_impact_to_severity(detector.get('impact', 'Low'))
            })

        return processed

    def _map_impact_to_severity(self, impact: str) -> str:
        """
        Map Slither impact to standard severity levels.

        Args:
            impact: Slither impact level

        Returns:
            Standardized severity level
        """
        impact_map = {
            'High': 'critical',
            'Medium': 'high',
            'Low': 'medium',
            'Informational': 'low',
            'Optimization': 'informational'
        }
        return impact_map.get(impact, 'medium')

    def get_specific_detector(self, contract_path: str, detector_name: str) -> Dict:
        """
        Run a specific Slither detector.

        Args:
            contract_path: Path to the Solidity contract
            detector_name: Name of the detector to run

        Returns:
            Results from the specific detector
        """
        try:
            cmd = [
                'slither',
                contract_path,
                '--detect', detector_name,
                '--json', '-'
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if result.stdout:
                return json.loads(result.stdout)
            return {}

        except Exception as e:
            return {'error': str(e)}
