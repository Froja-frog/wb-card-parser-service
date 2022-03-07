import datetime

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
        today = datetime.date.today().strftime('%d.%m')
        print(today)
        queries = Query.objects.all()
        for query in queries:
            result = Result.objects.filter(query=query, results_dict__has_key=today)
            print(f"{result = }")
            if len(result) == 0:
                return True
        return False

    @staticmethod
    def __get_pages_urls() -> list[dict]:
        queries = Query.objects.all()
        pages_urls = []
        for query in queries:
            query_urls = {query.prod_article:
                              [f"https://www.wildberries.ru/catalog/0/search.aspx?page={page}&search={query.query_text}"
                               for page in range(1, settings.DEFAULT_PAGES_COUNT + 1)],
                          'query_text': query.query_text}
            pages_urls.append(query_urls)
        return pages_urls

    def __get_results(self):
        pages_urls = self.__get_pages_urls()
        for query_dict in pages_urls:
            print(query_dict.values())
            for url_list in list(query_dict.values())[:-1]:
                for url in url_list:
                    print(url)
                    self.driver.get(url)
                    WebDriverWait(self.driver, 30).until(
                        ec.presence_of_element_located((By.CLASS_NAME, "product-card")))
                    page_html = bs(self.driver.page_source, "lxml")
                    if url == 'https://www.wildberries.ru/catalog/0/search.aspx?page=1&search=чай':
                        with open('test.html', 'w') as f:
                            f.write(str(page_html))
                    article = list(query_dict.keys())[0]
                    page_index = url_list.index(url)
                    found = self.__product_found(page_html, article)
                    print(found)
                    if page_index == settings.DEFAULT_PAGES_COUNT - 1 and not found:
                        position = "X"
                        self.__add_result(article, query_dict.get('query_text'), position)
                    else:
                        position = self.__get_product_position(page_html, article, page_index)
                        print(position)
                        self.__add_result(article, query_dict.get('query_text'), position)
                        break

    @staticmethod
    def __get_product_position(page: bs, article: str, page_index: int) -> int:
        cards = page.find_all('div', {'class': "product-card"})[:100]
        for card in cards:
            if card["id"] == f"c{article}":
                return cards.index(card) + (100 * page_index)

    @staticmethod
    def __product_found(page: bs, article: str) -> bool:
        print(f"c{article}")
        product = page.find("div", {'id': f"c{article}"})
        if product is not None:
            return True
        return False

    @staticmethod
    def __add_result(article, query_text, position):
        query = Query.objects.get(prod_article=article, query_text=query_text)
        result = Result.objects.get_or_create(query=query)[0]
        result.results_dict[datetime.date.today().strftime('%d.%m')] = position
        result.save()

    def run(self):
        print(self.__needs_to_parse())
        if self.__needs_to_parse():
            try:
                self.__init_driver()
                self.__get_results()
            finally:
                self.driver.close()
                self.driver.quit()


def run():
    parser = Parser()
    parser.run()


if __name__ == '__main__':
    run()
