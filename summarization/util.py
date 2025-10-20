import logging
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Website:
    """A class to extract and clean text content from a website.

    Attributes:
        url (str): The URL of the website to extract content from.
        title (str): The title of the webpage.
        description (str): The meta description of the webpage.
        content (str): The cleaned text content extracted from the website.
    """

    def __init__(self, url: str):
        """Initializes the Website class with a URL and sets up headers for requests.
        Args:
            url (str): The URL of the website to extract content from.
        """

        if not urlparse(url).scheme:
            url = "http://" + url
        self.url = url
        self.title = ""
        self.description = ""
        self.content = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def _is_value(self, url: str) -> bool:
        """Checks if the URL is valid.
        Args:
            url (str): The URL to check.
        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        try:
            result = urlparse(url)
            if all([result.scheme, result.netloc]):
                return True
        except Exception as e:
            logging.error(f"Error parsing URL: {e}")
            return False

    def extract_content(self) -> Optional[str]:
        """Extracts and cleans text from a website.
        Returns:
            Optional[str]: The cleaned text content from the website or None if the extraction fails.
        """
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            # Extract title and description
            self.title = self._get_title(soup)
            self.description = self._get_description(soup)
            # Clean HTML content
            self.content = self._clean_html(soup)
            return self.content

        except requests.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return ""

    def _get_title(self, soup: BeautifulSoup) -> str:
        """Returns the title of the webpage."""
        if soup.title:
            return soup.title.string.strip()
        else:
            return "No Title"

    def _get_description(self, soup: BeautifulSoup) -> str:
        """Returns the meta description of the webpage."""
        description_tag = soup.find("meta", attrs={"name": "description"})
        if description_tag and "content" in description_tag.attrs:
            return description_tag["content"].strip()
        else:
            return "No Description"

    def _clean_html(self, soup: BeautifulSoup) -> str:
        """Cleans HTML content by removing unwanted elements.
        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the HTML content.
        Returns:
            str: The cleaned text content.
        """
        unwanted_tags = [
            "script",
            "style",
            "noscript",
            "iframe",
            "ad",
            "img",
            "form",
            "nav",
            "aside",
            "link",
            "button",
            "figure",
            "input",
        ]
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        # Remove empty tags
        for element in soup.find_all():
            if not element.get_text(strip=True):
                element.decompose()
        return soup.get_text(separator="\n", strip=True)


if __name__ == "__main__":
    url = "https://finance.yahoo.com/news/inflation-in-focus-as-september-fed-meeting-nears-what-to-watch-this-week-120006808.html"
    website = Website(url)
    if website.extract_content() is not None:
        print(f"Title: {website.title}")
        print(f"Description: {website.description}")
        print("\nContent Preview (first 500 characters):")
        content = website.extract_content()
        print(f"{content[:500]}...")
