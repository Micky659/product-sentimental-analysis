from bs4 import BeautifulSoup as bs
import requests


def get_soup(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/90.0.4430.212 Safari/537.36'}
    response = requests.get(url, headers=header)
    soup = bs(response.content, 'html.parser')
    return soup


def get_reviews(soup):
    review_list = []
    rating_list = []
    reviews = soup.find_all('div', {'data-hook': 'review'})

    try:
        for items in reviews:
            review_list.append(items.find('span', {'data-hook': 'review-body'}).text.strip())
            rating_list.append(float(items.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars','').strip()))
    except Exception as e:
        print(f'An error occurred --> {e}')
    return review_list, rating_list


def start_scraping(url, pagecount):
    review_set, rating_set = [], []
    url = url.replace("dp", "product-reviews")
    loc = url.find("ref")
    url_final = url[:loc] + "/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
    for x in range(10, pagecount+10):
        soup = get_soup(f'{url_final}{x}')

        review, rating = get_reviews(soup)
        review_set.extend(review)
        rating_set.extend(rating)
        if not soup.find('li', {'class': 'a-disabled a-last'}):
            pass
        else:
            break
    return review_set, rating_set
