# -*- coding: utf-8 -*-
import requests
import re

"""
自我认知：
    对于cookie的获取不太明白，需要掌握怎么取获取网页的cookie 以及什么叫做cookie.jar 还有怎么去自己构造cookie
    对于数据持久化不太熟练 尤其是csv文件保存，有点生疏，
    ajxs的网址怎么去分析出他的实际地址
    简单数据清洗
"""
"""
    需求1：获取一下信息
        'city': 城市
        'companyFullName': 公司名
        'companySize': 公司规模
        'education': 学历
        'positionName': 职位名称
        'salary': 薪资
        'workYear': 工作时间

    需求2：以逗号（,）分割信息内容，写入文件。要求文件名为 `拉钩职位信息.csv`。
    例如：
        上海,上海沸橙信息科技有限公司,150-500人,本科,python,8k-12k,不限
        """


# 构造请求头
class LGSpider:

    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        self.url_real = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        self.headers_real = {
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

        }

    # 获取Cooike
    def get_cookie(self):
        """

        :return:  返回cookie 的jar值
        """
        cookie = requests.get(url=self.url, headers=self.headers, allow_redirects=False).cookies
        return cookie

    # 构建表单
    def data(self, first='false', kd='python', pn='1'):
        """

        :param first:
        :param kd: 关键字 爬取的职位 默认为爬取pyhton
        :param pn:  爬取的页数 默认爬取一页
        :return:
        """
        data_real = {
            'first': first,
            'pn': pn,
            'kd': kd,
        }
        return data_real

    # 请求原始网址
    def post_lg(self, real_data):

        print('*' * 50 + 'data:' + '*' * 50, real_data)
        response = requests.post(url=self.url_real, headers=self.headers_real, data=real_data,
                                 cookies=self.get_cookie())
        return response.json()

    # 数据解析
    def parsel_lg(self, real_data, position):
        """

        :param real_data: 构造的请求表单，详见main函数
        :param position: 为了保存的信息
        :return:
        """
        response_json = self.post_lg(real_data)
        lg_data_lis = response_json['content']['positionResult']['result']
        for da in lg_data_lis:
            lg_data = []
            lg_data.append(da['city'])
            lg_data.append(da['companyFullName'])
            lg_data.append(da['companySize'])
            lg_data.append(da['education'])
            lg_data.append(da['positionName'])
            lg_data.append(da['salary'])
            lg_data.append([da['workYear'][:-1]])
            lg_data_str = str(lg_data)
            lg_data_str_done = re.sub("\[|\]|\'", "", lg_data_str)
            print(lg_data_str_done)
            self.save_lg_data(lg_data_str_done, position)

    def write_head(self, position):
        with open(f'{position}拉钩.csv', mode='w', encoding='utf-8', newline='') as fp:
            fp.write("city,companyFullName,companySize,education,positionName,salary,workYear" + '\n')

    # 数据持久化 保存成csv格式
    def save_lg_data(self, lg_data_str_done, position):
        with open(f'{position}拉钩.csv', mode='a', encoding='utf-8', newline='') as fp:
            fp.writelines(lg_data_str_done + '\n')

    # 启动函数
    def main(self, page=5, kd='python'):
        self.write_head(kd)
        for page in range(page):
            real_data = self.data(pn=str(page), kd=kd)
            position = real_data.get('kd')
            self.parsel_lg(real_data, position)
            # position = real_data.get('kd')
            print(f"----正在爬取第{page}页的{position}职位的招聘信息-----")


if __name__ == '__main__':
    Spider = LGSpider()
    kd = input("你想爬取的职位:")
    pn = int(input("爬取的页数:"))
    Spider.main(kd=kd, page=pn)

# cookie = requests.get("https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=", headers={
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
#                       allow_redirects=False).cookies
# print(cookie)
