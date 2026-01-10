import os
import sys
from scrapy.cmdline import execute

# 获取当前脚本所在目录（bookschina目录）
base_dir = os.path.dirname(os.path.abspath(__file__))
# 切换到bookschina目录
os.chdir(base_dir)
# 将bookschina目录添加到Python路径
sys.path.append(base_dir)

execute(["scrapy","crawl","bsc_spider"])

