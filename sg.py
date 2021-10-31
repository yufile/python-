import requests, json, threading, time, os
# requests 请求数据 json 用来将接口数据转为json数据 使用线程threading模块  time 时间戳 os 识别电脑路径查找文件夹和创建文件夹
from queue import Queue  # 使用队列


class Picture(threading.Thread):  # 创建一个自定义线程类Picture,继承Thread
    # 初始化
    def __init__(self, num, search, url_queue=None):  # 默认如果没有传值就不使用队列
        super().__init__()  # 调用父类的所有方法 threading.Thread(他是传过来的模块) 使用父类的线程方法 使用了这个super.__init__()通过self可以调用父类的所有方法
        # 相当于构造函数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.90 Safari/537.36 '
        }
        self.num = num
        self.search = search

    # 获取爬取的页数的每页图片接口url
    def get_url(self):
        url_list = []
        for start in range(self.num):
            # 多少页 从0开始循环 start 携带参数https://pic.sogou.com/pics?query=动漫&mode=1&start=0&reqType=ajax&reqFrom=result&tn=0
            url = 'https://pic.sogou.com/pics?query=' + self.search + '&mode=1&start=' + str(
                start * 48) + '&reqType=ajax&reqFrom=result&tn=0'
            url_list.append(url)  # 将获取的每页的接口数据存储
        return url_list

    # 获取每页的接口资源详情
    def get_page(self, url):
        response = requests.get(url, headers=self.headers)  # 获取接口数据
        return response.text  # 将数据返回

    #
    def run(self):
        while True:
            # 如果队列为空代表制定页数爬取完毕
            if url_queue.empty():
                break
            else:
                url = url_queue.get()  # 本页地址 获取当前页队列
                data = json.loads(self.get_page(url))  # 获取到本页图片接口资源 将接口数据转为json数据
                # 处理异常
                try:
                    # 每页48张图片
                    for i in range(1, 49):
                        pic = data['items'][i]['pic_url']
                        reponse = requests.get(pic)  # get请求图片

                        # 如果文件夹不存在，则创建 查找文件夹如果存在就打开 不存在重新创建
                        if not os.path.exists(r'D:/tupian' + self.search):
                            os.mkdir(r'D:/tupian' + self.search)
                            #  文件名后面拼接上搜索后缀  格式化写入通过时间并且将 '.' 分割成为'_'
                        with open(r'D:/tupian' + self.search + '/%s.jpg' % (str(time.time()).replace('.', '_')),
                                  'wb') as f:
                            f.write(reponse.content)  # 将图片写入目录中
                            print('下载成功！')
                # 线程结束之后会抛出异常
                except:
                    print('该页图片保存完毕')


if __name__ == '__main__':
    # 1.获取初始化的爬取url
    num = int(input('请输入爬取页数（每页48张）：'))
    content = input('请输入爬取内容：')
    pic = Picture(num, content)  # 实例化对象
    url_list = pic.get_url()  # 将请求地址返回 每页的数据接口 共多少页
    # 2.创建队列
    url_queue = Queue()
    for i in url_list:
        url_queue.put(i)  # 如果队列满了，那么使用put放入数据会等待，直到队列有空闲位置才可以放入
    # 3.创建线程任务 使用多线程比单线程要快很多
    crawl = [1, 2, 3, 4, 5]
    for i in crawl:
        pic = Picture(num, content, url_queue=url_queue)  # 三个参数第一个是传入的页数 第二个是 搜索内容 第三个是队列 通过 super.__init__ 继承调用
        pic.start()  # 开启线程
