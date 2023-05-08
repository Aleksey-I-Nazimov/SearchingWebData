# Scrapy settings for web_parser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.settings.default_settings import LOG_LEVEL

BOT_NAME = 'web_parser'

SPIDER_MODULES = ['web_parser.spiders']
NEWSPIDER_MODULE = 'web_parser.spiders'

# Logging
LOG_ENABLED = True
LOG_LEVEL = "INFO"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   #'Cookie': 'PHPSESSID=Z2pdOih9TP4CkKYuEQA8Xhlp7PuaT7x3; BITRIX_SM_book24_visitor_id=f7b0ab71-6ac5-49b9-bb89-b0ae6d022949; BITRIX_SM_location_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; BITRIX_SM_location_code=0c5b2444-70a0-4932-980c-b4dc0d3f02b5; BITRIX_SM_location_country=RU; BITRIX_SM_location_region_code=; BITRIX_SM_location_coords=%5B%2255.75396%22%2C%2237.620393%22%5D; ssaid=bf7028c0-ed87-11ed-bb00-19615ec167dc; tmr_lvid=8ae96aecd7eda718d9b27c60b074f1d2; tmr_lvidTS=1683540281210; _ga=GA1.2.1378711564.1683540281; _gid=GA1.2.264715469.1683540281; _ym_uid=1683540281142128905; _ym_d=1683540281; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=bea681c4-0975-4e15-a83c-7efe5ad4b872; st_uid=14423c7dce3c3c41a865a18bb18c339b; _ym_isad=2; g4c_x=1; flocktory-uuid=551f1b45-0839-4dc7-a33f-973e39955767-9; _tt_enable_cookie=1; _ttp=iySflexjIEyGjbsaJEqQpLvbzjN; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; adid=168354028446247; analytic_id=1683540284594243; mindboxDeviceUUID=ba06e495-40c9-42e6-ac7f-fc74db2501b2; directCrm-session=%7B%22deviceGuid%22%3A%22ba06e495-40c9-42e6-ac7f-fc74db2501b2%22%7D; tmr_detect=0%7C1683540426480; __tld__=null'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'web_parser.middlewares.WebParserSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'web_parser.middlewares.WebParserDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'web_parser.pipelines.WebParserPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
