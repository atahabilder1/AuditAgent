"""
DEX price fetcher for economic vulnerability analysis.

Fetches real-time prices from decentralized exchanges (PancakeSwap, Uniswap)
to compare against contract internal prices for arbitrage detection.
"""

import logging
from typing import Dict, Optional, List, Tuple
from decimal import Decimal
from web3 import Web3
from web3.contract import Contract
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class DEXPriceFetcher:
    """
    Fetches token prices from DEXes for economic analysis.

    Supports PancakeSwap V2 (BSC), Uniswap V2/V3 (Ethereum), and other forks.
    """

    # DEX Factory addresses
    FACTORIES = {
        'bsc': {
            'pancakeswap_v2': '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73',
            'pancakeswap_v3': '0x0BFbCF9fa4f9C56B0F40a671Ad40E0805A091865',
        },
        'ethereum': {
            'uniswap_v2': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
            'uniswap_v3': '0x1F98431c8aD98523631AE4a59f267346ea31F984',
        },
        'polygon': {
            'quickswap': '0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32',
        }
    }

    # Common stablecoin addresses
    STABLECOINS = {
        'bsc': {
            'USDT': '0x55d398326f99059fF775485246999027B3197955',
            'USDC': '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d',
            'BUSD': '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56',
        },
        'ethereum': {
            'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
            'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
            'DAI': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
        }
    }

    # Wrapped native tokens
    WNATIVE = {
        'bsc': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',  # WBNB
        'ethereum': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',  # WETH
        'polygon': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',  # WMATIC
    }

    # PancakeSwap V2 Pair ABI (minimal)
    PAIR_ABI = [
        {
            'constant': True,
            'inputs': [],
            'name': 'getReserves',
            'outputs': [
                {'name': 'reserve0', 'type': 'uint112'},
                {'name': 'reserve1', 'type': 'uint112'},
                {'name': 'blockTimestampLast', 'type': 'uint32'}
            ],
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'token0',
            'outputs': [{'name': '', 'type': 'address'}],
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'token1',
            'outputs': [{'name': '', 'type': 'address'}],
            'type': 'function'
        }
    ]

    # Factory ABI (minimal)
    FACTORY_ABI = [
        {
            'constant': True,
            'inputs': [
                {'name': 'tokenA', 'type': 'address'},
                {'name': 'tokenB', 'type': 'address'}
            ],
            'name': 'getPair',
            'outputs': [{'name': 'pair', 'type': 'address'}],
            'type': 'function'
        }
    ]

    def __init__(self, chain: str = 'bsc', rpc_url: Optional[str] = None):
        """
        Initialize DEX price fetcher.

        Args:
            chain: Blockchain network ('bsc', 'ethereum', 'polygon')
            rpc_url: Optional custom RPC URL
        """
        self.chain = chain.lower()

        # Default RPC URLs
        default_rpcs = {
            'bsc': 'https://bsc-dataseed.binance.org',
            'ethereum': 'https://eth.llamarpc.com',
            'polygon': 'https://polygon-rpc.com',
        }

        rpc = rpc_url or default_rpcs.get(self.chain)
        if not rpc:
            raise ValueError(f"Unsupported chain: {chain}")

        try:
            self.w3 = Web3(Web3.HTTPProvider(rpc))
            if not self.w3.is_connected():
                raise ConnectionError(f"Failed to connect to {chain} RPC")
        except Exception as e:
            logger.error(f"Web3 connection failed: {e}")
            raise

        console.print(f"[green]Connected to {chain.upper()} network[/green]")

    def get_token_price_in_usd(
        self,
        token_address: str,
        dex: str = 'pancakeswap_v2'
    ) -> Optional[Dict[str, any]]:
        """
        Get token price in USD from DEX.

        Args:
            token_address: Token contract address
            dex: DEX name (e.g., 'pancakeswap_v2', 'uniswap_v2')

        Returns:
            Dictionary with price information or None if not found
        """
        token_address = Web3.to_checksum_address(token_address)

        # Try to get price against each stablecoin
        stablecoins = self.STABLECOINS.get(self.chain, {})

        for stable_name, stable_address in stablecoins.items():
            try:
                price = self._get_price_from_pair(
                    token_address,
                    stable_address,
                    dex
                )
                if price:
                    return {
                        'price_usd': float(price),
                        'pair_token': stable_name,
                        'dex': dex,
                        'chain': self.chain,
                        'token_address': token_address
                    }
            except Exception as e:
                logger.debug(f"Failed to get {stable_name} price: {e}")
                continue

        # Try native token (BNB/ETH) route
        try:
            native_price = self._get_price_via_native(token_address, dex)
            if native_price:
                return native_price
        except Exception as e:
            logger.debug(f"Failed to get native token price: {e}")

        return None

    def _get_price_from_pair(
        self,
        token_a: str,
        token_b: str,
        dex: str
    ) -> Optional[Decimal]:
        """
        Get price of token_a in terms of token_b from DEX pair.

        Args:
            token_a: First token address
            token_b: Second token address
            dex: DEX name

        Returns:
            Price as Decimal or None
        """
        # Get factory address
        factory_address = self.FACTORIES.get(self.chain, {}).get(dex)
        if not factory_address:
            raise ValueError(f"DEX {dex} not supported on {self.chain}")

        factory_address = Web3.to_checksum_address(factory_address)
        factory = self.w3.eth.contract(
            address=factory_address,
            abi=self.FACTORY_ABI
        )

        # Get pair address
        pair_address = factory.functions.getPair(
            Web3.to_checksum_address(token_a),
            Web3.to_checksum_address(token_b)
        ).call()

        if pair_address == '0x0000000000000000000000000000000000000000':
            return None

        # Get reserves
        pair = self.w3.eth.contract(
            address=pair_address,
            abi=self.PAIR_ABI
        )

        reserves = pair.functions.getReserves().call()
        reserve0 = Decimal(reserves[0])
        reserve1 = Decimal(reserves[1])

        # Determine token order
        token0 = pair.functions.token0().call()

        if Web3.to_checksum_address(token_a) == token0:
            # token_a is token0, so price = reserve1 / reserve0
            price = reserve1 / reserve0 if reserve0 > 0 else Decimal(0)
        else:
            # token_a is token1, so price = reserve0 / reserve1
            price = reserve0 / reserve1 if reserve1 > 0 else Decimal(0)

        return price

    def _get_price_via_native(
        self,
        token_address: str,
        dex: str
    ) -> Optional[Dict[str, any]]:
        """
        Get token price by routing through native token (BNB/ETH).

        Args:
            token_address: Token to price
            dex: DEX name

        Returns:
            Price information dictionary
        """
        wnative = self.WNATIVE.get(self.chain)
        if not wnative:
            return None

        # Get token price in native currency
        token_per_native = self._get_price_from_pair(token_address, wnative, dex)
        if not token_per_native:
            return None

        # Get native currency price in USD
        stablecoins = self.STABLECOINS.get(self.chain, {})
        for stable_name, stable_address in stablecoins.items():
            native_usd_price = self._get_price_from_pair(wnative, stable_address, dex)
            if native_usd_price:
                usd_price = float(token_per_native * native_usd_price)
                return {
                    'price_usd': usd_price,
                    'pair_token': f'{stable_name} (via native)',
                    'dex': dex,
                    'chain': self.chain,
                    'token_address': token_address,
                    'route': f'{token_address} -> {wnative} -> {stable_address}'
                }

        return None

    def get_prices_from_multiple_dexes(
        self,
        token_address: str
    ) -> List[Dict[str, any]]:
        """
        Get token prices from all available DEXes on the chain.

        Args:
            token_address: Token contract address

        Returns:
            List of price dictionaries from different DEXes
        """
        prices = []
        dexes = self.FACTORIES.get(self.chain, {}).keys()

        for dex in dexes:
            try:
                price_data = self.get_token_price_in_usd(token_address, dex)
                if price_data:
                    prices.append(price_data)
            except Exception as e:
                logger.debug(f"Failed to get price from {dex}: {e}")

        return prices

    def get_pair_reserves(
        self,
        token_a: str,
        token_b: str,
        dex: str = 'pancakeswap_v2'
    ) -> Optional[Tuple[int, int]]:
        """
        Get reserves for a token pair.

        Args:
            token_a: First token address
            token_b: Second token address
            dex: DEX name

        Returns:
            Tuple of (reserve_a, reserve_b) or None
        """
        try:
            factory_address = self.FACTORIES.get(self.chain, {}).get(dex)
            if not factory_address:
                return None

            factory = self.w3.eth.contract(
                address=Web3.to_checksum_address(factory_address),
                abi=self.FACTORY_ABI
            )

            pair_address = factory.functions.getPair(
                Web3.to_checksum_address(token_a),
                Web3.to_checksum_address(token_b)
            ).call()

            if pair_address == '0x0000000000000000000000000000000000000000':
                return None

            pair = self.w3.eth.contract(
                address=pair_address,
                abi=self.PAIR_ABI
            )

            reserves = pair.functions.getReserves().call()
            token0 = pair.functions.token0().call()

            if Web3.to_checksum_address(token_a) == token0:
                return (reserves[0], reserves[1])
            else:
                return (reserves[1], reserves[0])

        except Exception as e:
            logger.error(f"Failed to get reserves: {e}")
            return None
