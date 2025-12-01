"""
Logging configuration module for the financial summarization application.
"""

import logging
import sys
from typing import Optional


def setup_logging(log_level: str = "INFO", debug: bool = False) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        debug: If True, adds more verbose logging.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("financial_summarizer")
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Format
    if debug:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    else:
        format_string = "%(asctime)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
