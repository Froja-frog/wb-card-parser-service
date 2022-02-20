import datetime

from django.db import IntegrityError

from .models import Query, Result
from bs4 import BeautifulSoup as bs
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Parser:
    """Parser that gets product card position at page"""

    def __init_driver(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path='/Users/macadmin/wb_webparser/main/chromedriver',
                                       options=self.options)

    @staticmethod
    def __needs_to_parse():
        """Checks if app needs to parse some info from wildberries"""
        today = datetime.date.today().day
        queries = Query.objects.all()
        for query in queries:
            try:
                Result.objects.get(query__prod_article=query.prod_article, date__day=today)
            except Result.DoesNotExist:
                return True
        return False

    @staticmethod
    def __get_pages_urls() -> list[dict]:
        queries = Query.objects.all()
        pages_urls = []
        for query in queries:
            query_urls = {query.prod_article:
                          [f"https://www.wildberries.ru/catalog/0/search.aspx?page={page}&search={query.query_text}"
                           for page in range(1, settings.DEFAULT_PAGES_COUNT + 1)]}
            pages_urls.append(query_urls)
        return pages_urls

    def __get_results(self):
        pages_urls = self.__get_pages_urls()
        for query_dict in pages_urls:
            for url_list in query_dict.values():
                for url in url_list:
                    self.driver.get(url)
                    WebDriverWait(self.driver, 30).until(
                        ec.presence_of_element_located((By.CLASS_NAME, "product-card")))
                    page_html = bs(self.driver.page_source, "lxml")
                    article = list(query_dict.keys())[0]
                    page_index = url_list.index(url)
                    found = self.__product_found(page_html, article)
                    if page_index == settings.DEFAULT_PAGES_COUNT - 1 and not found:
                        position = "X"
                    else:
                        position = self.__get_product_position(page_html, article, page_index)
                    self.__add_result(article, position)

    @staticmethod
    def __get_product_position(page: bs, article: str, page_index: int) -> int:
        cards = page.find_all('div', {'class': "product-card"})[:100]
        for card in cards:
            if card["id"] == f"c{article}":
                return cards.index(card) + (100 * page_index)

    @staticmethod
    def __product_found(page: bs, article: str) -> bool:
        product = page.find("div", {'id': f"c{article}"})
        if product is not None:
            return True
        return False

    @staticmethod
    def __add_result(article, position):
        query = Query.objects.get(prod_article=article)
        try:
            Result.objects.create(position=position, query=query)
        except IntegrityError:
            return True

    def run(self):
        if self.__needs_to_parse():
            try:
                self.__init_driver()
                self.__get_results()
            finally:
                self.driver.close()
                self.driver.quit()


if __name__ == '__main__':
    parser = Parser()
    parser.run()
