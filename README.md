# ng-bookscraping
Midterm project for Data scraping with Python

##  BookScraper

A Python-based web scraper that extracts book data from [Books to Scrape](https://books.toscrape.com), an online demo site for practicing web scraping.

##  Features

- Scrapes book data across all categories and pages
- Extracts:
  - Title
  - Price
  - Availability
  - Star rating
  - Product URL
- Saves data to CSV and/or JSON
- Modular, readable code with room for extension

## Technologies Used

- Python 3.13.2
- [requests]
- [BeautifulSoup (bs4)]
- CSV / JSON 

##                                           INSTRUCTIONS 

1. INITIALIZATION 

The BookScraper class is initialized with a base URL and custom headers to mimic a browser.

A Book class is used to structure the data for each book (title, price, availability, rating, link).

2. robots.txt

Scraper first attempts to access robots.txt to check if scraping is allowed 

This site doesn't have robots.txt but i included this feauture for good scraping etiquette

3. Scraping homepage

It fetches HTML content of the homepage using requests 

BeautifulSoup parses the html to extract book data:

Title, Price, Availability, Star rating, Relative product link(converted to full URL)

4. Saving Data

After scraping the script converts the list of books to dictionaries

Data is saved in readable format in collected_data.json

5. Loading data from JSON

Data can be loaded back from JSON

After loading data, it's used to reconstruct book objects using the load_from_json() method

6. Analysis

Script counts how many books have 1 star rating , 2 star rating .... 5 star rating

After running script it's displayed how many books fall into each star rating category



