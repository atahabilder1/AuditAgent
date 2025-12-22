"""
Local LLM integration module for AI-powered vulnerability analysis.

This module provides interfaces to Ollama for running local LLMs
(specifically Qwen2.5-Coder-32B) for smart contract security analysis.
"""

from .ollama_client import OllamaClient
from .prompts import PromptBuilder
from .response_parser import ResponseParser

__all__ = ['OllamaClient', 'PromptBuilder', 'ResponseParser']
