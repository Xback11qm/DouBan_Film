import requests,time,random
from fake_useragent import UserAgent
from threading import Thread,Lock
from queue import Queue

class Douban:
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start={}&limit=20'
        self.i = 0
        self.q = Queue()
        self.lock = Lock()

    def get_agent(self):
        return UserAgent().random

    def url_in(self):
        """把所有要抓取的url地址放入队列"""
        for start in range(0,684,20):
            url = self.url.format(start)
            self.q.put(url)
    #线程事件函数:请求+解析+数据处理
    def get_html(self):
        while True:
            #从队列中获取地址
            self.lock.acquire()
            if not self.q.empty():
                headers = {'User-Agent':self.get_agent()}
                url = self.q.get()
                self.lock.release()
                html = requests.get(url=url,headers=headers).json()
                self.parse_html(html)
            else:
                self.lock.release()
                break

    def parse_html(self,html):
        item = {}
        for one_film in html:
            item['rank'] = one_film['rank']
            item['title'] = one_film['title']
            item['score'] = one_film['score']
            print(item)
            self.lock.acquire()
            self.i+=1
            self.lock.release()

    def run(self):
        # 先让url地址入队列
        self.url_in()
        #创建多线程
        t_list = []
        for i in range(10):
            t = Thread(target=self.get_html)
            t_list.append(t)
            t.start()
        for t in t_list:
            t.join()
        print("数量",self.i)

if __name__ == '__main__':
    start_time = time.time()
    spider = Douban()
    spider.run()
    end_time = time.time()
    print("执行时间%.2f"%(end_time-start_time))
