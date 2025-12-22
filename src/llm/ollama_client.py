"""
Ollama client for local LLM inference.

Provides a wrapper around the Ollama API for running Qwen2.5-Coder-32B
locally on the RTX A6000 GPU.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

try:
    import ollama
except ImportError:
    ollama = None

console = Console()
logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Client for interacting with local Ollama models.

    This client provides methods for vulnerability analysis, exploit generation,
    and fix recommendations using locally-hosted LLMs.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize Ollama client.

        Args:
            config: Configuration dictionary with model settings
        """
        self.config = config or {}
        self.model = self.config.get('model', 'qwen2.5-coder:32b-instruct')
        self.temperature = self.config.get('temperature', 0.1)
        self.num_ctx = self.config.get('num_ctx', 8192)  # Context window
        self.num_gpu = self.config.get('num_gpu', 1)  # Use GPU

        # Check if Ollama is available
        if ollama is None:
            raise ImportError(
                "Ollama package not found. Install with: pip install ollama"
            )

        self._verify_model_available()

    def _verify_model_available(self):
        """Verify that the specified model is available in Ollama."""
        try:
            models = ollama.list()
            model_names = [m['name'] for m in models.get('models', [])]

            if self.model not in model_names:
                console.print(
                    f"[yellow]Warning: Model '{self.model}' not found in Ollama.[/yellow]"
                )
                console.print(
                    f"[yellow]Available models: {', '.join(model_names)}[/yellow]"
                )
                console.print(
                    f"[yellow]Pull the model with: ollama pull {self.model}[/yellow]"
                )
        except Exception as e:
            logger.warning(f"Could not verify Ollama models: {e}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Send a chat request to the LLM.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (overrides default)
            max_tokens: Maximum tokens to generate
            json_mode: Whether to force JSON output format

        Returns:
            Dictionary containing the model's response
        """
        options = {
            'temperature': temperature or self.temperature,
            'num_ctx': self.num_ctx,
            'num_gpu': self.num_gpu,
        }

        if max_tokens:
            options['num_predict'] = max_tokens

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True
            ) as progress:
                progress.add_task(description="Analyzing with LLM...", total=None)

                response = ollama.chat(
                    model=self.model,
                    messages=messages,
                    options=options,
                    format='json' if json_mode else ''
                )

            return {
                'success': True,
                'content': response['message']['content'],
                'model': response['model'],
                'total_duration': response.get('total_duration', 0),
                'load_duration': response.get('load_duration', 0),
                'prompt_eval_count': response.get('prompt_eval_count', 0),
                'eval_count': response.get('eval_count', 0),
            }

        except Exception as e:
            logger.error(f"Ollama chat failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': None
            }

    def analyze_vulnerability(
        self,
        contract_code: str,
        slither_findings: List[Dict],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze contract for vulnerabilities using LLM.

        Args:
            contract_code: Solidity source code
            slither_findings: Findings from Slither analysis
            context: Additional context about the contract

        Returns:
            Dictionary with vulnerability analysis
        """
        from .prompts import PromptBuilder

        prompt = PromptBuilder.vulnerability_analysis_prompt(
            contract_code, slither_findings, context
        )

        messages = [
            {
                'role': 'system',
                'content': 'You are an expert smart contract security auditor. '
                          'Analyze contracts for vulnerabilities and provide detailed findings.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        return self.chat(messages, json_mode=True)

    def generate_exploit(
        self,
        contract_code: str,
        vulnerability: Dict,
        chain: str = 'bsc'
    ) -> Dict[str, Any]:
        """
        Generate exploit code for a detected vulnerability.

        Args:
            contract_code: Target contract source code
            vulnerability: Vulnerability details
            chain: Target blockchain (for correct interfaces)

        Returns:
            Dictionary with exploit code and explanation
        """
        from .prompts import PromptBuilder

        prompt = PromptBuilder.exploit_generation_prompt(
            contract_code, vulnerability, chain
        )

        messages = [
            {
                'role': 'system',
                'content': 'You are an expert in smart contract security and exploit development. '
                          'Generate working Solidity exploit code for educational and defensive purposes.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        return self.chat(messages, temperature=0.2, max_tokens=4096)

    def suggest_fix(
        self,
        contract_code: str,
        vulnerability: Dict
    ) -> Dict[str, Any]:
        """
        Generate fix recommendations for a vulnerability.

        Args:
            contract_code: Vulnerable contract code
            vulnerability: Vulnerability details

        Returns:
            Dictionary with fix suggestions and patched code
        """
        from .prompts import PromptBuilder

        prompt = PromptBuilder.fix_suggestion_prompt(contract_code, vulnerability)

        messages = [
            {
                'role': 'system',
                'content': 'You are an expert smart contract developer. '
                          'Provide secure code fixes for vulnerabilities.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        return self.chat(messages, json_mode=True)

    def analyze_economic_vulnerability(
        self,
        contract_code: str,
        price_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze contract for economic vulnerabilities using price data.

        Args:
            contract_code: Contract source code
            price_data: Price information from DEX analysis

        Returns:
            Dictionary with economic vulnerability analysis
        """
        from .prompts import PromptBuilder

        prompt = PromptBuilder.economic_analysis_prompt(contract_code, price_data)

        messages = [
            {
                'role': 'system',
                'content': 'You are an expert in DeFi economics and smart contract security. '
                          'Identify economic exploits like arbitrage opportunities and price manipulation.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        return self.chat(messages, json_mode=True)

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.

        Returns:
            Dictionary with model information
        """
        try:
            models = ollama.list()
            for model in models.get('models', []):
                if model['name'] == self.model:
                    return {
                        'success': True,
                        'model': model
                    }

            return {
                'success': False,
                'error': f'Model {self.model} not found'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
