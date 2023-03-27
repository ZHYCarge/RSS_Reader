import asyncio
import json
import time
from email.mime.multipart import MIMEMultipart
from config import logger, Config
import feedparser
import smtplib
from email.mime.text import MIMEText


async def send_email(subject,rss_title, message):
    """发送电子邮件"""
    msg = MIMEMultipart()
    msg['Subject'] = '[RSS小助手]' + f'[{rss_title}]'+subject
    msg['From'] = Config.EMAIL_ADDRESS
    msg['To'] = Config.RECIPIENT_ADDRESS
    msg.attach(MIMEText(message, 'html'))
    server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
    server.starttls()
    server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
    server.sendmail(Config.EMAIL_ADDRESS, Config.RECIPIENT_ADDRESS, msg.as_string())
    server.quit()
    logger.info(f"邮件`{subject}`已经成功发送！")


def read_RSSinfo():
    file = open(Config.FILE_PATH, 'r')
    content = json.loads(file.read())
    Config.RSS_FEED_URL = content['url']
    Config.RSS_FEEED_TITLE = content['title']
    file.close()


def write_RSSinfo():
    content = {}
    content['title'] = Config.RSS_FEEED_TITLE
    content['url'] = Config.RSS_FEED_URL
    file = open(Config.FILE_PATH, 'w')
    file.write(str(content).replace("'", "\""))
    file.close()


async def main():
    logger.debug('获取RSS源信息')
    for i in range(0, len(Config.RSS_FEED_URL)):
        logger.debug(f"这是第{i + 1}条url，链接为：{Config.RSS_FEED_URL[i]}")
        try:
            feed = feedparser.parse(Config.RSS_FEED_URL[i])
        except Exception as e:
            logger.warning(f"在获取{Config.RSS_FEED_URL[i]}订阅链接时出现错误{e},本次获取将跳过")
        else:
            if feed.entries:
                # 判断是否第一次执行
                if Config.RSS_FEED_URL[i] not in Config.RSS_FEEED_TITLE:
                    latest_entry = feed.entries[0]
                    Config.RSS_FEEED_TITLE[Config.RSS_FEED_URL[i]] = latest_entry.title

                    logger.info(f"已将RSS主题为{feed.feed.title}的第一次主题`{latest_entry.title}`添加到数据中")
                    # await send_email(latest_entry.title, latest_entry['summary'])
                else:
                    if Config.RSS_FEEED_TITLE[Config.RSS_FEED_URL[i]] != feed.entries[0].title:
                        for ii in range(0, len(feed.entries)):
                            latest_entry = feed.entries[ii]
                            if latest_entry.title == Config.RSS_FEEED_TITLE[Config.RSS_FEED_URL[i]]:
                                Config.RSS_FEEED_TITLE[Config.RSS_FEED_URL[i]] = feed.entries[0].title
                                break
                            else:
                                await send_email(latest_entry.title, feed.feed.title, latest_entry['summary'])
                    else:
                        logger.debug(f"RSS订阅地址：{Config.RSS_FEED_URL[i]}下没有最新信息")
            else:
                logger.info(f"RSS订阅地址：{Config.RSS_FEED_URL[i]}下没有信息，请查询后重试")


if __name__ == '__main__':
    while True:
        read_RSSinfo()
        asyncio.run(main())
        write_RSSinfo()
        time.sleep(Config.CHECK_INTERVAL)
