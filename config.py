import sys
from loguru import logger

class Config:
    # 邮件配置
    SMTP_SERVER = ''  # SMTP服务器地址
    SMTP_PORT = 25  # SMTP服务器端口
    EMAIL_ADDRESS = ''  # 发件邮箱地址
    EMAIL_PASSWORD = ''  # 发件邮箱密码或者授权码
    RECIPIENT_ADDRESS = ''  # 收件邮箱地址 强烈推荐和发件邮箱地址一致，不然容易出现广告邮件导致无法发信成功！


    # RSS信息配置
    RSS_FEED_URL = ''
    RSS_FEEED_TITLE = {}
    CHECK_INTERVAL = 3600  # 检查间隔，单位为秒

    # 日志设置
    logger.remove()
    logger.add(sys.stderr, level='DEBUG') # 将level=debug的信息输出到控制台中
    logger.add('logs/error.log', retention='3 days')# 将level=debug的信息输出到logs/error.log文件中，并且输出日志信息仅保存3天

    # 其它配置
    FILE_PATH = 'rss.txt'  # 配置文件路径