from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.options import Options

def get_reviews(driver):
    review_list = []
    rating_list = [] 
    reviews = driver.find_elements(By.CLASS_NAME,"review")
    
    try:
        for items in reviews:
            
            review_list.append(items.find_element(By.CLASS_NAME,"review-text").text.strip())
    except Exception as e:
        print(f'An error occurred --> {e}')
    return review_list


def start_scraping(url,pagecount=10):
    Options.headless = True

    review_set = []
    url = url.replace("dp", "product-reviews")
    loc = url.find("ref")
    inital_page_ref = "ref=cm_cr_dp_d_show_all_btm"
    url_final = url[:loc] + f"/{inital_page_ref}?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber="
    driver = webdriver.Firefox()
    new_page = url_final+f'{1}'
    for x in range(2, pagecount):
        print(new_page)
        driver.get(new_page)
        time.sleep(5)
        review= get_reviews(driver)
        review_set.extend(review)
        try:
            next_page = driver.find_element(By.CLASS_NAME ,'a-disabled a-last')
            break
        except:
            pass
        paging_ref = f'ref=cm_cr_getr_d_paging_btm_next_{x}'
        new_page = url[:loc] + f"/{paging_ref}?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={x}"
    driver.close()
    return review_set

