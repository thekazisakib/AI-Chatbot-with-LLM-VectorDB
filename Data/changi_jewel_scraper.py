import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_content(url):
    """
    Scrape the content of the given URL while filtering out ads.
    Args:
        url (str): URL to scrape content from.
    Returns:
        list: List of cleaned paragraphs from the page.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Filter out known ad elements
        for ad in soup.find_all(['div', 'span', 'iframe'], class_=re.compile(r'ad|ads|advertisement|promo', re.I)):
            ad.decompose()

        # Extract FAQs, guides, and descriptive sections
        content = []

        # Selectors for relevant text elements
        for section in soup.find_all(['p', 'h2', 'h3', 'li'], recursive=True):
            text = section.get_text(strip=True)
            if text and len(text) > 30:  # Filter short or irrelevant texts
                content.append(text)

        if not content:
            print(f"No relevant content found on {url}.")
        return content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def clean_content(content):
    """
    Clean the extracted content by normalizing and removing unwanted characters.
    Args:
        content (list): List of raw text data.
    Returns:
        list: List of cleaned text data.
    """
    cleaned_data = []
    for text in content:
        # Normalize text
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove special characters
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
        cleaned_data.append(text)

    return cleaned_data

def save_to_json(data, filename):
    """
    Save the cleaned data to a JSON file.
    Args:
        data (dict): Dictionary containing cleaned data.
        filename (str): Filename for the JSON file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

if __name__ == "__main__":
    # URLs to scrape
    urls = {
        "changi_airport": "https://www.changiairport.com/in/en.html",
        "jewel_changi_airport": "https://www.jewelchangiairport.com"
    }

    all_data = {}

    for name, url in urls.items():
        print(f"Scraping {name}...")
        raw_content = scrape_content(url)
        print(f"Extracted {len(raw_content)} sections from {name}.")

        print(f"Cleaning {name} content...")
        cleaned_content = clean_content(raw_content)
        all_data[name] = cleaned_content

    # Save cleaned content to JSON
    save_to_json(all_data, "changi_jewel_content.json")
