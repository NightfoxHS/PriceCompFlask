from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import os

class SN:
    def __init__(self,searchKeyword,searchNum):
        self.searchKeyword = searchKeyword
        self.serchNum = searchNum

    def getItems(self):
        res = []
        nowPage = 0
        nowItemNum = 0
        startUrl = 'https://search.suning.com/' + self.searchKeyword+'/'

        try:
            chrom_options = Options()
            chrom_options.add_argument('--headless')
            chrom_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=chrom_options)
            script = '''
                    Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                    })
            ''' # 规避反爬
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
            driver.get(startUrl)
            while nowItemNum < self.serchNum:
                nowPage = nowPage + 1
                if nowPage > 1:
                    driver.find_element_by_id('nextPage').click()
                html = bs(driver.page_source,'html.parser')
                itemsList = html.find_all('li',attrs={'doctype':'1'})
                if itemsList == None:
                    return res
                for i in itemsList:
                    if nowItemNum < self.serchNum:
                        item = {}
                        item['id'] = 'S' + i['id']
                        item['name'] = i.find(class_='title-selling-point').a.get_text()
                        item['price'] = float(str(i.find(class_='def-price').get_text()).replace('¥',''))
                        item['store'] = i.find(class_='store-name').get_text()
                        item['origin'] = 'SN'
                        nowItemNum = nowItemNum+1
                        res.append(item)
            driver.quit()
            return res
        except:
            print('Perhaps reasons : 1. searchNum is too big for the keyword (most perhaps); 2. network error\n')
            driver.quit()



if __name__=='__main__':
    crawler = SN('MX375',2)
    res = crawler.getItems()
    print(res)