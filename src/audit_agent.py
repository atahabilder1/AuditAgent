"""
Main AuditAgent class that orchestrates the security audit process.
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

from src.analyzers.slither_analyzer import SlitherAnalyzer
from src.analyzers.mythril_analyzer import MythrilAnalyzer
from src.analyzers.ai_analyzer import AIAnalyzer
from src.detectors.vulnerability_detector import VulnerabilityDetector
from src.reporters.report_generator import ReportGenerator


class AuditAgent:
    """
    AI-powered smart contract security audit agent.

    Orchestrates multiple analysis tools and AI models to identify vulnerabilities
    in Solidity smart contracts including reentrancy, overflow/underflow,
    access control issues, and more.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the AuditAgent with optional configuration.

        Args:
            config: Configuration dictionary for analyzers and detectors
        """
        self.config = config or self._load_default_config()

        # Initialize analyzers
        self.slither_analyzer = SlitherAnalyzer(self.config.get('slither', {}))
        self.mythril_analyzer = MythrilAnalyzer(self.config.get('mythril', {}))
        self.ai_analyzer = AIAnalyzer(self.config.get('ai', {}))

        # Initialize detector and reporter
        self.vulnerability_detector = VulnerabilityDetector()
        self.report_generator = ReportGenerator()

        self.results = {}

    def _load_default_config(self) -> Dict:
        """Load default configuration."""
        return {
            'slither': {
                'timeout': 300,
                'exclude_informational': False
            },
            'mythril': {
                'timeout': 600,
                'max_depth': 128,
                'execution_timeout': 300
            },
            'ai': {
                'model': 'gpt-4',
                'temperature': 0.1,
                'max_tokens': 2000
            },
            'output': {
                'format': 'json',
                'verbose': True
            }
        }

    def audit_contract(self, contract_path: str, output_dir: Optional[str] = None) -> Dict:
        """
        Perform comprehensive security audit on a smart contract.

        Args:
            contract_path: Path to the Solidity contract file
            output_dir: Optional directory for audit reports

        Returns:
            Dictionary containing audit results from all analyzers
        """
        print(f"\n[AuditAgent] Starting security audit for: {contract_path}")
        print("=" * 80)

        if not os.path.exists(contract_path):
            raise FileNotFoundError(f"Contract not found: {contract_path}")

        # Initialize results
        self.results = {
            'contract': contract_path,
            'timestamp': datetime.now().isoformat(),
            'analyzers': {},
            'vulnerabilities': [],
            'summary': {}
        }

        # Phase 1: Static Analysis with Slither
        print("\n[Phase 1/4] Running Slither static analysis...")
        try:
            slither_results = self.slither_analyzer.analyze(contract_path)
            self.results['analyzers']['slither'] = slither_results
            print(f"  ✓ Found {len(slither_results.get('detectors', []))} potential issues")
        except Exception as e:
            print(f"  ✗ Slither analysis failed: {str(e)}")
            self.results['analyzers']['slither'] = {'error': str(e)}

        # Phase 2: Symbolic Execution with Mythril
        print("\n[Phase 2/4] Running Mythril symbolic execution...")
        try:
            mythril_results = self.mythril_analyzer.analyze(contract_path)
            self.results['analyzers']['mythril'] = mythril_results
            print(f"  ✓ Found {len(mythril_results.get('issues', []))} potential issues")
        except Exception as e:
            print(f"  ✗ Mythril analysis failed: {str(e)}")
            self.results['analyzers']['mythril'] = {'error': str(e)}

        # Phase 3: Vulnerability Pattern Detection
        print("\n[Phase 3/4] Running vulnerability pattern detection...")
        try:
            detected_vulns = self.vulnerability_detector.detect(contract_path, self.results)
            self.results['vulnerabilities'] = detected_vulns
            print(f"  ✓ Detected {len(detected_vulns)} vulnerability patterns")
        except Exception as e:
            print(f"  ✗ Detection failed: {str(e)}")
            self.results['vulnerabilities'] = []

        # Phase 4: AI-Powered Analysis
        print("\n[Phase 4/4] Running AI-powered security analysis...")
        try:
            ai_results = self.ai_analyzer.analyze(contract_path, self.results)
            self.results['analyzers']['ai'] = ai_results
            print(f"  ✓ AI analysis completed with {len(ai_results.get('recommendations', []))} recommendations")
        except Exception as e:
            print(f"  ✗ AI analysis failed: {str(e)}")
            self.results['analyzers']['ai'] = {'error': str(e)}

        # Generate summary
        self._generate_summary()

        # Generate and save report
        if output_dir:
            print(f"\n[Report] Generating audit report...")
            report_path = self.report_generator.generate(self.results, output_dir)
            print(f"  ✓ Report saved to: {report_path}")
            self.results['report_path'] = report_path

        print("\n" + "=" * 80)
        print(f"[AuditAgent] Audit complete! Total vulnerabilities: {self.results['summary']['total_vulnerabilities']}")
        print(f"  - Critical: {self.results['summary']['severity']['critical']}")
        print(f"  - High: {self.results['summary']['severity']['high']}")
        print(f"  - Medium: {self.results['summary']['severity']['medium']}")
        print(f"  - Low: {self.results['summary']['severity']['low']}")
        print("=" * 80 + "\n")

        return self.results

    def audit_directory(self, directory_path: str, output_dir: Optional[str] = None) -> List[Dict]:
        """
        Audit all Solidity contracts in a directory.

        Args:
            directory_path: Path to directory containing contracts
            output_dir: Optional directory for audit reports

        Returns:
            List of audit results for each contract
        """
        contracts = list(Path(directory_path).rglob("*.sol"))

        if not contracts:
            print(f"No Solidity contracts found in: {directory_path}")
            return []

        print(f"\n[AuditAgent] Found {len(contracts)} contracts to audit")

        all_results = []
        for i, contract in enumerate(contracts, 1):
            print(f"\n{'=' * 80}")
            print(f"Auditing contract {i}/{len(contracts)}: {contract.name}")
            print(f"{'=' * 80}")

            try:
                result = self.audit_contract(str(contract), output_dir)
                all_results.append(result)
            except Exception as e:
                print(f"Error auditing {contract}: {str(e)}")
                all_results.append({
                    'contract': str(contract),
                    'error': str(e)
                })

        return all_results

    def _generate_summary(self):
        """Generate audit summary statistics."""
        vulnerabilities = self.results.get('vulnerabilities', [])

        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'informational': 0
        }

        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'low').lower()
            if severity in severity_counts:
                severity_counts[severity] += 1

        self.results['summary'] = {
            'total_vulnerabilities': len(vulnerabilities),
            'severity': severity_counts,
            'analyzers_run': list(self.results.get('analyzers', {}).keys()),
            'risk_score': self._calculate_risk_score(severity_counts)
        }

    def _calculate_risk_score(self, severity_counts: Dict[str, int]) -> float:
        """
        Calculate overall risk score (0-100) based on vulnerabilities.

        Args:
            severity_counts: Dictionary of vulnerability counts by severity

        Returns:
            Risk score from 0 (safe) to 100 (critical)
        """
        weights = {
            'critical': 25,
            'high': 10,
            'medium': 5,
            'low': 2,
            'informational': 0.5
        }

        score = sum(count * weights[severity]
                   for severity, count in severity_counts.items())

        # Cap at 100
        return min(score, 100.0)
