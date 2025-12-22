#!/usr/bin/env python3
"""
Enhanced usage example with detailed logging.

This script shows the audit process step-by-step with comprehensive logging
so you can understand what's happening at each phase.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audit_agent import AuditAgent

# Initialize Rich console for beautiful output
console = Console()


def setup_logging(verbose=True):
    """
    Configure logging with Rich handler for beautiful console output.

    Args:
        verbose: If True, show DEBUG level logs. Otherwise, show INFO level.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )

    # Set specific loggers
    logging.getLogger("src").setLevel(logging.DEBUG if verbose else logging.INFO)
    logging.getLogger("slither").setLevel(logging.WARNING)  # Reduce Slither noise


def print_header():
    """Print a beautiful header."""
    console.print(Panel.fit(
        "[bold cyan]AuditAgent v2.0[/bold cyan]\n"
        "[white]AI-Powered Smart Contract Security Analysis[/white]\n"
        "[dim]With Economic Vulnerability Detection[/dim]",
        border_style="cyan"
    ))


def print_phase(phase_number, phase_name, description):
    """Print phase information."""
    console.print(f"\n[bold yellow]{'='*80}[/bold yellow]")
    console.print(f"[bold yellow]PHASE {phase_number}: {phase_name}[/bold yellow]")
    console.print(f"[dim]{description}[/dim]")
    console.print(f"[bold yellow]{'='*80}[/bold yellow]\n")


def print_results_table(results):
    """Print results in a beautiful table."""
    # Severity breakdown table
    table = Table(title="Vulnerability Breakdown", show_header=True, header_style="bold magenta")
    table.add_column("Severity", style="cyan", justify="left")
    table.add_column("Count", style="yellow", justify="right")
    table.add_column("Visual", style="red")

    severity_order = ['critical', 'high', 'medium', 'low', 'informational']
    severity_colors = {
        'critical': 'red',
        'high': 'orange1',
        'medium': 'yellow',
        'low': 'blue',
        'informational': 'dim'
    }

    for severity in severity_order:
        count = results['summary']['severity'].get(severity, 0)
        if count > 0:
            color = severity_colors[severity]
            bar = "█" * min(count, 50)  # Visual bar
            table.add_row(
                f"[{color}]{severity.upper()}[/{color}]",
                f"[{color}]{count}[/{color}]",
                f"[{color}]{bar}[/{color}]"
            )

    console.print(table)


