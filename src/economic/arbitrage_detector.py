"""
Arbitrage opportunity detector.

Identifies profitable arbitrage opportunities between contract prices
and DEX prices, similar to Anthropic's $4.6M exploit discovery.
"""

import logging
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from rich.console import Console
from rich.panel import Panel

console = Console()
logger = logging.getLogger(__name__)


class ArbitrageDetector:
    """
    Detects arbitrage opportunities in smart contracts.

    Focuses on finding economic exploits where tokens can be bought
    at one price and sold at another for guaranteed profit.
    """

    def __init__(self, min_profit_usd: float = 100.0):
        """
        Initialize arbitrage detector.

        Args:
            min_profit_usd: Minimum profit threshold in USD to flag
        """
        self.min_profit_usd = min_profit_usd

    def detect_simple_arbitrage(
        self,
        buy_price: float,
        sell_price: float,
        volume: Optional[float] = None
    ) -> Optional[Dict]:
        """
        Detect simple arbitrage opportunity (buy low, sell high).

        Args:
            buy_price: Price to buy token
            sell_price: Price to sell token
            volume: Optional volume in tokens

        Returns:
            Arbitrage opportunity details or None
        """
        if sell_price <= buy_price:
            return None

        profit_per_token = sell_price - buy_price
        profit_percent = (profit_per_token / buy_price) * 100

        if volume:
            total_profit = profit_per_token * volume
        else:
            # Assume 1000 token volume for estimation
            total_profit = profit_per_token * 1000
            volume = 1000

        if total_profit >= self.min_profit_usd:
            return {
                'type': 'simple_arbitrage',
                'buy_price': buy_price,
                'sell_price': sell_price,
                'profit_per_token': profit_per_token,
                'profit_percent': profit_percent,
                'estimated_volume': volume,
                'total_profit_usd': total_profit,
                'execution_steps': [
                    f'1. Buy tokens at ${buy_price:.4f}',
                    f'2. Sell tokens at ${sell_price:.4f}',
                    f'3. Profit: ${profit_per_token:.4f} per token'
                ]
            }

        return None

    def detect_triangular_arbitrage(
        self,
        prices: List[Dict[str, float]]
    ) -> List[Dict]:
        """
        Detect triangular arbitrage opportunities across three tokens.

        Args:
            prices: List of price dictionaries from different pairs

        Returns:
            List of triangular arbitrage opportunities
        """
        opportunities = []

        # Need at least 3 pairs for triangular arbitrage
        if len(prices) < 3:
            return opportunities

        # Try all combinations of 3 prices
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                for k in range(j + 1, len(prices)):
                    opportunity = self._calculate_triangular_profit(
                        prices[i], prices[j], prices[k]
                    )
                    if opportunity and opportunity['profit_usd'] >= self.min_profit_usd:
                        opportunities.append(opportunity)

        return opportunities

    def _calculate_triangular_profit(
        self,
        price1: Dict,
        price2: Dict,
        price3: Dict
    ) -> Optional[Dict]:
        """Calculate profit from triangular arbitrage path."""
        # This is a simplified version
        # Real implementation would need to match token pairs correctly
        try:
            # Simulate: Start with 1000 USD
            start_amount = 1000.0

            # Convert USD -> Token1
            token1_amount = start_amount / price1.get('price_usd', 1)

            # Convert Token1 -> Token2 (using ratio)
            token2_amount = token1_amount * price2.get('price_usd', 1) / price1.get('price_usd', 1)

            # Convert Token2 -> USD
            final_usd = token2_amount * price3.get('price_usd', 1)

            profit = final_usd - start_amount

            if profit > 0:
                return {
                    'type': 'triangular_arbitrage',
                    'start_amount': start_amount,
                    'final_amount': final_usd,
                    'profit_usd': profit,
                    'profit_percent': (profit / start_amount) * 100,
                    'path': [
                        price1.get('dex', 'unknown'),
                        price2.get('dex', 'unknown'),
                        price3.get('dex', 'unknown')
                    ]
                }
        except (KeyError, ZeroDivisionError, TypeError):
            pass

        return None

    def detect_flash_loan_arbitrage(
        self,
        contract_analysis: Dict,
        dex_prices: List[Dict]
    ) -> List[Dict]:
        """
        Detect flash loan arbitrage opportunities.

        Flash loans allow borrowing large amounts without collateral,
        enabling exploitation of small price discrepancies at scale.

        Args:
            contract_analysis: Economic analysis of contract
            dex_prices: DEX price data

        Returns:
            List of flash loan arbitrage opportunities
        """
        opportunities = []

        price_discrepancies = contract_analysis.get('price_discrepancies', [])

        for discrepancy in price_discrepancies:
            # Even small discrepancies become profitable with flash loans
            if discrepancy.get('discrepancy_percent', 0) > 1.0:  # >1%
                # Simulate flash loan attack
                flash_loan_amounts = [10000, 100000, 1000000]  # USD

                for loan_amount in flash_loan_amounts:
                    profit = self._calculate_flash_loan_profit(
                        loan_amount,
                        discrepancy['contract_price'],
                        discrepancy['market_price']
                    )

                    if profit and profit >= self.min_profit_usd:
                        opportunities.append({
                            'type': 'flash_loan_arbitrage',
                            'loan_amount_usd': loan_amount,
                            'contract_price': discrepancy['contract_price'],
                            'market_price': discrepancy['market_price'],
                            'gross_profit': profit,
                            'flash_loan_fee': loan_amount * 0.0009,  # 0.09% typical fee
                            'net_profit': profit - (loan_amount * 0.0009),
                            'roi_percent': (profit / (loan_amount * 0.0009)) * 100,
                            'execution_steps': [
                                f'1. Flash loan ${loan_amount:,.0f} from Aave/dYdX',
                                f'2. Buy tokens from contract at ${discrepancy["contract_price"]:.4f}',
                                f'3. Sell tokens on DEX at ${discrepancy["market_price"]:.4f}',
                                f'4. Repay flash loan + fee',
                                f'5. Keep profit: ${profit:,.2f}'
                            ],
                            'severity': 'critical' if profit > 10000 else 'high'
                        })

        return opportunities

    def _calculate_flash_loan_profit(
        self,
        loan_amount: float,
        buy_price: float,
        sell_price: float
    ) -> Optional[float]:
        """Calculate profit from flash loan arbitrage."""
        if sell_price <= buy_price:
            return None

        # Calculate how many tokens can be bought
        tokens = loan_amount / buy_price

        # Calculate revenue from selling
        revenue = tokens * sell_price

        # Profit = revenue - loan amount
        profit = revenue - loan_amount

        return profit if profit > 0 else None

    def analyze_contract_for_arbitrage(
        self,
        contract_analysis: Dict,
        dex_prices: List[Dict]
    ) -> Dict:
        """
        Comprehensive arbitrage analysis.

        Args:
            contract_analysis: Economic analysis of contract
            dex_prices: DEX price data

        Returns:
            Complete arbitrage analysis
        """
        opportunities = []

        # Simple arbitrage from price discrepancies
        for discrepancy in contract_analysis.get('price_discrepancies', []):
            simple = self.detect_simple_arbitrage(
                discrepancy['contract_price'],
                discrepancy['market_price']
            )
            if simple:
                opportunities.append(simple)

        # Flash loan arbitrage
        flash_loan_opps = self.detect_flash_loan_arbitrage(
            contract_analysis,
            dex_prices
        )
        opportunities.extend(flash_loan_opps)

        # Triangular arbitrage
        if len(dex_prices) >= 3:
            triangular = self.detect_triangular_arbitrage(dex_prices)
            opportunities.extend(triangular)

        # Calculate total profit potential
        total_profit = sum(
            opp.get('total_profit_usd', 0) or opp.get('net_profit', 0)
            for opp in opportunities
        )

        return {
            'arbitrage_opportunities': opportunities,
            'total_opportunities': len(opportunities),
            'total_profit_potential': total_profit,
            'highest_profit_opportunity': max(
                opportunities,
                key=lambda o: o.get('total_profit_usd', 0) or o.get('net_profit', 0),
                default=None
            ) if opportunities else None,
            'is_profitable': total_profit >= self.min_profit_usd
        }

    def generate_arbitrage_report(
        self,
        analysis: Dict
    ) -> str:
        """
        Generate human-readable arbitrage report.

        Args:
            analysis: Arbitrage analysis results

        Returns:
            Formatted report string
        """
        if not analysis['arbitrage_opportunities']:
            return Panel(
                "[green]No significant arbitrage opportunities detected.[/green]",
                title="Arbitrage Analysis",
                border_style="green"
            )

        report_lines = [
            f"[bold]Total Opportunities:[/bold] {analysis['total_opportunities']}",
            f"[bold]Total Profit Potential:[/bold] ${analysis['total_profit_potential']:,.2f}",
            "",
            "[bold yellow]Top Opportunities:[/bold yellow]"
        ]

        # Sort by profit
        sorted_opps = sorted(
            analysis['arbitrage_opportunities'],
            key=lambda o: o.get('total_profit_usd', 0) or o.get('net_profit', 0),
            reverse=True
        )

        for i, opp in enumerate(sorted_opps[:5], 1):  # Top 5
            profit = opp.get('total_profit_usd', 0) or opp.get('net_profit', 0)
            opp_type = opp.get('type', 'unknown').replace('_', ' ').title()

            report_lines.append(f"\n{i}. {opp_type}")
            report_lines.append(f"   Profit: ${profit:,.2f}")

            if 'execution_steps' in opp:
                report_lines.append("   Steps:")
                for step in opp['execution_steps'][:3]:  # First 3 steps
                    report_lines.append(f"     {step}")

        return Panel(
            "\n".join(report_lines),
            title="[bold red]Arbitrage Opportunities Detected[/bold red]",
            border_style="red"
        )
