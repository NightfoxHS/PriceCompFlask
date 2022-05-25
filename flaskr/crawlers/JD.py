import traceback
from typing import List
import requests
from bs4 import BeautifulSoup as bs

class JD:
    def __init__(self,searchKeyword,searchNum):
        self.searchKeyword = searchKeyword
        self.searchNum = searchNum

    def getItems(self) -> List:
        res=[]
        nowPage = 0
        nowItemNum = 0
        startUrl = 'https://search.jd.com/Search?keyword='+ self.searchKeyword +'&enc=utf-8&wq='+ self.searchKeyword
        head = {'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'}
        try:
            while nowItemNum < self.searchNum:
                nowPage = nowPage + 1
                nowUrl = startUrl +'&page=' + str(nowPage)
                r = requests.get(nowUrl,headers=head)
                r.raise_for_status()
                html = bs(r.content,'html.parser')
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
        except:
            print(traceback.format_exc())
        return res

            

    

if __name__=='__main__':
    crawler = JD('MX375',10)
    res = crawler.getItems()
    print(res)
