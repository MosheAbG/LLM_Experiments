"""
Configuration module for the financial summarization application.

This module manages environment variables, API settings, and application defaults.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class OpenAIConfig:
    """Configuration for OpenAI API."""
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: int = 30


@dataclass
class WebsiteConfig:
    """Configuration for website scraping."""
    timeout: int = 10
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"


@dataclass
class AppConfig:
    """Main application configuration."""
    openai: OpenAIConfig
    website: WebsiteConfig
    debug: bool = False
    log_level: str = "INFO"


def load_config() -> AppConfig:
    """
    Load configuration from environment variables and defaults.
    
    Returns:
        AppConfig: Application configuration object.
        
    Raises:
        ValueError: If required environment variables are missing.
    """
    # Check for required API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set in the environment variables. "
            "Please set it in your .env file or as an environment variable."
        )
    
    # Load optional configurations from environment
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    openai_config = OpenAIConfig(
        model=model,
        temperature=temperature
    )
    
    website_config = WebsiteConfig()
    
    return AppConfig(
        openai=openai_config,
        website=website_config,
        debug=debug,
        log_level=log_level
    )
