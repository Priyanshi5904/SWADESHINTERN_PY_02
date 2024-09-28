"""
First install the necessary libraries to make it workable:
pip install requests beautifulsoup4
"""
import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL for Books to Scrape (this is the website we'll scrape)
BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'

# Headers to mimic a web browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def fetch_html(url):
    """
    Fetch the HTML content of the given URL.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def parse_page(html):
    """
    Parse the HTML content and extract relevant data (book title, price, availability).
    """
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    
    book_list = []
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()
        
        book_list.append({
            'title': title,
            'price': price,
            'availability': availability
        })
    
    return book_list

def save_to_csv(data, filename='books_scraped.csv'):
    """
    Save the extracted data into a CSV file.
    """
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def scrape_books(base_url, max_pages=3):
    """
    Scrape books from multiple pages with pagination.
    """
    all_books = []
    
    for page in range(1, max_pages + 1):
        url = base_url.format(page)
        print(f"Scraping: {url}")
        
        html = fetch_html(url)
        if html:
            books = parse_page(html)
            all_books.extend(books)
        
        # Delay to avoid overwhelming the server
        time.sleep(2)
    
    return all_books

if __name__ == "__main__":
    # Scrape data from the first 3 pages
    scraped_books = scrape_books(BASE_URL, max_pages=3)
    
    if scraped_books:
        # Save the data to CSV
        save_to_csv(scraped_books)
        print(f"Scraped {len(scraped_books)} books. Data saved to books_scraped.csv.")
    else:
        print("No data scraped.")
