"""
Blockchain forker using Anvil.

Creates isolated forks of live blockchains for safe exploit testing.
"""

import subprocess
import time
import logging
import signal
from typing import Optional, Dict
from pathlib import Path
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class ChainForker:
    """
    Manages blockchain forks using Anvil (from Foundry).

    Creates isolated environments for testing exploits without
    affecting the real blockchain.
    """

    DEFAULT_RPC_URLS = {
        'ethereum': 'https://eth.llamarpc.com',
        'bsc': 'https://bsc-dataseed.binance.org',
        'polygon': 'https://polygon-rpc.com',
        'arbitrum': 'https://arb1.arbitrum.io/rpc',
        'optimism': 'https://mainnet.optimism.io',
    }

    def __init__(self, chain: str = 'bsc', rpc_url: Optional[str] = None):
        """
        Initialize chain forker.

        Args:
            chain: Blockchain to fork ('ethereum', 'bsc', etc.)
            rpc_url: Optional custom RPC URL
        """
        self.chain = chain.lower()
        self.rpc_url = rpc_url or self.DEFAULT_RPC_URLS.get(self.chain)

        if not self.rpc_url:
            raise ValueError(f"No RPC URL for chain: {chain}")

        self.anvil_process = None
        self.fork_url = None
        self.fork_block = None

    def fork_at_block(
        self,
        block_number: Optional[int] = None,
        port: int = 8545,
        host: str = '127.0.0.1'
    ) -> Dict[str, any]:
        """
        Fork blockchain at specific block using Anvil.

        Args:
            block_number: Block number to fork at (None = latest)
            port: Local port for Anvil
            host: Local host address

        Returns:
            Dictionary with fork information
        """
        console.print(f"[yellow]Forking {self.chain} at block {block_number or 'latest'}...[/yellow]")

        # Build Anvil command
        cmd = [
            'anvil',
            '--fork-url', self.rpc_url,
            '--host', host,
            '--port', str(port),
            '--no-rate-limit'
        ]

        if block_number:
            cmd.extend(['--fork-block-number', str(block_number)])
            self.fork_block = block_number

        try:
            # Start Anvil process
            self.anvil_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # Wait for Anvil to start
            time.sleep(3)

            # Check if process is running
            if self.anvil_process.poll() is not None:
                stdout, stderr = self.anvil_process.communicate()
                raise RuntimeError(f"Anvil failed to start:\n{stderr}")

            self.fork_url = f"http://{host}:{port}"

            console.print(f"[green]Fork created successfully at {self.fork_url}[/green]")

            return {
                'success': True,
                'fork_url': self.fork_url,
                'chain': self.chain,
                'block_number': self.fork_block,
                'process_pid': self.anvil_process.pid
            }

        except FileNotFoundError:
            console.print("[red]Anvil not found! Install Foundry:[/red]")
            console.print("curl -L https://foundry.paradigm.xyz | bash && foundryup")
            raise
        except Exception as e:
            logger.error(f"Failed to fork chain: {e}")
            if self.anvil_process:
                self.stop_fork()
            raise

    def stop_fork(self):
        """Stop the Anvil fork process."""
        if self.anvil_process:
            try:
                self.anvil_process.send_signal(signal.SIGTERM)
                self.anvil_process.wait(timeout=5)
                console.print("[green]Fork stopped successfully[/green]")
            except subprocess.TimeoutExpired:
                self.anvil_process.kill()
                console.print("[yellow]Fork process killed (timeout)[/yellow]")
            except Exception as e:
                logger.error(f"Error stopping fork: {e}")

            self.anvil_process = None
            self.fork_url = None

    def is_running(self) -> bool:
        """
        Check if fork is still running.

        Returns:
            True if Anvil process is running
        """
        if not self.anvil_process:
            return False

        return self.anvil_process.poll() is None

    def get_fork_info(self) -> Optional[Dict]:
        """
        Get information about the current fork.

        Returns:
            Fork information or None
        """
        if not self.is_running():
            return None

        return {
            'fork_url': self.fork_url,
            'chain': self.chain,
            'block_number': self.fork_block,
            'process_pid': self.anvil_process.pid,
            'is_running': True
        }

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup."""
        self.stop_fork()

    def __del__(self):
        """Destructor - ensure fork is stopped."""
        self.stop_fork()
