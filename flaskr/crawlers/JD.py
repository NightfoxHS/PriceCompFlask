import requests
from bs4 import BeautifulSoup as bs

class JD:
    def __init__(self,searchKeyword,searchNum):
        self.searchKeyword = searchKeyword
        self.searchNum = searchNum
        self.res = []

    def getItems(self):
        nowPage = 0
        nowItemNum = 0
        startUrl = 'https://search.jd.com/Search?keyword='+ self.searchKeyword +'&enc=utf-8&wq='+ self.searchKeyword
        head = {'user-agent':'Mozilla/5.0'}
        while nowItemNum < self.searchNum:
            nowPage = nowPage + 1
            nowUrl = startUrl +'&page=' + str(nowPage)
            r = requests.get(nowUrl,headers=head,timeout=50)
            r.raise_for_status()
            r.encoding=r.apparent_encoding

            if r.status_code==200:
                html = bs(r.text,'html.parser')
                itemsList = html.find(id='J_goodsList')
                itemsIdList = itemsList.find_all('li')
                itemsPriceList = itemsList.find_all('i',attrs={'data-price':True})
                itemsNameList = itemsList.find_all(class_='p-name')
                for i in range(len(itemsList)):
                    if nowItemNum < self.searchNum:
                        item = {}
                        item['id'] = 'J'+itemsIdList[i]['data-sku']
                        item['name'] = itemsNameList[i].a.em.get_text()
                        item['price'] = float(itemsPriceList[i].string)
                        item['link'] = itemsNameList[i].a['href']
                        item['origin'] = 'JD'
                        nowItemNum = nowItemNum + 1
                        self.res.append(item)
            else:
                return self.res 
        return self.res

            

    

if __name__=='__main__':
    crawler = JD('Iphone XS',10)
    res = crawler.getItems()
    print(res)
