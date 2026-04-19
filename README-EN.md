# 📚 BooksChina Book Data Crawler Based on the Scrapy Framework

![Project Status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Scrapy](https://img.shields.io/badge/scrapy-2.11%2B-green) ![MySQL](https://img.shields.io/badge/mysql-8.0%2B-blue) ![Fake_UserAgent](https://img.shields.io/badge/fake--useragent-1.5%2B-orange)

## 🚀 Project Introduction

**BooksChina Book Data Crawler** is a high-performance web crawler developed using the Scrapy framework, specifically designed to crawl book information from BooksChina (China's book website). The crawler can automatically retrieve various ranking data, including 24-hour bestseller lists, category rankings, etc., and store complete book information in a MySQL database, providing data support for book data analysis and research.

### ✨ Core Features

- 📊 **Multi-level Ranking Crawling**: Supports crawling of primary and secondary category rankings
- 🔄 **Intelligent Pagination Handling**: Automatically identifies and crawls all paginated content
- 💾 **MySQL Data Storage**: Bulk inserts data for efficient processing of large amounts of book information
- 🔒 **Anti-crawler Mechanism Handling**: Supports custom Cookies, random User-Agent, request delays, etc.
- 📋 **Rich Data Fields**: Contains 17 key fields including book title, author, price, discount, rating, etc.
- 📝 **Detailed Logging**: Complete records of crawling process and data processing status
- ⚡ **Performance Optimization**: Configured with reasonable concurrent requests and automatic rate limiting mechanism

## 🛠️ Technology Stack

| Technology/Library | Version | Purpose |
|--------------------|---------|--------|
| Python | ^3.8 | Development language |
| Scrapy | ^2.11.0 | Crawler framework |
| pymysql | ^1.1.0 | MySQL database connection |
| fake_useragent | ^1.5.0 | Generate random User-Agent |
| MySQL | ^8.0 | Data storage |

## 📁 Project Structure

```
bookschina/
├── bookschina/                # Project main directory
│   ├── __init__.py            # Initialization file
│   ├── items.py               # Data model definition
│   ├── middlewares.py         # Middleware configuration
│   ├── pipelines.py           # Data processing pipeline
│   ├── settings.py            # Project configuration file
│   └── spiders/               # Crawler scripts directory
│       ├── __init__.py        # Crawler initialization
│       └── bsc_spider.py      # Main crawler implementation
├── scrapy.cfg                 # Scrapy configuration file
├── start_bsc_spider.py        # Startup script
├── README.md                  # Project documentation (Chinese)
└── README-EN.md               # Project documentation (English)
```

## ⚙️ Quick Start

### Environment Requirements

- **Python**: 3.8 or higher
- **MySQL**: 8.0 or higher
- **Dependencies**: See requirements.txt

### Installation and Running

1. Clone or download the project to your local machine

2. Install dependencies
```bash
cd path/to/bookschina
pip install scrapy pymysql fake_useragent
```

3. Configure database connection
Edit the `bookschina/settings.py` file to modify MySQL connection information:
```python
MYSQL_HOST = 'localhost'       # Database host
MYSQL_USER = 'your_username'   # Database username
MYSQL_PASSWORD = 'your_password'  # Database password
MYSQL_DATABASE = 'your_database'  # Database name
MYSQL_PORT = 3306              # Database port
CHARSET = 'utf8mb4'            # Character set
```

4. Configure Cookies (optional)
Save your Cookies file in the project-supported format, or modify the Cookies loading path in `bsc_spider.py`.

5. Start the crawler
```bash
python start_bsc_spider.py
```

## 📊 Data Model

### Crawled Book Fields

| Field Name | Type | Description |
|------------|------|------------|
| book_id | String | Book unique identifier |
| title | String | Book title |
| author | String | Author information |
| publisher | String | Publisher |
| publish_date | String | Publication date |
| price | String/Number | Book price |
| one_star_price | String/Number | One-star member price |
| three_star_price | String/Number | Three-star member price |
| discount | String/Number | Discount information |
| reader_ratings | String | Reader ratings |
| rating_num | String | Rating count |
| is_stock | String | Stock status |
| free_shipping | String | Free shipping information |
| level_1_category | String | Primary category |
| level_2_category | String | Secondary category |
| ranking | String | Ranking list name |
| ranking_num | String | Ranking position |

### Database Table Structure

The crawler will automatically create or use the following table structure (if it already exists):

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

## 🔍 Crawler Workflow

1. **Initialization**: Load Cookies and configuration information
2. **Start Request**: Access the 24-hour bestseller list page
3. **Parse Rankings**: Extract primary and secondary category ranking links
4. **Pagination Handling**: Parse the total number of pages for each ranking and generate all pagination links
5. **List Parsing**: Extract book detail links from pagination pages
6. **Detail Crawling**: Visit each book's detail page and extract complete information
7. **Data Processing**: Process and bulk store data through Pipeline
8. **Completion Statistics**: Output crawling result statistics

## ⚡ Performance Optimization

- **Concurrent Requests**: Configured with `CONCURRENT_REQUESTS = 16` to improve crawling efficiency
- **Domain Limitation**: Maximum 6 concurrent requests per domain to avoid excessive pressure on the server
- **Random Delays**: Using random delays of 0.8-2.0 seconds to reduce anti-crawler risks
- **Auto Throttling**: Enabling AutoThrottle to automatically adjust request speed
- **Bulk Insertion**: Batch inserting data into the database every 20 records to improve storage efficiency
- **Failure Retry**: Configured with automatic retry mechanism to handle temporary network issues

## 🚀 Deployment Recommendations

### Production Environment Deployment

1. **Configuration Optimization**:
   - Adjust concurrent parameters according to server performance
   - Increase logging to files
   - Set more reasonable delay times

2. **Regular Running**:
   - Use scheduled tasks to run the crawler regularly to update data
   - Example (Windows Task Scheduler):
     ```
     python path/to/bookschina/start_bsc_spider.py
     ```

## 🔧 Common Issues and Solutions

### Slow Crawling Speed
- Check network connection
- Adjust `CONCURRENT_REQUESTS` and `DOWNLOAD_DELAY` parameters
- Ensure good database performance

### Anti-crawler Interception
- Use valid Cookies
- Increase random delay time
- Modify User-Agent generation strategy

### Data Storage Failure
- Check database connection configuration
- Ensure database user has sufficient permissions
- View error logs for specific information

## 📝 Development Guide

### Adding New Crawling Fields
1. Add new fields to the `BookschinaItem` class in `items.py`
2. Extract the field in the `parse_info` method of `bsc_spider.py`
3. Update the SQL statement in the `_batch_insert` method of `pipelines.py`

### Modifying Crawling Scope
- Adjust the `start_urls` list to add new starting pages
- Modify the `parse_ranking` method to adapt to different ranking structures

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details

## 📧 Contact Information

- Project Address: [Github](https://github.com/P1M0U/BooksChinaScrapy/)
- If you find this project useful, please give me a star ⭐

---

Thank you for using BooksChina Book Data Crawler! 🎉