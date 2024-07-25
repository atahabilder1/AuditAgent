#!/usr/bin/env python3
"""
Basic usage example for AuditAgent.

This script demonstrates how to use AuditAgent to audit a single contract.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audit_agent import AuditAgent


def main():
    """Run basic audit example."""
    # Initialize AuditAgent
    agent = AuditAgent()

    # Path to contract
    contract_path = "tests/contracts/VulnerableBank.sol"

    print("=" * 80)
    print("AuditAgent - Basic Usage Example")
    print("=" * 80)
    print(f"\nAuditing contract: {contract_path}\n")

    # Run audit
    try:
        results = agent.audit_contract(
            contract_path=contract_path,
            output_dir="reports"
        )

        # Display summary
        print("\n" + "=" * 80)
        print("AUDIT SUMMARY")
        print("=" * 80)
        print(f"Total Vulnerabilities: {results['summary']['total_vulnerabilities']}")
        print(f"Risk Score: {results['summary']['risk_score']:.1f}/100")
        print(f"\nSeverity Breakdown:")
        for severity, count in results['summary']['severity'].items():
            if count > 0:
                print(f"  {severity.upper()}: {count}")

        if 'report_path' in results:
            print(f"\nDetailed report saved to: {results['report_path']}")

    except FileNotFoundError:
        print(f"Error: Contract not found at {contract_path}")
        print("Make sure you're running this from the project root directory.")
    except Exception as e:
        print(f"Error during audit: {str(e)}")


if __name__ == "__main__":
    main()
