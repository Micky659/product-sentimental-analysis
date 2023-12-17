from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

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
    url_final = url[:loc] + f"/{inital_page_ref}?ie=UTF8&reviewerType=all_reviews&pageNumber="
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
        new_page = url[:loc] + f"/{paging_ref}?ie=UTF8&reviewerType=all_reviews&pageNumber={x}"
    driver.close()
    return review_set












def change_to_international(driver):
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "j-earth-icon")))
    world = driver.find_element(By.CLASS_NAME,"j-earth-icon")
    ActionChains(driver)\
            .move_to_element(world)\
            .perform()
    ActionChains(driver)\
            .click(world)\
            .perform()
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "global-international")))
    world_international = driver.find_element(By.CLASS_NAME,"global-international")
    ActionChains(driver)\
            .click(world_international)\
            .perform()
    


def get_reviews(driver):
    reviews=[]
    comments = driver.find_elements(By.CLASS_NAME,"common-reviews__list-item-detail")
    pattern = r"(.*)\nTranslate\n"
    for comment in comments:
        match = re.search(pattern, comment.text)
        if match:
            reviews.append(match.group(1))
    return reviews

def close_dialog_box(driver):
    close_btns = driver.find_elements(By.CLASS_NAME,"she-close")
    for close_btn in close_btns:
        try:
            ActionChains(driver)\
                    .click(close_btn)\
                    .perform()
            break
        except Exception as e:
            pass
            



def start_scraping_shein(url,page_count=5):
    init_url="https://www.shein.com/?is_manual_change_site=0&is_from_origin_btn=0&ref=de&ret=www&from_country=de"
    all_reviews= []
    driver = webdriver.Firefox()
    driver.get(init_url)
    try:
        close_dialog_box(driver)
    except:
        pass

    change_to_international(driver)
    url = "https://www.shein.com/Manfinity-Men-Japanese-Letter-Graphic-Tee-p-25111268-cat-1980.html?src_identifier=fc%3DMen%20fashion%60sc%3DMen%20fashion%60tc%3DShop%20By%20Category%60oc%3DTops%60ps%3Dtab05navbar05menu01dir04%60jc%3DitemPicking_100157210&src_module=topcat&src_tab_page_id=page_home1702816080839&mallCode=1&imgRatio=3-4"

    driver.get(url)
    time.sleep(5)
    try:
        close_dialog_box(driver)
    except:
        pass

    # change_to_international(driver)
    reviews = get_reviews(driver)
    all_reviews.extend(reviews)
    page_limit=5
    elements=driver.find_elements(By.CLASS_NAME,"common-reviews__list-item-detail")

    execute_script = "arguments[0].scrollIntoView(true);"
    driver.execute_script(execute_script, elements[-1])

    for page in range(2,page_limit):
        elements=driver.find_elements(By.CLASS_NAME,"sui-pagination__hover")
        
        element= elements[page-2]
        driver.execute_script(execute_script, element)
            
        ActionChains(driver)\
                    .click(element)\
                    .perform()
        reviews = get_reviews(driver)
        all_reviews.extend(reviews)
    all_reviews
