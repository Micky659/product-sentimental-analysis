import requests
from amazon_product_review_scraper import amazon_product_review_scraper
from bs4 import BeautifulSoup

def start_scraping(url):
    review_set, rating_set = [], []
    url_list = url.split('/')
    review_scraper = amazon_product_review_scraper(amazon_site="amazon.com", product_asin=url_list[5])
    reviews_df = review_scraper.scrape()
    print(reviews_df.head(5))

    return review_set, rating_set

url_link = input()
start_scraping(url_link)
