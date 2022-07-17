import time

# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup

CONFIRM1 = "VfPpkd-dgl2Hf-ppHlrf-sM5MNb"
CONFIRM2 = "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qfvgSe.qIypjc" \
           ".TrZEUc.lw1w4b "
INPUT_TAG = "input"
INPUT_CLASS = "whsOnd.zHQkBf"

GOOGLE_ACCOUNT = "2016123304@yonsei.ac.kr"
PASSWORD = "p0assW2O9R4D!@"


class Web:

    def __init__(self, chromedriver, identifier):
        self.driver = chromedriver
        self.identifier = identifier

    def login(self, url):
        try:
            self.driver.get(url)
            self.driver.find_element(By.CLASS_NAME, CONFIRM1)
            time.sleep(1)
            self.driver.find_element(By.TAG_NAME, INPUT_TAG).send_keys(GOOGLE_ACCOUNT)
            time.sleep(2)
            self.driver.find_element(By.CLASS_NAME, CONFIRM2).click()
            time.sleep(5)
            self.driver.find_element(By.CLASS_NAME, INPUT_CLASS).send_keys(PASSWORD)
            time.sleep(5)
            self.driver.find_element(By.CLASS_NAME, CONFIRM2).click()
            time.sleep(10)
        except RuntimeError as error:
            print(f'runtime_error:{error}')

    def crawl(self, head, tail):
        html = self.driver.execute_script("return document.body.innerHTML;")
        html_parser = BeautifulSoup(html, 'html.parser')
        docs_container = html_parser.find_all(attrs={'class': f"{self.identifier}"})
        docs_url = []
        for docsId in docs_container:
            docs_string = str(docsId)
            if head in docs_string and tail in docs_string:
                start_index = docs_string.index(head)
                end_index = docs_string.index(tail)
                docs_url.append(docs_string[start_index + len(head) + 1:end_index])
        return docs_url


if __name__ == '__main__':
    pass
    # macro = MacroBot(Chrome(), "docs-homescreen-grid-item-thumbnail", "crawl")
    # macro.login("https://docs.google.com")
    # macro.crawl("/d", "=w")
