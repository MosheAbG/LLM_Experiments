# Financial Content Summarization Tool

A robust Python application for summarizing and analyzing financial news articles and content using OpenAI's GPT models.

## Features

- **Article Summarization**: Fetch and summarize financial articles from URLs
- **Multiple Analysis Types**: Get summaries, key points, action items, or risk analysis
- **Website Recommendations**: Get AI-powered recommendations for financial information sources
- **Custom Questions**: Ask custom financial analysis questions with optional context
- **Interactive Mode**: User-friendly interactive command-line interface
- **Comprehensive Logging**: Debug logging and detailed error messages
- **Configurable**: Easy configuration via environment variables
- **Production-Ready**: Proper error handling, retry logic, and rate limit handling

## Project Structure

```
summarization/
├── basic_summarization.py          # Main CLI application
├── config.py                       # Configuration management
├── logger.py                       # Logging setup
├── api_client.py                   # OpenAI API client wrapper
├── summarization_service.py        # Core summarization service
├── util.py                         # Website content extraction
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## Installation

### Prerequisites

- Python 3.9+
- OpenAI API key

### Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd summarization
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   
   Optional environment variables:
   ```
   OPENAI_MODEL=gpt-4o-mini        # Default model to use
   OPENAI_TEMPERATURE=0.7          # Model temperature (0-2)
   LOG_LEVEL=INFO                  # Logging level (DEBUG, INFO, WARNING, ERROR)
   DEBUG=false                     # Enable debug mode
   ```

## Usage

### Command-Line Options

#### Get Website Recommendations
```bash
python basic_summarization.py --websites
python basic_summarization.py --websites --topic "cryptocurrency"
```

#### Summarize an Article
```bash
# Basic summary
python basic_summarization.py --url "https://finance.yahoo.com/news/..."

# Get key points
python basic_summarization.py --url "https://finance.yahoo.com/news/..." --type key_points

# Get actionable items
python basic_summarization.py --url "https://finance.yahoo.com/news/..." --type action_items

# Identify risks
python basic_summarization.py --url "https://finance.yahoo.com/news/..." --type risks
```

#### Ask a Custom Question
```bash
python basic_summarization.py --ask "What are the implications of rising interest rates for tech stocks?"
```

#### Analyze Provided Text
```bash
python basic_summarization.py --text "Your financial text here" --type summary
```

#### Interactive Mode
```bash
python basic_summarization.py --interactive
```

In interactive mode, available commands:
- `summarize <url>` - Summarize an article from URL
- `analyze <url> <type>` - Analyze with specific type
- `ask <question>` - Ask a financial question
- `websites [topic]` - Get website recommendations
- `help` - Show help
- `exit` - Exit the program

#### Debug Mode
```bash
python basic_summarization.py --debug --url "https://..."
```

#### Default Demo
```bash
# Run default demo (no arguments)
python basic_summarization.py
```

## Analysis Types

- **summary**: Summarize key points and implications
- **key_points**: Extract top 5 key points
- **action_items**: Identify actionable items for investors
- **risks**: Identify and explain risks

## Configuration

### Via Environment Variables

The application reads configuration from a `.env` file in the same directory. Create a `.env` file with:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
LOG_LEVEL=INFO
DEBUG=false
```

### Programmatic Configuration

You can also configure the application programmatically:

```python
from config import AppConfig, OpenAIConfig, WebsiteConfig, load_config
from logger import setup_logging
from api_client import FinancialAnalystClient
from summarization_service import FinancialSummarizationService

# Load configuration
config = load_config()

# Setup logging
logger = setup_logging(config.log_level, config.debug)

# Initialize clients
api_client = FinancialAnalystClient(config.openai, logger)
service = FinancialSummarizationService(api_client, logger)

# Use the service
result = service.summarize_article_from_url("https://example.com")
print(result)
```

## Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV LOG_LEVEL=INFO

ENTRYPOINT ["python", "basic_summarization.py"]
CMD ["--help"]
```

Build and run:
```bash
docker build -t financial-summarizer .
docker run -e OPENAI_API_KEY="your_key" financial-summarizer --help
```

### AWS Lambda Deployment

The application can be deployed as an AWS Lambda function:

```python
# lambda_handler.py
from basic_summarization import main
import sys
from io import StringIO

def lambda_handler(event, context):
    """Lambda handler for AWS Lambda deployment."""
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        # Parse event parameters and set sys.argv
        sys.argv = ["basic_summarization.py"]
        if event.get("url"):
            sys.argv.extend(["--url", event["url"]])
        if event.get("type"):
            sys.argv.extend(["--type", event["type"]])
        
        main()
        output = sys.stdout.getvalue()
        
        return {
            "statusCode": 200,
            "body": output
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
    finally:
        sys.stdout = old_stdout
```

### Systemd Service (Linux)

Create `/etc/systemd/system/financial-summarizer.service`:

```ini
[Unit]
Description=Financial Content Summarization Tool
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/financial-summarizer
Environment="OPENAI_API_KEY=your_key_here"
ExecStart=/usr/bin/python3 basic_summarization.py --interactive
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable financial-summarizer
sudo systemctl start financial-summarizer
```

## Error Handling

The application handles various error scenarios:

- **Missing API Key**: Clear error message if `OPENAI_API_KEY` is not set
- **Rate Limiting**: Handles OpenAI rate limit errors gracefully
- **Network Errors**: Handles website extraction failures
- **Invalid URLs**: Validates and handles malformed URLs
- **API Errors**: Comprehensive error logging and user-friendly messages

## Logging

The application provides detailed logging:

- **INFO**: Standard operation logging
- **DEBUG**: Detailed debugging information (enable with `--debug`)
- **ERROR**: Error conditions and exceptions

Logs include timestamps and can be redirected:

```bash
python basic_summarization.py --url "https://..." > output.log 2>&1
```

## Examples

### Example 1: Summarize a News Article
```bash
python basic_summarization.py --url "https://finance.yahoo.com/news/..." --type summary
```

### Example 2: Find Investment Opportunities
```bash
python basic_summarization.py --ask "What sectors are recommended for investment in the current market?"
```

### Example 3: Analyze Multiple Articles in a Loop
```bash
for url in $(cat urls.txt); do
    python basic_summarization.py --url "$url" --type key_points
done
```

## Troubleshooting

### "OPENAI_API_KEY is not set"
- Ensure you have created a `.env` file with your API key
- Check that the file is in the same directory as `basic_summarization.py`
- Verify the API key is correct and not expired

### "Rate limit exceeded"
- Wait a moment and try again
- Consider spreading requests over time
- Check your OpenAI account usage

### "Failed to extract content from URL"
- Verify the URL is correct and accessible
- Some websites may have CORS restrictions
- Try a different article URL

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using a Python 3.9+ environment

## Performance Considerations

- API calls to OpenAI are rate-limited per your account tier
- Website extraction timeout is set to 10 seconds
- Large articles may take longer to process
- Consider caching results for frequently accessed content

## Security Considerations

- **Never commit `.env` file** with your API key to version control
- Store API keys securely in production (use AWS Secrets Manager, Azure Key Vault, etc.)
- Validate and sanitize user inputs
- Use HTTPS for all external API calls (handled by the `requests` library)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the detailed logging output with `--debug`
3. Verify your OpenAI API key and account status
4. Check the OpenAI documentation at https://platform.openai.com/docs
