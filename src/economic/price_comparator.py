"""
Price comparator for detecting economic vulnerabilities.

Compares contract internal prices with DEX market prices to identify
arbitrage opportunities and price manipulation vulnerabilities.
"""

import logging
import re
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from rich.console import Console
from rich.table import Table

console = Console()
logger = logging.getLogger(__name__)


class PriceComparator:
    """
    Compares contract prices with market prices for arbitrage detection.

    This is a NOVEL contribution: detecting economic exploits by comparing
    hardcoded or calculated prices in smart contracts against real DEX prices.
    """

    # Threshold for flagging price discrepancy (10% by default)
    DEFAULT_THRESHOLD = 0.10  # 10%

    def __init__(self, threshold: float = DEFAULT_THRESHOLD):
        """
        Initialize price comparator.

        Args:
            threshold: Price discrepancy threshold (0.10 = 10%)
        """
        self.threshold = threshold

    def extract_prices_from_contract(self, contract_code: str) -> List[Dict]:
        """
        Extract hardcoded prices from contract source code.

        Args:
            contract_code: Solidity source code

        Returns:
            List of extracted price information
        """
        prices = []

        # Pattern 1: Direct price assignments (e.g., price = 5 * 10**18)
        price_patterns = [
            r'price\s*=\s*(\d+)\s*\*\s*10\*\*(\d+)',  # price = 5 * 10**18
            r'price\s*=\s*(\d+)e(\d+)',  # price = 5e18
            r'rate\s*=\s*(\d+)',  # rate = 1000
            r'exchangeRate\s*=\s*(\d+)',  # exchangeRate = 1000
        ]

        for pattern in price_patterns:
            matches = re.finditer(pattern, contract_code, re.IGNORECASE)
            for match in matches:
                try:
                    if len(match.groups()) == 2:
                        base = int(match.group(1))
                        exp = int(match.group(2))
                        value = base * (10 ** exp)
                    else:
                        value = int(match.group(1))

                    prices.append({
                        'type': 'hardcoded_price',
                        'value': value,
                        'context': match.group(0),
                        'line': contract_code[:match.start()].count('\n') + 1
                    })
                except (ValueError, IndexError) as e:
                    logger.debug(f"Failed to parse price: {e}")

        # Pattern 2: Token sale prices
        sale_patterns = [
            r'tokenPrice\s*=\s*(\d+)',
            r'salePrice\s*=\s*(\d+)',
            r'buyPrice\s*=\s*(\d+)',
            r'sellPrice\s*=\s*(\d+)',
        ]

        for pattern in sale_patterns:
            matches = re.finditer(pattern, contract_code, re.IGNORECASE)
            for match in matches:
                try:
                    value = int(match.group(1))
                    prices.append({
                        'type': 'sale_price',
                        'value': value,
                        'context': match.group(0),
                        'line': contract_code[:match.start()].count('\n') + 1
                    })
                except ValueError:
                    pass

        # Pattern 3: Liquidity pool ratios
        ratio_patterns = [
            r'reserveA\s*=\s*(\d+)',
            r'reserveB\s*=\s*(\d+)',
        ]

        reserves = {}
        for pattern in ratio_patterns:
            matches = re.finditer(pattern, contract_code, re.IGNORECASE)
            for match in matches:
                try:
                    token_name = 'A' if 'A' in match.group(0) else 'B'
                    reserves[token_name] = int(match.group(1))
                except ValueError:
                    pass

        if 'A' in reserves and 'B' in reserves:
            prices.append({
                'type': 'pool_ratio',
                'value': reserves['B'] / reserves['A'] if reserves['A'] > 0 else 0,
                'context': f"reserveA={reserves['A']}, reserveB={reserves['B']}",
                'reserves': reserves
            })

        return prices

    def compare_prices(
        self,
        contract_prices: List[Dict],
        market_prices: List[Dict]
    ) -> List[Dict]:
        """
        Compare contract prices with market prices.

        Args:
            contract_prices: Prices extracted from contract
            market_prices: Prices fetched from DEX

        Returns:
            List of price discrepancies and arbitrage opportunities
        """
        discrepancies = []

        if not market_prices:
            logger.warning("No market prices available for comparison")
            return discrepancies

        # Use average market price
        avg_market_price = sum(p['price_usd'] for p in market_prices) / len(market_prices)

        for contract_price in contract_prices:
            contract_value = contract_price['value']

            # Convert contract value to comparable format
            # Assuming most prices are in wei (18 decimals)
            contract_usd = float(contract_value) / 1e18

            # Calculate discrepancy
            if avg_market_price > 0:
                discrepancy_pct = abs(contract_usd - avg_market_price) / avg_market_price

                if discrepancy_pct > self.threshold:
                    profit_potential = abs(contract_usd - avg_market_price)

                    discrepancy = {
                        'contract_price': contract_usd,
                        'market_price': avg_market_price,
                        'discrepancy_percent': discrepancy_pct * 100,
                        'profit_potential_usd': profit_potential,
                        'is_exploitable': discrepancy_pct > 0.05,  # >5% is likely exploitable
                        'severity': self._calculate_severity(discrepancy_pct),
                        'type': contract_price['type'],
                        'context': contract_price.get('context', ''),
                        'line': contract_price.get('line', 0),
                        'market_data': market_prices
                    }

                    discrepancies.append(discrepancy)

        return discrepancies

    def _calculate_severity(self, discrepancy_pct: float) -> str:
        """
        Calculate severity based on price discrepancy.

        Args:
            discrepancy_pct: Discrepancy percentage (0.0-1.0)

        Returns:
            Severity level
        """
        if discrepancy_pct > 0.50:  # >50%
            return 'critical'
        elif discrepancy_pct > 0.25:  # >25%
            return 'high'
        elif discrepancy_pct > 0.10:  # >10%
            return 'medium'
        else:
            return 'low'

    def analyze_contract_for_economic_exploits(
        self,
        contract_code: str,
        token_address: Optional[str],
        dex_prices: List[Dict]
    ) -> Dict:
        """
        Comprehensive economic analysis of a contract.

        Args:
            contract_code: Solidity source code
            token_address: Token contract address
            dex_prices: DEX price data

        Returns:
            Complete economic analysis
        """
        # Extract contract prices
        contract_prices = self.extract_prices_from_contract(contract_code)

        # Compare with market
        discrepancies = self.compare_prices(contract_prices, dex_prices)

        # Look for specific economic vulnerability patterns
        patterns = self._detect_economic_patterns(contract_code)

        # Calculate total profit potential
        total_profit = sum(d['profit_potential_usd'] for d in discrepancies)

        analysis = {
            'has_economic_vulnerabilities': len(discrepancies) > 0,
            'price_discrepancies': discrepancies,
            'contract_prices_found': len(contract_prices),
            'market_prices_available': len(dex_prices),
            'total_profit_potential_usd': total_profit,
            'vulnerability_patterns': patterns,
            'highest_severity': self._get_highest_severity(discrepancies),
            'exploitable_count': sum(1 for d in discrepancies if d['is_exploitable'])
        }

        return analysis

    def _detect_economic_patterns(self, contract_code: str) -> List[Dict]:
        """
        Detect common economic vulnerability patterns.

        Args:
            contract_code: Solidity source code

        Returns:
            List of detected patterns
        """
        patterns = []

        # Pattern 1: Fixed price oracle (dangerous!)
        if re.search(r'function\s+getPrice.*?returns.*?{\s*return\s+\d+', contract_code, re.DOTALL):
            patterns.append({
                'type': 'fixed_price_oracle',
                'severity': 'high',
                'description': 'Contract uses fixed price oracle, vulnerable to market price changes'
            })

        # Pattern 2: No slippage protection
        if 'swap' in contract_code.lower() and 'slippage' not in contract_code.lower():
            patterns.append({
                'type': 'no_slippage_protection',
                'severity': 'medium',
                'description': 'Swap functionality without slippage protection'
            })

        # Pattern 3: Flash loan vulnerable
        if 'transfer' in contract_code and 'balanceOf' in contract_code:
            if 'nonReentrant' not in contract_code and 'ReentrancyGuard' not in contract_code:
                patterns.append({
                    'type': 'flash_loan_vulnerable',
                    'severity': 'high',
                    'description': 'Potential flash loan attack vector without reentrancy protection'
                })

        # Pattern 4: Price calculation based on reserves
        if re.search(r'price\s*=\s*reserve\w+\s*/\s*reserve\w+', contract_code):
            patterns.append({
                'type': 'reserve_based_pricing',
                'severity': 'medium',
                'description': 'Price calculated from reserves, manipulable with large trades'
            })

        return patterns

    def _get_highest_severity(self, discrepancies: List[Dict]) -> str:
        """Get highest severity level from discrepancies."""
        if not discrepancies:
            return 'none'

        severity_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'none': 0}
        highest = max(discrepancies, key=lambda d: severity_order.get(d['severity'], 0))
        return highest['severity']

    def generate_price_comparison_table(
        self,
        discrepancies: List[Dict]
    ) -> Table:
        """
        Generate rich table for price comparison visualization.

        Args:
            discrepancies: List of price discrepancies

        Returns:
            Rich Table object
        """
        table = Table(title="Price Discrepancy Analysis")

        table.add_column("Type", style="cyan")
        table.add_column("Contract Price", style="magenta")
        table.add_column("Market Price", style="green")
        table.add_column("Discrepancy", style="yellow")
        table.add_column("Profit Potential", style="red")
        table.add_column("Severity", style="bold")

        for disc in discrepancies:
            severity_color = {
                'critical': 'bold red',
                'high': 'red',
                'medium': 'yellow',
                'low': 'white'
            }.get(disc['severity'], 'white')

            table.add_row(
                disc['type'],
                f"${disc['contract_price']:.4f}",
                f"${disc['market_price']:.4f}",
                f"{disc['discrepancy_percent']:.2f}%",
                f"${disc['profit_potential_usd']:.2f}",
                f"[{severity_color}]{disc['severity'].upper()}[/{severity_color}]"
            )

        return table
