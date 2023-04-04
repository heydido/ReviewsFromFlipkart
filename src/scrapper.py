import bs4
import requests
from abc import ABC, abstractmethod


class EComReviewsScrapping(ABC):
    """
    This is the parent class for scrapping reviews from ECommerce websites.
    """

    def __init__(self):
        pass

    @abstractmethod
    def get_reviews(self, search_item: str):
        pass


class FlipkartReviewsScrapping(EComReviewsScrapping):
    def __init__(self, base_url="https://www.flipkart.com/search?q="):
        super().__init__()
        self.base_url = base_url

    def get_reviews(self, search_item: str):
        reviews = []

        search_url = self.base_url + search_item
        res = requests.get(search_url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        product_boxes = soup.find_all("div", {"class": "_1AtVbE col-12-12"})[3:]
        product_box = product_boxes[0]

        try:
            sub_link = product_box.div.div.div.a['href']
            product_link = "https://www.flipkart.com" + sub_link

            product_description = {}
            product_name = sub_link.split('/')[1]
            product_description['product_name'] = product_name
            product_description['product_page'] = product_link
            reviews.append(product_description)

            product_res = requests.get(product_link)
            product_soup = bs4.BeautifulSoup(product_res.text, 'lxml')
            comment_boxes = product_soup.find_all("div", {"class": "_16PBlm"})

            for comment_box in comment_boxes:
                review = {}
                who_commented = comment_box.div.div.find_all("p", {"class": "_2sc7ZR _2V5EHH"})[0].text
                star_rating = comment_box.div.div.div.div.text
                comment_title = comment_box.div.div.div.p.text

                comment_body = comment_box.div.div.find_all("div", {"class": ""})[0].text
                comment_body = comment_body.replace('READ MORE', '') if 'READ MORE' in comment_body else comment_body

                review['who_commented'] = who_commented
                review['star_rating'] = star_rating
                review['comment_title'] = comment_title
                review['comment_body'] = comment_body

                reviews.append(review)
        except AttributeError as e:
            pass
        return reviews


class AmazonReviewsScrapping(EComReviewsScrapping):
    def __init__(self):
        super().__init__()
        pass

    def get_reviews(self, search_item: str):
        pass
