"""
Etherscan API integration for fetching verified contract source code.

Supports multiple chains: Ethereum, BSC, Polygon, Arbitrum, Optimism, etc.
"""

import os
import requests
import time
from typing import Dict, Optional, List
from pathlib import Path


class EtherscanFetcher:
    """
    Fetches verified contract source code from Etherscan and similar explorers.
    """

    # API endpoints for different chains
    ENDPOINTS = {
        'ethereum': 'https://api.etherscan.io/api',
        'goerli': 'https://api-goerli.etherscan.io/api',
        'sepolia': 'https://api-sepolia.etherscan.io/api',
        'bsc': 'https://api.bscscan.com/api',
        'bsc_testnet': 'https://api-testnet.bscscan.com/api',
        'polygon': 'https://api.polygonscan.com/api',
        'polygon_mumbai': 'https://api-testnet.polygonscan.com/api',
        'arbitrum': 'https://api.arbiscan.io/api',
        'optimism': 'https://api-optimistic.etherscan.io/api',
        'avalanche': 'https://api.snowtrace.io/api',
        'fantom': 'https://api.ftmscan.com/api',
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Etherscan fetcher.

        Args:
            api_key: Etherscan API key (or set ETHERSCAN_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv('ETHERSCAN_API_KEY')
        if not self.api_key:
            print("Warning: No Etherscan API key provided. Rate limits will be strict.")
            print("Get a free key at: https://etherscan.io/myapikey")
            self.api_key = "YourApiKeyToken"  # Free tier default

    def fetch_contract(
        self,
        address: str,
        chain: str = 'ethereum',
        save_to: Optional[str] = None
    ) -> Dict:
        """
        Fetch verified contract source code from blockchain explorer.

        Args:
            address: Contract address (0x...)
            chain: Blockchain name (ethereum, bsc, polygon, etc.)
            save_to: Optional path to save contract file

        Returns:
            Dictionary with contract data including source code

        Raises:
            ValueError: If chain is not supported
            Exception: If contract is not verified or fetch fails
        """
        if chain not in self.ENDPOINTS:
            raise ValueError(
                f"Unsupported chain: {chain}. "
                f"Supported: {', '.join(self.ENDPOINTS.keys())}"
            )

        # Validate address format
        if not address.startswith('0x') or len(address) != 42:
            raise ValueError(f"Invalid contract address format: {address}")

        endpoint = self.ENDPOINTS[chain]

        print(f"Fetching contract from {chain}: {address}")

        # Fetch contract source code
        params = {
            'module': 'contract',
            'action': 'getsourcecode',
            'address': address,
            'apikey': self.api_key
        }

        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data['status'] != '1':
                raise Exception(f"API Error: {data.get('result', 'Unknown error')}")

            result = data['result'][0]

            # Check if contract is verified
            if result['SourceCode'] == '':
                raise Exception(
                    f"Contract at {address} is not verified on {chain}. "
                    "Only verified contracts can be audited."
                )

            # Parse contract data
            contract_data = {
                'address': address,
                'chain': chain,
                'name': result['ContractName'],
                'compiler': result['CompilerVersion'],
                'optimization': result['OptimizationUsed'] == '1',
                'runs': result.get('Runs', 200),
                'source_code': result['SourceCode'],
                'abi': result['ABI'],
                'constructor_arguments': result.get('ConstructorArguments', ''),
                'evm_version': result.get('EVMVersion', 'default'),
                'license': result.get('LicenseType', 'None'),
            }

            # Handle multi-file contracts (JSON format)
            source_code = contract_data['source_code']
            if source_code.startswith('{{'):
                # Multi-file contract, extract main contract
                import json
                # Remove extra braces
                source_json = source_code[1:-1]
                sources = json.loads(source_json)

                # Find main contract file
                main_file = None
                for file_path, file_data in sources.get('sources', {}).items():
                    if contract_data['name'] in file_data.get('content', ''):
                        main_file = file_data['content']
                        contract_data['is_multifile'] = True
                        contract_data['all_sources'] = sources
                        break

                if main_file:
                    contract_data['source_code'] = main_file
                else:
                    # Use first file
                    contract_data['source_code'] = list(
                        sources.get('sources', {}).values()
                    )[0]['content']

            # Save to file if requested
            if save_to:
                self._save_contract(contract_data, save_to)

            print(f"✓ Successfully fetched {contract_data['name']}")
            print(f"  Compiler: {contract_data['compiler']}")
            print(f"  License: {contract_data['license']}")

            return contract_data

        except requests.RequestException as e:
            raise Exception(f"Network error fetching contract: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching contract: {str(e)}")

    def fetch_multiple_contracts(
        self,
        addresses: List[str],
        chain: str = 'ethereum',
        save_dir: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch multiple contracts from blockchain.

        Args:
            addresses: List of contract addresses
            chain: Blockchain name
            save_dir: Optional directory to save contracts

        Returns:
            List of contract data dictionaries
        """
        contracts = []

        for i, address in enumerate(addresses, 1):
            print(f"\n[{i}/{len(addresses)}] Fetching {address}...")

            try:
                save_path = None
                if save_dir:
                    save_path = f"{save_dir}/contract_{i}.sol"

                contract = self.fetch_contract(address, chain, save_path)
                contracts.append(contract)

                # Rate limiting - free tier allows 5 req/sec
                if i < len(addresses):
                    time.sleep(0.2)

            except Exception as e:
                print(f"✗ Failed to fetch {address}: {str(e)}")
                contracts.append({
                    'address': address,
                    'error': str(e)
                })

        return contracts

    def _save_contract(self, contract_data: Dict, save_path: str):
        """
        Save contract source code to file.

        Args:
            contract_data: Contract data dictionary
            save_path: Path to save the contract
        """
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Create header comment with metadata
        header = f"""// Contract: {contract_data['name']}
// Address: {contract_data['address']}
// Chain: {contract_data['chain']}
// Compiler: {contract_data['compiler']}
// License: {contract_data['license']}
// Fetched: {time.strftime('%Y-%m-%d %H:%M:%S')}

"""

        with open(path, 'w') as f:
            f.write(header + contract_data['source_code'])

        print(f"  Saved to: {save_path}")

    def get_contract_info(self, address: str, chain: str = 'ethereum') -> Dict:
        """
        Get basic contract information without full source code.

        Args:
            address: Contract address
            chain: Blockchain name

        Returns:
            Basic contract information
        """
        endpoint = self.ENDPOINTS.get(chain)
        if not endpoint:
            raise ValueError(f"Unsupported chain: {chain}")

        params = {
            'module': 'contract',
            'action': 'getsourcecode',
            'address': address,
            'apikey': self.api_key
        }

        response = requests.get(endpoint, params=params, timeout=30)
        data = response.json()

        if data['status'] != '1':
            raise Exception(f"API Error: {data.get('result', 'Unknown error')}")

        result = data['result'][0]

        return {
            'address': address,
            'name': result['ContractName'],
            'compiler': result['CompilerVersion'],
            'is_verified': result['SourceCode'] != '',
            'optimization': result['OptimizationUsed'] == '1',
            'license': result.get('LicenseType', 'None'),
        }

    @staticmethod
    def is_valid_address(address: str) -> bool:
        """
        Validate Ethereum address format.

        Args:
            address: Address to validate

        Returns:
            True if valid format
        """
        if not isinstance(address, str):
            return False
        if not address.startswith('0x'):
            return False
        if len(address) != 42:
            return False
        try:
            int(address, 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_supported_chains() -> List[str]:
        """Get list of supported blockchain networks."""
        return list(EtherscanFetcher.ENDPOINTS.keys())