def main():
    """Run audit with detailed logging."""
    # Setup
    setup_logging(verbose=True)  # Set to False for less verbose output
    print_header()

    # Configuration
    contract_path = "tests/contracts/VulnerableBank.sol"
    output_dir = "reports"

    console.print(f"[bold]Contract:[/bold] {contract_path}")
    console.print(f"[bold]Output Directory:[/bold] {output_dir}")
    console.print(f"[bold]Time:[/bold] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        # Phase 1: Initialization
        print_phase(1, "INITIALIZATION", "Loading AuditAgent and checking environment...")

        with console.status("[bold green]Initializing AuditAgent...", spinner="dots"):
            agent = AuditAgent()

        console.print("✅ [green]AuditAgent initialized successfully[/green]")
        console.print(f"   • Configuration loaded")
        console.print(f"   • Analyzers ready: Slither, Pattern Detector, Advanced Detector")
        console.print(f"   • LLM Status: {'Available' if agent.config.get('ai', {}).get('enabled', False) else 'Disabled'}")

        # Phase 2: Contract Loading
        print_phase(2, "CONTRACT LOADING", "Reading and parsing the smart contract...")

        console.print(f"📄 Reading contract from: [cyan]{contract_path}[/cyan]")

        if not Path(contract_path).exists():
            console.print(f"[bold red]❌ Error: Contract not found at {contract_path}[/bold red]")
            console.print("[yellow]💡 Tip: Make sure you're running from the project root directory[/yellow]")
            return

        # Get file info
        file_size = Path(contract_path).stat().st_size
        with open(contract_path, 'r') as f:
            lines = len(f.readlines())

        console.print(f"   • File size: {file_size} bytes")
        console.print(f"   • Lines of code: {lines}")
        console.print("✅ [green]Contract loaded successfully[/green]")

        # Phase 3: Static Analysis
        print_phase(3, "STATIC ANALYSIS", "Running Slither and pattern-based detectors...")

        start_time = datetime.now()

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:

            task1 = progress.add_task("[cyan]Running Slither static analysis...", total=None)
            task2 = progress.add_task("[cyan]Running pattern detectors...", total=None)
            task3 = progress.add_task("[cyan]Running advanced detectors...", total=None)

            # Run audit (this is where the actual analysis happens)
            results = agent.audit_contract(
                contract_path=contract_path,
                output_dir=output_dir
            )

            progress.update(task1, completed=True)
            progress.update(task2, completed=True)
            progress.update(task3, completed=True)

        analysis_time = (datetime.now() - start_time).total_seconds()

        console.print(f"✅ [green]Analysis completed in {analysis_time:.2f} seconds[/green]")

        # Phase 4: Results Aggregation
        print_phase(4, "RESULTS AGGREGATION", "Combining findings from all analyzers...")

        total_vulns = results['summary']['total_vulnerabilities']
        risk_score = results['summary']['risk_score']

        # Determine color based on risk score
        risk_color = 'red' if risk_score > 70 else ('yellow' if risk_score > 40 else 'green')

        console.print(f"   • Total vulnerabilities found: [bold red]{total_vulns}[/bold red]")
        console.print(f"   • Risk score: [bold {risk_color}]{risk_score:.1f}/100[/bold {risk_color}]")
        console.print(f"   • Analyzers run: {', '.join(results['summary']['analyzers_run'])}")

        # Phase 5: Report Generation
        print_phase(5, "REPORT GENERATION", "Creating detailed markdown report...")

        if 'report_path' in results:
            console.print(f"📝 Report generated: [cyan]{results['report_path']}[/cyan]")

            # Show report stats
            report_size = Path(results['report_path']).stat().st_size
            console.print(f"   • Report size: {report_size} bytes")
            console.print(f"   • Format: Markdown")
            console.print("✅ [green]Report saved successfully[/green]")

        # Final Summary
        console.print("\n" + "=" * 80)
        console.print("[bold cyan]FINAL SUMMARY[/bold cyan]")
        console.print("=" * 80 + "\n")

        print_results_table(results)

        # Risk assessment
        console.print(f"\n[bold]Risk Assessment:[/bold]")
        if risk_score >= 80:
            console.print("🔴 [bold red]CRITICAL RISK - Immediate action required![/bold red]")
            console.print("   Multiple critical vulnerabilities detected. Do NOT deploy this contract.")
        elif risk_score >= 50:
            console.print("🟠 [bold orange1]HIGH RISK - Significant issues found[/bold orange1]")
            console.print("   Major vulnerabilities present. Requires thorough review and fixes.")
        elif risk_score >= 30:
            console.print("🟡 [bold yellow]MEDIUM RISK - Some issues detected[/bold yellow]")
            console.print("   Vulnerabilities found but may not be critical. Review recommended.")
        else:
            console.print("🟢 [bold green]LOW RISK - Minor or no issues[/bold green]")
            console.print("   Contract appears relatively secure. Standard review recommended.")

        # Next steps
        console.print(f"\n[bold]Next Steps:[/bold]")
        console.print(f"1. Review the detailed report: [cyan]{results.get('report_path', 'reports/')}[/cyan]")
        console.print(f"2. Fix critical and high severity issues")
        console.print(f"3. Run audit again to verify fixes")
        console.print(f"4. Consider professional manual audit for production contracts")

        # Show some example vulnerabilities
        if results.get('vulnerabilities'):
            console.print(f"\n[bold]Top 3 Critical Findings:[/bold]")
            critical_vulns = [v for v in results['vulnerabilities'] if v.get('severity') == 'critical'][:3]

            for i, vuln in enumerate(critical_vulns, 1):
                console.print(f"\n  {i}. [bold red]{vuln.get('type', 'Unknown')}[/bold red]")
                console.print(f"     Line {vuln.get('line', 'N/A')}: {vuln.get('description', 'No description')[:80]}...")

        console.print("\n" + "=" * 80)
        console.print("[bold green]✅ Audit completed successfully![/bold green]")
        console.print("=" * 80 + "\n")

    except FileNotFoundError as e:
        console.print(f"\n[bold red]❌ Error: Contract not found[/bold red]")
        console.print(f"[red]{str(e)}[/red]")
        console.print("\n[yellow]💡 Tip: Make sure you're running this from the project root directory.[/yellow]")
        console.print(f"[yellow]Current directory: {Path.cwd()}[/yellow]")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error during audit:[/bold red]")
        # Escape special characters for Rich
        error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
        console.print(f"[red]{error_msg}[/red]")

        # Show traceback in debug mode
        import traceback
        console.print("\n[dim]Full traceback:[/dim]")
        tb = traceback.format_exc().replace("[", "\\[").replace("]", "\\]")
        console.print(tb)


if __name__ == "__main__":
    # You can also pass arguments
    import argparse

    parser = argparse.ArgumentParser(description="Run AuditAgent with detailed logging")
    parser.add_argument("--contract", "-c", default="tests/contracts/VulnerableBank.sol",
                        help="Path to contract file")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Reduce logging verbosity")

    args = parser.parse_args()

    main()
