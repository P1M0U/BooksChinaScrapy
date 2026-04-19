# 📚 基于Scrapy框架的中图网图书数据爬虫

![项目状态](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Scrapy](https://img.shields.io/badge/scrapy-2.11%2B-green) ![MySQL](https://img.shields.io/badge/mysql-8.0%2B-blue) ![Fake_UserAgent](https://img.shields.io/badge/fake--useragent-1.5%2B-orange)

## 🚀 项目简介

**BooksChina 图书数据爬虫**是一个使用 Scrapy 框架开发的高性能爬虫，专门用于爬取中国图书网（BooksChina）的图书信息。该爬虫能够自动获取各类榜单数据，包括 24 小时热销榜、分类榜单等，并将完整的图书信息存储到 MySQL 数据库中，为图书数据分析和研究提供数据支持。

### ✨ 核心功能

- 📊 **多级榜单爬取**：支持爬取一级分类和二级分类榜单
- 🔄 **智能分页处理**：自动识别并爬取所有分页内容
- 💾 **MySQL 数据存储**：批量插入数据，高效处理大量图书信息
- 🔒 **反爬机制应对**：支持自定义 Cookies、随机 User-Agent、请求延迟等
- 📋 **丰富的数据字段**：包含图书标题、作者、价格、折扣、评分等 17 个关键字段
- 📝 **详细日志记录**：完整记录爬取过程和数据处理状态
- ⚡ **性能优化**：配置合理的并发请求和自动限速机制

## 🛠️ 技术栈

| 技术/库 | 版本 | 用途 |
|---------|------|------|
| Python | ^3.8 | 开发语言 |
| Scrapy | ^2.11.0 | 爬虫框架 |
| pymysql | ^1.1.0 | MySQL 数据库连接 |
| fake_useragent | ^1.5.0 | 生成随机 User-Agent |
| MySQL | ^8.0 | 数据存储 |

## 📁 项目结构

```
bookschina/
├── bookschina/                # 项目主目录
│   ├── __init__.py            # 初始化文件
│   ├── items.py               # 数据模型定义
│   ├── middlewares.py         # 中间件配置
│   ├── pipelines.py           # 数据处理管道
│   ├── settings.py            # 项目配置文件
│   └── spiders/               # 爬虫脚本目录
│       ├── __init__.py        # 爬虫初始化
│       └── bsc_spider.py      # 主爬虫实现
├── scrapy.cfg                 # Scrapy 配置文件
├── start_bsc_spider.py        # 启动脚本
├── README.md                  # 项目说明文档（中文）
└── README-EN.md               # 项目说明文档（英文）
```

## ⚙️ 快速开始

### 环境要求

- **Python**：3.8 或更高版本
- **MySQL**：8.0 或更高版本
- **依赖库**：见 requirements.txt

### 安装与运行

1. 克隆或下载项目到本地

2. 安装依赖
```bash
cd path/to/bookschina
pip install scrapy pymysql fake_useragent
```

3. 配置数据库连接
编辑 `bookschina/settings.py` 文件，修改 MySQL 连接信息：
```python
MYSQL_HOST = 'localhost'       # 数据库主机
MYSQL_USER = 'your_username'   # 数据库用户名
MYSQL_PASSWORD = 'your_password'  # 数据库密码
MYSQL_DATABASE = 'your_database'  # 数据库名称
MYSQL_PORT = 3306              # 数据库端口
CHARSET = 'utf8mb4'            # 字符集
```

4. 配置 Cookies（可选）
将你的 Cookies 文件保存为项目支持的格式，或修改 `bsc_spider.py` 中的 Cookies 加载路径。

5. 启动爬虫
```bash
python start_bsc_spider.py
```

## 📊 数据模型

### 爬取的图书字段

| 字段名 | 类型 | 说明 |
|-------|------|------|
| book_id | 字符串 | 图书唯一标识 |
| title | 字符串 | 图书标题 |
| author | 字符串 | 作者信息 |
| publisher | 字符串 | 出版社 |
| publish_date | 字符串 | 出版日期 |
| price | 字符串/数字 | 图书价格 |
| one_star_price | 字符串/数字 | 一星价格 |
| three_star_price | 字符串/数字 | 三星价格 |
| discount | 字符串/数字 | 折扣信息 |
| reader_ratings | 字符串 | 读者评分 |
| rating_num | 字符串 | 评分数量 |
| is_stock | 字符串 | 库存状态 |
| free_shipping | 字符串 | 包邮信息 |
| level_1_category | 字符串 | 一级分类 |
| level_2_category | 字符串 | 二级分类 |
| ranking | 字符串 | 所属榜单名称 |
| ranking_num | 字符串 | 在榜单中的排名 |

### 数据库表结构

爬虫会自动创建或使用以下表结构（如果已存在）：

```sql
CREATE TABLE books_tb (
    book_id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    free_shipping VARCHAR(255),
    author VARCHAR(255),
    price VARCHAR(50),
    one_star_price VARCHAR(50),
    three_star_price VARCHAR(50),
    discount VARCHAR(50),
    reader_ratings VARCHAR(50),
    rating_num VARCHAR(50),
    is_stock VARCHAR(50),
    level_1_category VARCHAR(100),
    level_2_category VARCHAR(100),
    publisher VARCHAR(255),
    publish_date VARCHAR(100),
    ranking VARCHAR(255),
    ranking_num VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🔍 爬虫工作流程

1. **初始化**：加载 Cookies 和配置信息
2. **起始请求**：访问 24 小时热销榜页面
3. **解析榜单**：提取一级和二级分类榜单链接
4. **分页处理**：解析每个榜单的总页数并生成所有分页链接
5. **列表解析**：从分页页面提取图书详情链接
6. **详情爬取**：访问每个图书的详情页，提取完整信息
7. **数据处理**：通过 Pipeline 处理和批量存储数据
8. **完成统计**：输出爬取结果统计信息

## ⚡ 性能优化

- **并发请求**：配置 `CONCURRENT_REQUESTS = 16` 提高爬取效率
- **域名限制**：每个域名最多同时 6 个请求，避免对服务器压力过大
- **随机延迟**：使用 0.8-2.0 秒的随机延迟，减少被反爬风险
- **自动限速**：启用 AutoThrottle 自动调整请求速度
- **批量插入**：每 20 条数据批量插入数据库，提高存储效率
- **失败重试**：配置自动重试机制，应对临时网络问题

## 🚀 部署建议

### 生产环境部署

1. **配置优化**：
   - 根据服务器性能调整并发参数
   - 增加日志记录到文件
   - 设置更合理的延迟时间

2. **定期运行**：
   - 使用定时任务定期运行爬虫更新数据
   - 示例（Windows 计划任务）：
     ```
     python path/to/bookschina/start_bsc_spider.py
     ```

## 🔧 常见问题与解决方案

### 爬取速度过慢
- 检查网络连接
- 调整 `CONCURRENT_REQUESTS` 和 `DOWNLOAD_DELAY` 参数
- 确保数据库性能良好

### 反爬拦截
- 使用有效的 Cookies
- 增加随机延迟时间
- 修改 User-Agent 生成策略

### 数据存储失败
- 检查数据库连接配置
- 确保数据库用户有足够权限
- 查看错误日志获取具体信息

## 📝 开发指南

### 添加新的爬取字段
1. 在 `items.py` 中的 `BookschinaItem` 类添加新字段
2. 在 `bsc_spider.py` 的 `parse_info` 方法中提取该字段
3. 更新 `pipelines.py` 中的 `_batch_insert` 方法的 SQL 语句

### 修改爬取范围
- 调整 `start_urls` 列表以添加新的起始页面
- 修改 `parse_ranking` 方法以适应不同的榜单结构

## 📜 许可证

本项目采用 MIT 许可证 - 详情请查看 LICENSE 文件

## 📧 联系方式

- 项目地址：[Github](https://github.com/P1M0U/BooksChinaScrapy/)
- 个人邮箱：[P1M0U](mailto:p1m0u@foxmail.com)
- 如果觉得对你有用，麻烦请您帮我点一下star ⭐

---

感谢使用 BooksChina 图书数据爬虫！🎉