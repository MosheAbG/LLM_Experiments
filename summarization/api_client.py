"""
API client module for OpenAI interactions.
"""

import logging
from typing import Optional
from openai import OpenAI, RateLimitError, APIError
from config import OpenAIConfig


class FinancialAnalystClient:
    """Client for interacting with OpenAI API as a financial analyst."""
    
    def __init__(self, config: OpenAIConfig, logger: logging.Logger):
        """
        Initialize the OpenAI client.
        
        Args:
            config: OpenAI configuration object.
            logger: Logger instance.
        """
        self.client = OpenAI()
        self.config = config
        self.logger = logger
    
    def get_website_recommendations(self, topic: str = "stock market") -> Optional[str]:
        """
        Get recommendations for financial websites.
        
        Args:
            topic: The topic to get recommendations for.
            
        Returns:
            str: Response containing website recommendations, or None if request fails.
        """
        try:
            self.logger.info(f"Fetching website recommendations for: {topic}")
            
            message = f"Provide some good websites for financial information pertaining to the {topic}. These should include both sites with news and analysis, as well as sites that provide data and statistics on {topic}, especially sites where basic financial information, such as EPS, revenue, earnings, etc. Please include a brief description of each site and what it offers."
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                temperature=self.config.temperature,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant who is an expert financial analyst."},
                    {"role": "user", "content": message}
                ]
            )
            
            self.logger.debug(f"Successfully retrieved recommendations for {topic}")
            return response.choices[0].message.content
            
        except RateLimitError:
            self.logger.error("Rate limit exceeded. Please try again later.")
            return None
        except APIError as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching recommendations: {str(e)}")
            return None
    
    def summarize_content(self, content: str, analysis_type: str = "summary") -> Optional[str]:
        """
        Summarize or analyze financial content.
        
        Args:
            content: The financial content to analyze.
            analysis_type: Type of analysis ("summary", "key_points", "action_items", "risks").
            
        Returns:
            str: Analysis result, or None if request fails.
        """
        try:
            self.logger.info(f"Performing {analysis_type} analysis on content")
            
            prompts = {
                "summary": "You are provided with a cleaned up financial news article. Please summarize the key points and implications for investors.",
                "key_points": "Extract and list the top 5 key points from this financial article that investors should know about.",
                "action_items": "Based on this financial article, what actionable items should investors consider? List them clearly.",
                "risks": "Identify and explain the key risks mentioned or implied in this financial article for investors."
            }
            
            system_prompt = prompts.get(analysis_type, prompts["summary"])
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                temperature=self.config.temperature,
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant who is an expert financial analyst. {system_prompt}"},
                    {"role": "user", "content": f"Here is the content to analyze:\n\n{content}"}
                ]
            )
            
            self.logger.debug(f"Successfully completed {analysis_type} analysis")
            return response.choices[0].message.content
            
        except RateLimitError:
            self.logger.error("Rate limit exceeded. Please try again later.")
            return None
        except APIError as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during analysis: {str(e)}")
            return None
    
    def ask_question(self, question: str, context: Optional[str] = None) -> Optional[str]:
        """
        Ask a custom financial question.
        
        Args:
            question: The financial question to ask.
            context: Optional context or document to reference.
            
        Returns:
            str: Response to the question, or None if request fails.
        """
        try:
            self.logger.info(f"Processing custom question: {question[:50]}...")
            
            content = question
            if context:
                content = f"Context:\n{context}\n\nQuestion: {question}"
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                temperature=self.config.temperature,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant who is an expert financial analyst. Provide clear, actionable advice."},
                    {"role": "user", "content": content}
                ]
            )
            
            return response.choices[0].message.content
            
        except RateLimitError:
            self.logger.error("Rate limit exceeded. Please try again later.")
            return None
        except APIError as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing question: {str(e)}")
            return None
