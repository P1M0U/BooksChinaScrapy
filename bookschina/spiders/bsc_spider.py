import scrapy 
import re
import random
import json
import fake_useragent
import os
from urllib.parse import urlparse
from datetime import datetime    # 添加datetime导入
from ..items import BookschinaItem
class BscSpiderSpider(scrapy.Spider):
    name = "bsc_spider"
    allowed_domains = ["www.bookschina.com"]
    start_urls = ["https://www.bookschina.com/24hour/"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cookie = self.load_cookies()
        self.logger.debug(f"初始化完成，已加载 {len(self.cookie)} 个cookie")
        self.ua = fake_useragent.UserAgent()
        self.success_count = 0
    def load_cookies(self):
        try:
            with open('D:\\ztw_cookies.json', 'r', encoding='utf-8') as f:
                cookies_list = json.load(f)
                cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}
                self.logger.debug(f"成功加载{len(cookies_dict)}个Cookie")
                return cookies_dict
        except Exception as e:
            self.logger.error(f"加载Cookie失败: {e}")
            return {}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse_ranking,
                headers={'User-Agent': self.ua.random,'Referer': 'https://www.bookschina.com/'},
                cookies=self.cookie,
                dont_filter=True
            )
    def closed(self, reason):
        self.logger.warning(f"爬虫关闭原因: {reason}")
        self.logger.info(f"共成功获取{self.success_count}条数据")
    def parse_ranking(self, response):
        self.logger.debug(f"开始解析榜单页面: {response.url}")
        ranking_list = []
        for row in response.xpath('//div[@class="bookListInner"]/ul[@class="booktop"]/li'):
            ranking_url = row.xpath('./dl/dt/a/@href').get()
            ranking_name = row.xpath('./dl/dt/a/text()').get()
            ranking_url = response.urljoin(ranking_url)
            self.logger.debug(f"正在获取一级分类榜单{ranking_name},URL: {ranking_url}")
            ranking_list.append({
                'name': ranking_name,
                'url': ranking_url
            })
            for link in row.xpath('./dl/dd/a'):
                ranking_url = link.xpath('./@href').get()
                ranking_name = link.xpath('./text()').get()
                ranking_url = response.urljoin(ranking_url)
                self.logger.debug(f"正在获取二级分类榜单{ranking_name},URL: {ranking_url}")
                ranking_list.append({
                    'name': ranking_name,
                    'url': ranking_url
            })
        for ranking in ranking_list:
            yield scrapy.Request(
                ranking['url'], 
                callback=self.parse_page,
                headers={'User-Agent': self.ua.random},
                cookies=self.cookie,
                dont_filter=True,
                meta={'ranking_name': ranking['name']}
            )

    def parse_page(self,response):
        self.logger.debug(f"开始解析榜单翻页: {response.meta.get('ranking_name')}")
        page_num = response.xpath('//div[@class="pagination"]/div[@class="paging"]/div[@class="p-skip"]/em/b/text()').get()
        if page_num is None:
            self.logger.warning(f"榜单{response.meta.get('ranking_name')}没有分页信息,可能只有一页")
            page_num = 1
        else:
            page_num = int(page_num.strip())
        self.logger.debug(f"{response.meta.get('ranking_name')}榜单总共有{page_num}页")
        parsed_url = urlparse(response.url)
        current_path = parsed_url.path
        for page in range(1,page_num+1):
            #https://www.bookschina.com/24hour/shaoer/1_0_2/
            #https://www.bookschina.com/24hour/48000000/30_0_1/
            if '_' in current_path:
                base_path = current_path.rsplit('/', 2)[0] + '/'
            else:
                base_path = current_path
            page_url = response.urljoin(f"{base_path}1_0_{page}/")
            self.logger.debug(f"正在获取榜单{response.meta.get('ranking_name')},第{page}页,URL: {page_url}")
            yield scrapy.Request(
                page_url,
                callback=self.parse_list,
                headers={'User-Agent': self.ua.random,'Referer': response.url},
                cookies=self.cookie,
                dont_filter=True,
                meta={'ranking_name': response.meta.get('ranking_name'),
                'page':page}
            )
        
    def parse_list(self,response):
        self.logger.debug(f" 当前是{response.meta.get('ranking_name')}榜单的第{response.meta.get('page')}页,响应码{response.status}")
        # book_list = []
        for row in response.xpath('//div[@id="container"]/div[@class="listMain clearfix"]/div[@class="listLeft"]/div[@class="bookList"]/ul/li'):
            info_url = row.xpath('./div[@class="infor"]/h2/a/@href').get()
            if info_url is None:
                self.logger.warning(f"没有书籍ID信息,URL: {info_url}")
                continue
            match = re.search(r'/(\d+)\.htm',info_url)
            if not match:
                self.logger.warning(f"无法从URL中提取书籍ID: {info_url}，跳过此书")
                continue
            book_id = match.group(1)
            info_url = response.urljoin(info_url)
            # info_url = "https://www.bookschina.com/"+info_url
            self.logger.info(f"获取到书籍详情页URL: {info_url}")
            title = row.xpath('./div[@class="infor"]/h2/a/text()').get()
            author = row.xpath('./div[@class="infor"]/div[@class="author"]/a/text()').get()
            if author is None:
                author = "佚名"
            else:
                author = author.strip()
            rating_num = row.xpath('./div[@class="infor"]/div[@class="startWrap"]/a/text()').get()
            if rating_num is None:
                rating_num = "0条评论"
            else:
                rating_num = rating_num.strip()
            self.logger.debug(f"列表页中获取到书籍ID: {book_id},书名: {title},作者: {author},评论数: {rating_num}")
            yield scrapy.Request(
                info_url,
                callback=self.parse_info,
                headers={'User-Agent': self.ua.random,'Referer': response.url},
                cookies=self.cookie,
                dont_filter=True,
                meta={
                'book_id': book_id,
                'title': title,
                'author': author,
                'rating_num': rating_num}
            )

    def parse_info(self,response):
        self.logger.debug(f"开始解析书籍信息:ID {response.meta.get('book_id')},书名：{response.meta.get('title')},响应码{response.status}")
        title = response.meta.get('title')
        author = response.meta.get('author')
        rating_num = response.meta.get('rating_num')
        try:
            # 提取书籍信息
            for row in response.xpath('//div[@class="bookInfo"]'):       
                free_shipping = row.xpath('./div[@class="padLeft10"]/h1/span/text()').get()
                if free_shipping is None:
                    free_shipping = "不包邮"
                publisher = row.xpath('./div[@class="padLeft10"]/div[@class="publisher"]/a/text()').get()
                if publisher is None:
                    publisher = "未知出版社"
                else:
                    publisher = publisher.strip()
                publish_date = row.xpath('./div[@class="padLeft10"]/div[@class="publisher"]/i/text()').get()
                if publish_date and publish_date.strip() == "暂无":
                        publish_date = None

                reader_ratings = row.xpath('./div[@class="padLeft10"]/div[@class="startWrap"]/em/text()').get()
                if reader_ratings is None:
                    reader_ratings = "暂无评分"
                else:
                    reader_ratings = reader_ratings.strip()

                ranking = row.xpath('./div[@class="padLeft10"]/div[@class="sort"]/a/text()').get()
                if ranking is None:
                    ranking = "无"
                else:
                    ranking = ranking.strip()
                    
                ranking_num = row.xpath('./div[@class="padLeft10"]/div[@class="sort"]/b/i/text()').get()
                if ranking_num is None:
                    ranking_num = "无"
                else:
                    ranking_num = ranking_num.strip()
                    
                price = row.xpath('./div[@class="priceWrap"]/del[@class="price"]/text()').get()
                if price is None:
                    price = "0"
                else:
                    price = price.replace("\xa0¥", "").strip()
                    
                one_star_price = row.xpath('./div[@class="priceWrap"]/span[@class="sellPrice"]/text()').get()
                if one_star_price is None:
                    one_star_price = "0"
                    
                three_star_price = row.xpath('./div[@class="priceWrap"]/span[@class="bestPrice"]/text()').get()
                if three_star_price is None:
                    three_star_price = "0"
                else:
                    three_star_price = three_star_price.replace("三星价 \xa0¥", "")
                    
                discount = row.xpath('./div[@class="priceWrap"]/span[@class="discount"]/text()').get()
                if discount is None:
                    discount = response.xpath('//*[@id="PurWarp"]/div/i/text()').get()
                    if discount is None:
                            discount = "0.0"
                if discount is not None:
                    discount = str(discount).strip()
                    match = re.search(r'\d+\.?\d*', discount)
                    if match:
                        discount = match.group()
                    else:
                        self.logger.error(f"解析折扣时出错: 折扣{discount}")
                    
                is_stock = row.xpath('./div[@class="oparateButton clearfix"]/a[1]/text()').get()
                if is_stock == "加入购物车":
                    is_stock = "有库存"
                elif is_stock == "暂时缺货":
                    is_stock = "缺货"
                else:
                    is_stock = "未知"
                    
                level_1_category = response.xpath('//div[@class="crumbsNav clearfix"]/div[2]/a/text()').get()
                if level_1_category is None:
                    level_1_category = "无"
                    level_2_category = "无"
                else:
                    level_2_category = response.xpath('//div[@class="crumbsNav clearfix"]/div[3]/a/text()').get()
                    if level_2_category is None:
                        level_2_category = level_1_category
                    # 创建并填充item
                item = BookschinaItem()
                item['book_id'] = response.meta.get('book_id')
                item['title'] = title
                item['free_shipping'] = free_shipping
                item['author'] = author
                item['publisher'] = publisher
                item['publish_date'] = publish_date
                item['one_star_price'] = one_star_price
                item['three_star_price'] = three_star_price
                item['discount'] = discount
                item['price'] = price
                item['reader_ratings'] = reader_ratings
                item['rating_num'] = rating_num
                item['is_stock'] = is_stock
                item['level_1_category'] = level_1_category
                item['level_2_category'] = level_2_category
                item['ranking'] = ranking
                item['ranking_num'] = ranking_num
                print(item)
                self.success_count += 1
                yield item
                if self.success_count % 20 == 0:
                    self.logger.info(f"已成功爬取 {self.success_count} 条数据")
                    
        except Exception as e:
            self.logger.error(f"解析书籍信息出错(ID: {response.meta.get('book_id')}): {e}")
