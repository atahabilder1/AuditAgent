#!/usr/bin/env python3
"""
Command-line interface for AuditAgent.

This provides a CLI tool for auditing smart contracts.
"""

import sys
import click
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audit_agent import AuditAgent
from src.fetchers.etherscan_fetcher import EtherscanFetcher


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """AuditAgent - AI-Powered Smart Contract Security Auditor"""
    pass


@cli.command()
@click.argument('contract_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='reports', help='Output directory for reports')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def audit(contract_path, output, config, verbose):
    """Audit a single smart contract file."""
    click.echo(f"Starting audit of: {contract_path}")

    # Load config if provided
    agent_config = None
    if config:
        import json
        with open(config, 'r') as f:
            agent_config = json.load(f)

    # Initialize agent
    agent = AuditAgent(config=agent_config)

    try:
        # Run audit
        results = agent.audit_contract(contract_path, output)

        # Display results
        click.echo("\n" + "=" * 80)
        click.echo("AUDIT COMPLETE")
        click.echo("=" * 80)

        severity = results['summary']['severity']
        if severity['critical'] > 0:
            click.secho(f"CRITICAL: {severity['critical']} issues found!", fg='red', bold=True)
        if severity['high'] > 0:
            click.secho(f"HIGH: {severity['high']} issues found", fg='red')
        if severity['medium'] > 0:
            click.secho(f"MEDIUM: {severity['medium']} issues found", fg='yellow')
        if severity['low'] > 0:
            click.echo(f"LOW: {severity['low']} issues found")

        click.echo(f"\nRisk Score: {results['summary']['risk_score']:.1f}/100")

        if 'report_path' in results:
            click.echo(f"Report saved to: {results['report_path']}")

    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        sys.exit(1)


@cli.command()
@click.argument('directory_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='reports', help='Output directory for reports')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
def audit_all(directory_path, output, config):
    """Audit all contracts in a directory."""
    click.echo(f"Auditing all contracts in: {directory_path}")

    # Load config if provided
    agent_config = None
    if config:
        import json
        with open(config, 'r') as f:
            agent_config = json.load(f)

    # Initialize agent
    agent = AuditAgent(config=agent_config)

    try:
        # Run audit on directory
        results = agent.audit_directory(directory_path, output)

        # Display summary
        click.echo("\n" + "=" * 80)
        click.echo(f"AUDITED {len(results)} CONTRACTS")
        click.echo("=" * 80)

        total_critical = sum(r.get('summary', {}).get('severity', {}).get('critical', 0) for r in results)
        total_high = sum(r.get('summary', {}).get('severity', {}).get('high', 0) for r in results)
        total_medium = sum(r.get('summary', {}).get('severity', {}).get('medium', 0) for r in results)

        if total_critical > 0:
            click.secho(f"Total CRITICAL: {total_critical}", fg='red', bold=True)
        if total_high > 0:
            click.secho(f"Total HIGH: {total_high}", fg='red')
        if total_medium > 0:
            click.secho(f"Total MEDIUM: {total_medium}", fg='yellow')

    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        sys.exit(1)


@cli.command()
@click.argument('address')
@click.option('--chain', '-c', default='ethereum', help='Blockchain network (ethereum, bsc, polygon, etc.)')
@click.option('--output', '-o', default='reports', help='Output directory for reports')
@click.option('--save-contract', '-s', is_flag=True, help='Save fetched contract to file')
def audit_address(address, chain, output, save_contract):
    """Audit a deployed contract from blockchain explorer."""
    try:
        # Validate address
        if not EtherscanFetcher.is_valid_address(address):
            click.secho(f"Error: Invalid contract address format: {address}", fg='red', err=True)
            click.echo("Address must be in format: 0x followed by 40 hexadecimal characters")
            sys.exit(1)

        # Initialize fetcher
        fetcher = EtherscanFetcher()

        click.echo(f"Fetching contract from {chain}...")
        click.echo(f"Address: {address}\n")

        # Fetch contract
        contract_data = fetcher.fetch_contract(
            address=address,
            chain=chain,
            save_to=f"temp_{address[:8]}.sol" if save_contract else None
        )

        # Save to temp file for auditing
        temp_file = f"/tmp/contract_{address[:10]}.sol"
        Path(temp_file).write_text(contract_data['source_code'])

        # Initialize agent and audit
        agent = AuditAgent()
        click.echo("\nStarting security audit...\n")

        results = agent.audit_contract(temp_file, output)

        # Add on-chain metadata to results
        results['on_chain_info'] = {
            'address': address,
            'chain': chain,
            'contract_name': contract_data['name'],
            'compiler': contract_data['compiler'],
            'verified': True
        }

        # Display results
        click.echo("\n" + "=" * 80)
        click.echo("AUDIT COMPLETE")
        click.echo("=" * 80)
        click.echo(f"Contract: {contract_data['name']} on {chain}")
        click.echo(f"Address: {address}\n")

        severity = results['summary']['severity']
        if severity['critical'] > 0:
            click.secho(f"CRITICAL: {severity['critical']} issues found!", fg='red', bold=True)
        if severity['high'] > 0:
            click.secho(f"HIGH: {severity['high']} issues found", fg='red')
        if severity['medium'] > 0:
            click.secho(f"MEDIUM: {severity['medium']} issues found", fg='yellow')
        if severity['low'] > 0:
            click.echo(f"LOW: {severity['low']} issues found")

        click.echo(f"\nRisk Score: {results['summary']['risk_score']:.1f}/100")

        if 'report_path' in results:
            click.echo(f"Report saved to: {results['report_path']}")

        # Cleanup temp file unless saved
        if not save_contract and Path(temp_file).exists():
            Path(temp_file).unlink()

    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        sys.exit(1)


@cli.command()
def chains():
    """List supported blockchain networks."""
    click.echo("Supported blockchain networks:\n")
    for chain in EtherscanFetcher.get_supported_chains():
        click.echo(f"  • {chain}")
    click.echo("\nUsage: auditagent audit-address <address> --chain <network>")


@cli.command()
def version():
    """Show version information."""
    click.echo("AuditAgent v1.0.0")
    click.echo("AI-Powered Smart Contract Security Auditor")
    click.echo("\nFeatures:")
    click.echo("  • Static analysis with Slither")
    click.echo("  • Symbolic execution with Mythril")
    click.echo("  • AI-powered vulnerability detection")
    click.echo("  • Multi-chain contract fetching")


def main():
    """Entry point for CLI."""
    cli()


if __name__ == '__main__':
    main()
