#!/usr/bin/env python3
"""
Example: Audit a deployed contract from blockchain.

This demonstrates how to fetch and audit a contract that's already deployed
on Ethereum, BSC, Polygon, or other supported chains.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audit_agent import AuditAgent
from src.fetchers.etherscan_fetcher import EtherscanFetcher


def audit_deployed_contract(address: str, chain: str = 'ethereum'):
    """
    Fetch and audit a deployed contract.

    Args:
        address: Contract address (0x...)
        chain: Blockchain network (ethereum, bsc, polygon, etc.)
    """
    print("=" * 80)
    print("AuditAgent - On-Chain Contract Audit Example")
    print("=" * 80)

    # Initialize fetcher
    fetcher = EtherscanFetcher()

    try:
        # Step 1: Fetch contract from blockchain
        print(f"\n[Step 1/3] Fetching contract from {chain}...")
        print(f"Address: {address}\n")

        contract_data = fetcher.fetch_contract(
            address=address,
            chain=chain,
            save_to=f"fetched_contract_{address[:8]}.sol"
        )

        print(f"\n✓ Contract fetched successfully!")
        print(f"  Name: {contract_data['name']}")
        print(f"  Compiler: {contract_data['compiler']}")
        print(f"  License: {contract_data['license']}")
        print(f"  Source lines: {len(contract_data['source_code'].splitlines())}")

        # Step 2: Save to temporary file for auditing
        print(f"\n[Step 2/3] Preparing contract for audit...")
        temp_file = f"/tmp/audit_{address[:10]}.sol"
        Path(temp_file).write_text(contract_data['source_code'])

        # Step 3: Run audit
        print(f"\n[Step 3/3] Running security audit...")
        print("-" * 80)

        agent = AuditAgent()
        results = agent.audit_contract(
            contract_path=temp_file,
            output_dir="reports"
        )

        # Display summary
        print("\n" + "=" * 80)
        print("AUDIT RESULTS")
        print("=" * 80)
        print(f"Contract: {contract_data['name']}")
        print(f"Chain: {chain}")
        print(f"Address: {address}")
        print(f"\nVulnerabilities Found: {results['summary']['total_vulnerabilities']}")
        print(f"Risk Score: {results['summary']['risk_score']:.1f}/100")

        print("\nSeverity Breakdown:")
        for severity, count in results['summary']['severity'].items():
            if count > 0:
                emoji = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🔵',
                    'informational': 'ℹ️'
                }.get(severity, '•')
                print(f"  {emoji} {severity.upper()}: {count}")

        if 'report_path' in results:
            print(f"\nDetailed report: {results['report_path']}")

        # Show top 3 critical issues
        critical_issues = [v for v in results.get('vulnerabilities', [])
                          if v.get('severity') == 'critical']

        if critical_issues:
            print(f"\n{'=' * 80}")
            print("TOP CRITICAL ISSUES")
            print("=" * 80)
            for i, issue in enumerate(critical_issues[:3], 1):
                print(f"\n{i}. {issue.get('type', 'Unknown').replace('_', ' ').title()}")
                print(f"   {issue.get('description', 'No description')}")
                if issue.get('line'):
                    print(f"   Location: Line {issue.get('line')}")

        # Cleanup
        if Path(temp_file).exists():
            Path(temp_file).unlink()

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


def main():
    """Run example audits."""
    print("\nExample 1: Audit a popular DeFi contract")
    print("-" * 80)

    # Example: Uniswap V2 Router (well-known contract)
    # You can replace this with any verified contract address
    example_address = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"

    audit_deployed_contract(
        address=example_address,
        chain='ethereum'
    )

    print("\n" + "=" * 80)
    print("Example complete!")
    print("=" * 80)
    print("\nTo audit other contracts, use:")
    print("  python audit_onchain_contract.py")
    print("\nOr use the CLI:")
    print(f"  auditagent audit-address {example_address} --chain ethereum")
    print("\nSupported chains:")
    for chain in EtherscanFetcher.get_supported_chains():
        print(f"  • {chain}")


if __name__ == "__main__":
    # You can modify this to audit any contract
    import os

    # Set your Etherscan API key (get free key at etherscan.io/myapikey)
    if not os.getenv('ETHERSCAN_API_KEY'):
        print("\n⚠️  Warning: ETHERSCAN_API_KEY not set")
        print("Get a free API key at: https://etherscan.io/myapikey")
        print("Set it with: export ETHERSCAN_API_KEY='your-key-here'\n")

    main()
