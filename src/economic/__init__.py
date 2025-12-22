"""
Economic vulnerability analysis module.

This module implements the NOVEL contribution: detecting economic exploits
by comparing contract prices with DEX market prices to find arbitrage
opportunities and price manipulation vulnerabilities.
"""

from .dex_price_fetcher import DEXPriceFetcher
from .price_comparator import PriceComparator
from .arbitrage_detector import ArbitrageDetector

__all__ = ['DEXPriceFetcher', 'PriceComparator', 'ArbitrageDetector']
