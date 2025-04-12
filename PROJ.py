import requests
import time
import json
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"

# Custom headers mimicking real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Class representing a single book
class Book:
    
    def __init__(self, title, price, availability, rating, link):
        self.title = title
        self.price = price
        self.availability = availability
        self.rating = rating
        self.link = link

    # Displaying single book info
    def display(self):
        print(f"\nTitle: {self.title}")
        print(f"Price: {self.price}")
        print(f"Availability: {self.availability}")
        print(f"Rating: {self.rating}")
        print(f"Link: {self.link}")

# Class for scraping the website
class BookScraper:
    
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    # Function checking robots.txt (missing in this case)
    def check_robots_txt(self):
        url = self.base_url + "robots.txt"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            print("robots.txt content:\n", response.text)
        else:
            print(f"robots.txt not found (status code: {response.status_code})")

    # Function for rate limiting and error handling
    def fetch_page(self, url, delay=2):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            time.sleep(delay)  # Rate limiting to avoid server overload
            return response.text
        except requests.exceptions.HTTPError as htt_err:
            print(f"HTTP error: {htt_err}")
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
        return None

    # Scrape homepage book data
    def scrape_homepage(self):
        html = self.fetch_page(self.base_url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        books = []

        book_items = soup.find_all("article", class_="product_pod")  # Using find_all()
        for book in book_items:
            try:
                title_tag = book.select_one("h3 a")  # Using select_one()
                title = title_tag.get("title", "No title")

                price_tag = book.find("p", class_="price_color")  # Using find()
                price = price_tag.get_text(strip=True) if price_tag else "No price"

                availability_tag = book.find("p", class_="instock availability")
                availability = availability_tag.get_text(strip=True) if availability_tag else "No availability info"

                rating_tag = book.find("p", class_="star-rating")
                rating_class = rating_tag.get("class", []) if rating_tag else []
                rating = rating_class[1] if len(rating_class) > 1 else "No rating"

                link = title_tag.get("href", "#")
                full_link = self.base_url + link

                book_obj = Book(title, price, availability, rating, full_link)
                books.append(book_obj)

            except Exception as e:
                print(f"Skipping book due to error: {e}")

        return books

    # Save the collected data into a JSON file
    def save_to_json(self, books, filename="collected_data.json"):
        try:
            with open(filename, "w") as file:
                # Converting books list into a dictionary for easier JSON storage
                books_data = [{"title": book.title, "price": book.price, "availability": book.availability, 
                               "rating": book.rating, "link": book.link} for book in books]
                json.dump(books_data, file, indent=4)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data to JSON: {e}")

    # Load the data from the JSON file and convert back to Book objects
    def load_from_json(self, filename="collected_data.json"):
        try:
            with open(filename, "r") as file:
                books_data = json.load(file)
                # Convert each dictionary back to a Book object
                books = [Book(book_data['title'], book_data['price'], book_data['availability'], 
                              book_data['rating'], book_data['link']) for book_data in books_data]
            print(f"Data loaded from {filename}")
            return books
        except Exception as e:
            print(f"Error loading data from JSON: {e}")
        return []

    # Perform rating count analysis on the collected data
    def analyze_data(self, books):
        rating_count = {
            "One": 0,
            "Two": 0,
            "Three": 0,
            "Four": 0,
            "Five": 0
        }

        for book in books:
            if book.rating != "No rating":
                rating_count[book.rating] += 1

        print("\nBooks by Rating:")
        for rating, count in rating_count.items():
            print(f"{rating}: {count} books")

if __name__ == "__main__":
    scraper = BookScraper(BASE_URL, HEADERS)
    scraper.check_robots_txt()
    all_books = scraper.scrape_homepage()

    # Save collected data to JSON
    scraper.save_to_json(all_books)

    # Load data from the JSON file and convert back to Book objects
    books_from_json = scraper.load_from_json()

    # Perform analysis on the loaded data
    scraper.analyze_data(books_from_json)
