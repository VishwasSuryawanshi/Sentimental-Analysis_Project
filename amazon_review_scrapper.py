import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewlist = []

url = "https://www.amazon.in/SJCAM-Touchscreen-2880x2160-Novatek-Accessories/product-reviews/B07DC4SCXS/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def get_reviews(soup):
    reviews = soup.find_all("div", {"data-hook":"review"})
    try :
        for item in reviews :
            review = {
                "title" : item.find("a", {"data-hook":"review-title"}).text.strip(),
                "body" : item.find("span", {"data-hook":"review-body"}).text.strip(),
                "rating" : item.find("i",{"data-hook":"review-star-rating"}).text.strip(),
                }
            reviewlist.append(review)
    except :
        pass

for x in range(1,999):
    soup = get_soup(f"https://www.amazon.in/SJCAM-Touchscreen-2880x2160-Novatek-Accessories/product-reviews/B07DC4SCXS/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber={x}")
    print(f"Getting page : {x}")
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find("li", {"class":"a-disabled a-last"}):
        pass
    else :
        break

df = pd.DataFrame(reviewlist)
df.to_csv("amazon_reviews.csv", index=False)
print("Fin.")