import traceback
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

class SN:
    def __init__(self,searchKeyword,searchNum):
        self.searchKeyword = searchKeyword
        self.serchNum = searchNum

    def getItems(self) -> List:
        res = []
        nowPage = 0
        nowItemNum = 0
        startUrl = 'https://search.suning.com/' + self.searchKeyword+'/'

        try:
            chrom_options = Options()
            chrom_options.add_argument('--headless')
            chrom_options.add_argument('--disable-gpu')
            prefs = {'profile.managed_default_content_settings.images': 2}
            chrom_options.add_experimental_option('prefs',prefs)
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
                    print(driver.find_element_by_id('nextPage'))
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
                        item['price'] = str(i.find(class_='def-price').get_text()).replace('¥','')
                        item['img'] = i.find(class_='img-block').a.img['src']
                        try:
                            item['comments'] = str(i.find(class_='info-evaluate').a.get_text()).replace('评价','')
                        except:
                            item['comments'] = 'Unknown'
                        item['sales'] = 'N/A'
                        item['link'] = i.find(class_='title-selling-point').a['href']
                        try:
                            item['store'] = i.find(class_='store-name').get_text()
                        except:
                            item['store'] = 'Unknown'
                        item['origin'] = 'SN'
                        nowItemNum = nowItemNum+1
                        res.append(item)
            driver.quit()
        except:
            print(traceback.format_exc())
            driver.quit()
        return res


if __name__=='__main__':
    crawler = SN('洗衣机',10)
    res = crawler.getItems()
    print(res)