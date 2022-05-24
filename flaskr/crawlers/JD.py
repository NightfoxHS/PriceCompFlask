import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

class JD:
    def __init__(self,searchKeyword,searchNum):
        self.searchKeyword = searchKeyword
        self.searchNum = searchNum

    def getItems(self):
        res=[]
        nowPage = 0
        nowItemNum = 0
        startUrl = 'https://search.jd.com/Search?keyword='+ self.searchKeyword +'&enc=utf-8&wq='+ self.searchKeyword
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
        
            while nowItemNum < self.searchNum:
                nowPage = nowPage + 1
                nowUrl = startUrl +'&page=' + str(nowPage)
                driver.get(nowUrl)
                html = bs(driver.page_source,'html.parser')
                itemsList = html.find(id='J_goodsList')
                itemsList = itemsList.find_all('li')
                if itemsList==None:
                    return res
                for i in itemsList:
                    if nowItemNum < self.searchNum:
                        item = {}
                        item['id'] = 'J'+i['data-sku']
                        item['name'] = i.find(class_='p-name').a.em.get_text()
                        item['price'] = i.find(attrs={'data-price':True}).string
                        item['img'] = i.find(class_='p-img').a.img['data-lazy-img']
                        item['comments'] = i.find(class_='p-commit').strong.a.get_text()
                        item['sales'] = 'N/A'
                        item['link'] = i.find(class_='p-name').a['href']
                        item['store'] = i.find(class_='p-shop').span.a.get_text()
                        item['origin'] = 'JD'
                        nowItemNum = nowItemNum + 1
                        res.append(item)
            driver.quit()
        except:
            print(traceback.format_exc())
            driver.quit()
        return res

            

    

if __name__=='__main__':
    crawler = JD('MX375',10)
    res = crawler.getItems()
    print(res)
