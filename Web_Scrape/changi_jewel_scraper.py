import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url, output_file):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    content = [p.text.strip() for p in soup.find_all('p') if p.text.strip()]  # Extract text content
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4)
    print(f"Content scraped and saved to {output_file}")  # Save content to a JSON file

scrape_website("https://www.changiairport.com", "changi_airport_content.json")
scrape_website("https://www.jewelchangiairport.com", "jewel_changi_content.json")


def merge_json_files(file_paths, output_file):
    combined_content = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            combined_content.extend(json.load(file))
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(combined_content, file, indent=4)
    print(f"Content merged and saved to {output_file}")  # Save the combined content

merge_json_files(["changi_airport_content.json", "jewel_changi_content.json"], "changi_jewel_content.json")
