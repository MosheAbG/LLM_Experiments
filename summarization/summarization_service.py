"""
Summarization service module for processing articles and content.
"""

import logging
from typing import Optional
from util import Website
from api_client import FinancialAnalystClient


class FinancialSummarizationService:
    """Service for summarizing financial content."""
    
    def __init__(self, api_client: FinancialAnalystClient, logger: logging.Logger):
        """
        Initialize the summarization service.
        
        Args:
            api_client: OpenAI API client instance.
            logger: Logger instance.
        """
        self.api_client = api_client
        self.logger = logger
    
    def summarize_article_from_url(
        self,
        article_url: str,
        analysis_type: str = "summary"
    ) -> Optional[str]:
        """
        Fetch an article from a URL and summarize it.
        
        Args:
            article_url: URL of the article to summarize.
            analysis_type: Type of analysis to perform.
            
        Returns:
            str: Summarized content, or None if processing fails.
        """
        try:
            self.logger.info(f"Starting article summarization from URL: {article_url}")
            
            # Extract content from website
            website = Website(article_url)
            content = website.extract_content()
            
            if not content or content.strip() == "":
                self.logger.error("Failed to extract content from the URL")
                return None
            
            self.logger.debug(f"Successfully extracted {len(content)} characters from article")
            
            # Analyze the content
            result = self.api_client.summarize_content(content, analysis_type)
            
            if result:
                self.logger.info(f"Successfully completed {analysis_type} analysis")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error summarizing article: {str(e)}")
            return None
    
    def summarize_text(
        self,
        text: str,
        analysis_type: str = "summary"
    ) -> Optional[str]:
        """
        Summarize provided text content.
        
        Args:
            text: The text content to summarize.
            analysis_type: Type of analysis to perform.
            
        Returns:
            str: Analysis result, or None if processing fails.
        """
        try:
            self.logger.info(f"Performing {analysis_type} analysis on provided text")
            
            if not text or text.strip() == "":
                self.logger.error("No text provided for analysis")
                return None
            
            result = self.api_client.summarize_content(text, analysis_type)
            
            if result:
                self.logger.info(f"Successfully completed {analysis_type} analysis")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error summarizing text: {str(e)}")
            return None
    
    def get_analysis_types(self) -> list[str]:
        """
        Get available analysis types.
        
        Returns:
            list: Available analysis types.
        """
        return ["summary", "key_points", "action_items", "risks"]
