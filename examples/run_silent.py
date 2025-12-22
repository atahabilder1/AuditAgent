#!/usr/bin/env python3
"""
Silent mode - minimal output, just results.
"""

import sys
import logging
from pathlib import Path

# Suppress all logs except errors
logging.basicConfig(level=logging.ERROR)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audit_agent import AuditAgent


def main():
    """Run audit silently - only show final results."""

    # Initialize agent (silent)
    agent = AuditAgent()

    # Run audit (silent)
    results = agent.audit_contract(
        contract_path="tests/contracts/VulnerableBank.sol",
        output_dir="reports"
    )

    # Print only essential results
    print(f"\nVulnerabilities: {results['summary']['total_vulnerabilities']}")
    print(f"Risk Score: {results['summary']['risk_score']:.0f}/100")
    print(f"Report: {results.get('report_path', 'N/A')}\n")


if __name__ == "__main__":
    main()
