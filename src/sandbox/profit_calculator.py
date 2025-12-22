"""
Profit calculator for exploit validation.

Calculates actual dollar value of exploits based on blockchain results.
"""

import logging
from typing import Dict, Optional
from decimal import Decimal
from web3 import Web3
from rich.console import Console
from rich.table import Table

console = Console()
logger = logging.getLogger(__name__)


class ProfitCalculator:
    """
    Calculates profit from exploit results in USD.

    Converts native token profits (ETH, BNB, etc.) to USD values
    for meaningful impact assessment.
    """

    # Native token prices (should be fetched from oracle in production)
    DEFAULT_PRICES = {
        'ethereum': 2000.0,  # ETH price in USD
        'bsc': 300.0,        # BNB price in USD
        'polygon': 0.80,     # MATIC price in USD
        'arbitrum': 2000.0,  # Uses ETH
        'optimism': 2000.0,  # Uses ETH
    }

    def __init__(self, chain: str = 'bsc', native_price_usd: Optional[float] = None):
        """
        Initialize profit calculator.

        Args:
            chain: Blockchain network
            native_price_usd: Optional manual price for native token
        """
        self.chain = chain.lower()
        self.native_price_usd = native_price_usd or self.DEFAULT_PRICES.get(self.chain, 300.0)

    def calculate_profit(
        self,
        initial_balance_wei: int,
        final_balance_wei: int
    ) -> Dict[str, any]:
        """
        Calculate profit from balance change.

        Args:
            initial_balance_wei: Starting balance in wei
            final_balance_wei: Ending balance in wei

        Returns:
            Dictionary with profit calculations
        """
        # Calculate profit in wei
        profit_wei = final_balance_wei - initial_balance_wei

        # Convert to native token (18 decimals)
        profit_native = float(Web3.from_wei(profit_wei, 'ether'))

        # Convert to USD
        profit_usd = profit_native * self.native_price_usd

        # Calculate ROI
        if initial_balance_wei > 0:
            roi_percent = (profit_wei / initial_balance_wei) * 100
        else:
            roi_percent = 0.0

        return {
            'profit_wei': profit_wei,
            'profit_native': profit_native,
            'profit_usd': profit_usd,
            'initial_balance_wei': initial_balance_wei,
            'final_balance_wei': final_balance_wei,
            'roi_percent': roi_percent,
            'is_profitable': profit_wei > 0,
            'native_token': self._get_native_token_symbol(),
            'native_price_usd': self.native_price_usd
        }

    def calculate_from_test_results(self, test_results: Dict) -> Dict[str, any]:
        """
        Calculate profit from Foundry test results.

        Args:
            test_results: Results from ExploitRunner

        Returns:
            Profit calculation dictionary
        """
        parsed = test_results.get('parsed_output', {})

        initial = parsed.get('initial_balance', 0)
        final = parsed.get('final_balance', 0)

        # If parsed balances not available, try profit field
        if initial == 0 and final == 0:
            profit_wei = parsed.get('profit', 0)
            initial = 100 * 10**18  # Assume 100 ETH initial
            final = initial + profit_wei

        return self.calculate_profit(initial, final)

    def calculate_flash_loan_profit(
        self,
        loan_amount_wei: int,
        revenue_wei: int,
        fee_percent: float = 0.09
    ) -> Dict[str, any]:
        """
        Calculate flash loan exploit profit.

        Args:
            loan_amount_wei: Flash loan amount in wei
            revenue_wei: Revenue from exploit in wei
            fee_percent: Flash loan fee percentage (default 0.09%)

        Returns:
            Flash loan profit calculation
        """
        # Calculate flash loan fee
        fee_wei = int(loan_amount_wei * (fee_percent / 100))

        # Calculate gross profit
        gross_profit_wei = revenue_wei - loan_amount_wei

        # Calculate net profit (after fee)
        net_profit_wei = gross_profit_wei - fee_wei

        # Convert to native and USD
        gross_profit_native = float(Web3.from_wei(gross_profit_wei, 'ether'))
        net_profit_native = float(Web3.from_wei(net_profit_wei, 'ether'))
        fee_native = float(Web3.from_wei(fee_wei, 'ether'))

        gross_profit_usd = gross_profit_native * self.native_price_usd
        net_profit_usd = net_profit_native * self.native_price_usd
        fee_usd = fee_native * self.native_price_usd

        # Calculate ROI (based on fee paid, not loan amount)
        if fee_wei > 0:
            roi_percent = (net_profit_wei / fee_wei) * 100
        else:
            roi_percent = 0.0

        return {
            'loan_amount_wei': loan_amount_wei,
            'revenue_wei': revenue_wei,
            'gross_profit_wei': gross_profit_wei,
            'net_profit_wei': net_profit_wei,
            'fee_wei': fee_wei,
            'gross_profit_usd': gross_profit_usd,
            'net_profit_usd': net_profit_usd,
            'fee_usd': fee_usd,
            'roi_percent': roi_percent,
            'is_profitable': net_profit_wei > 0,
            'native_token': self._get_native_token_symbol()
        }

    def _get_native_token_symbol(self) -> str:
        """Get native token symbol for the chain."""
        symbols = {
            'ethereum': 'ETH',
            'bsc': 'BNB',
            'polygon': 'MATIC',
            'arbitrum': 'ETH',
            'optimism': 'ETH',
        }
        return symbols.get(self.chain, 'NATIVE')

    def generate_profit_report(self, profit_data: Dict) -> Table:
        """
        Generate rich table for profit visualization.

        Args:
            profit_data: Profit calculation results

        Returns:
            Rich Table object
        """
        table = Table(title="Exploit Profit Analysis")

        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        # Add rows
        native_symbol = profit_data.get('native_token', 'NATIVE')

        table.add_row(
            "Initial Balance",
            f"{Web3.from_wei(profit_data['initial_balance_wei'], 'ether'):.4f} {native_symbol}"
        )
        table.add_row(
            "Final Balance",
            f"{Web3.from_wei(profit_data['final_balance_wei'], 'ether'):.4f} {native_symbol}"
        )
        table.add_row(
            "Profit (Native)",
            f"[bold]{profit_data['profit_native']:.4f} {native_symbol}[/bold]"
        )
        table.add_row(
            "Profit (USD)",
            f"[bold green]${profit_data['profit_usd']:,.2f}[/bold green]"
        )
        table.add_row(
            "ROI",
            f"{profit_data['roi_percent']:.2f}%"
        )
        table.add_row(
            "Status",
            "[bold green]PROFITABLE[/bold green]" if profit_data['is_profitable']
            else "[bold red]NOT PROFITABLE[/bold red]"
        )

        return table

    def validate_exploit_profitability(
        self,
        profit_data: Dict,
        min_profit_usd: float = 100.0
    ) -> Dict[str, any]:
        """
        Validate if exploit meets profitability threshold.

        Args:
            profit_data: Profit calculation results
            min_profit_usd: Minimum profit threshold in USD

        Returns:
            Validation result
        """
        is_valid = (
            profit_data['is_profitable'] and
            profit_data['profit_usd'] >= min_profit_usd
        )

        severity = 'none'
        if profit_data['profit_usd'] >= 10000:
            severity = 'critical'
        elif profit_data['profit_usd'] >= 1000:
            severity = 'high'
        elif profit_data['profit_usd'] >= 100:
            severity = 'medium'
        elif profit_data['profit_usd'] > 0:
            severity = 'low'

        return {
            'is_valid_exploit': is_valid,
            'meets_threshold': profit_data['profit_usd'] >= min_profit_usd,
            'severity': severity,
            'profit_usd': profit_data['profit_usd'],
            'summary': f"Exploit {'IS' if is_valid else 'NOT'} profitable "
                      f"(${profit_data['profit_usd']:,.2f} profit)"
        }
