"""
Main application module with CLI interface.

This module provides a command-line interface for the financial summarization application.
"""

import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

from config import load_config
from logger import setup_logging
from api_client import FinancialAnalystClient
from summarization_service import FinancialSummarizationService


def print_section_header(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def main():
    """Main entry point for the application."""
    # Load environment variables
    load_dotenv(override=True)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Financial Content Summarization Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Summarize an article from a URL
  python basic_summarization.py --url https://finance.yahoo.com/news/...
  
  # Get website recommendations
  python basic_summarization.py --websites
  
  # Summarize with key points analysis
  python basic_summarization.py --url https://example.com --type key_points
  
  # Ask a custom financial question
  python basic_summarization.py --ask "What are the implications of rising interest rates?"
  
  # Interactive mode
  python basic_summarization.py --interactive
        """
    )
    
    parser.add_argument(
        "--url",
        type=str,
        help="URL of the financial article to summarize"
    )
    parser.add_argument(
        "--type",
        type=str,
        default="summary",
        choices=["summary", "key_points", "action_items", "risks"],
        help="Type of analysis to perform (default: summary)"
    )
    parser.add_argument(
        "--websites",
        action="store_true",
        help="Get recommendations for financial information websites"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="stock market",
        help="Topic for website recommendations (default: stock market)"
    )
    parser.add_argument(
        "--ask",
        type=str,
        help="Ask a custom financial question"
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Summarize provided text content"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive mode"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config()
        if args.debug:
            config.debug = True
            config.log_level = "DEBUG"
        
        # Setup logging
        logger = setup_logging(config.log_level, config.debug)
        logger.info("Application started")
        logger.debug(f"Configuration loaded: model={config.openai.model}")
        
        # Initialize clients
        api_client = FinancialAnalystClient(config.openai, logger)
        service = FinancialSummarizationService(api_client, logger)
        
        # Handle command-line actions
        if args.websites:
            print_section_header(f"Financial Website Recommendations: {args.topic}")
            result = api_client.get_website_recommendations(args.topic)
            if result:
                print(result)
            else:
                print("Failed to retrieve website recommendations.")
                return 1
        
        elif args.url:
            print_section_header(f"Analyzing Article ({args.type.replace('_', ' ').title()})")
            print(f"URL: {args.url}\n")
            result = service.summarize_article_from_url(args.url, args.type)
            if result:
                print(result)
            else:
                print("Failed to summarize the article.")
                return 1
        
        elif args.ask:
            print_section_header("Financial Analysis")
            print(f"Question: {args.ask}\n")
            result = api_client.ask_question(args.ask)
            if result:
                print(result)
            else:
                print("Failed to process the question.")
                return 1
        
        elif args.text:
            print_section_header(f"Text Analysis ({args.type.replace('_', ' ').title()})")
            result = service.summarize_text(args.text, args.type)
            if result:
                print(result)
            else:
                print("Failed to analyze the text.")
                return 1
        
        elif args.interactive:
            run_interactive_mode(api_client, service, logger)
        
        else:
            # Default behavior: run demo
            run_demo(api_client, service, logger)
        
        logger.info("Application completed successfully")
        return 0
        
    except ValueError as e:
        print(f"Configuration Error: {str(e)}", file=sys.stderr)
        logger.error(f"Configuration error: {str(e)}")
        return 1
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        print(f"Unexpected Error: {str(e)}", file=sys.stderr)
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return 1


def run_demo(api_client, service, logger):
    """Run the demo workflow."""
    print_section_header("Financial Website Recommendations")
    
    result = api_client.get_website_recommendations()
    if result:
        print(result)
    else:
        print("Failed to retrieve website recommendations.")
        return
    
    print_section_header("Summarizing Yahoo Finance Article")
    
    article_url = "https://finance.yahoo.com/news/inflation-in-focus-as-september-fed-meeting-nears-what-to-watch-this-week-120006808.html"
    print(f"URL: {article_url}\n")
    
    result = service.summarize_article_from_url(article_url)
    if result:
        print(result)
    else:
        print("Failed to summarize the article.")


def run_interactive_mode(api_client, service, logger):
    """Run the interactive mode."""
    print_section_header("Interactive Mode")
    print("Available commands:")
    print("  1. summarize <url>           - Summarize an article from URL")
    print("  2. analyze <url> <type>      - Analyze with specific type (summary, key_points, action_items, risks)")
    print("  3. ask <question>            - Ask a financial question")
    print("  4. websites [topic]          - Get website recommendations")
    print("  5. help                      - Show this help message")
    print("  6. exit                      - Exit the program\n")
    
    while True:
        try:
            user_input = input("Enter command: ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=2)
            command = parts[0].lower()
            
            if command == "exit":
                print("Exiting interactive mode.")
                break
            
            elif command == "help":
                print("  1. summarize <url>           - Summarize an article from URL")
                print("  2. analyze <url> <type>      - Analyze with specific type")
                print("  3. ask <question>            - Ask a financial question")
                print("  4. websites [topic]          - Get website recommendations")
                print("  5. help                      - Show this help message")
                print("  6. exit                      - Exit the program\n")
            
            elif command == "summarize":
                if len(parts) < 2:
                    print("Usage: summarize <url>")
                    continue
                url = parts[1]
                print("\nAnalyzing article...")
                result = service.summarize_article_from_url(url)
                if result:
                    print(f"\n{result}\n")
                else:
                    print("Failed to summarize the article.\n")
            
            elif command == "analyze":
                if len(parts) < 2:
                    print("Usage: analyze <url> [type]")
                    continue
                url = parts[1]
                analysis_type = parts[2] if len(parts) > 2 else "summary"
                if analysis_type not in service.get_analysis_types():
                    print(f"Invalid analysis type. Available: {', '.join(service.get_analysis_types())}")
                    continue
                print("\nAnalyzing article...")
                result = service.summarize_article_from_url(url, analysis_type)
                if result:
                    print(f"\n{result}\n")
                else:
                    print("Failed to analyze the article.\n")
            
            elif command == "ask":
                if len(parts) < 2:
                    print("Usage: ask <question>")
                    continue
                question = " ".join(parts[1:])
                print("\nProcessing question...")
                result = api_client.ask_question(question)
                if result:
                    print(f"\n{result}\n")
                else:
                    print("Failed to process the question.\n")
            
            elif command == "websites":
                topic = parts[1] if len(parts) > 1 else "stock market"
                print(f"\nGetting recommendations for: {topic}...")
                result = api_client.get_website_recommendations(topic)
                if result:
                    print(f"\n{result}\n")
                else:
                    print("Failed to retrieve recommendations.\n")
            
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.\n")
        
        except KeyboardInterrupt:
            print("\n\nExiting interactive mode.")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {str(e)}")
            print(f"Error: {str(e)}\n")


if __name__ == "__main__":
    sys.exit(main())
