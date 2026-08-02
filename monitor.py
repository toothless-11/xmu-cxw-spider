import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header
import sys

MAIL_USER = os.environ.get('MAIL_USER')
MAIL_PASS = os.environ.get('MAIL_PASS')
URL = "https://cxw.xmu.edu.cn/cms/0qRRjDIv4uaDz4FcwMRk00-1"

# ========== 收件人列表（改成你的） ==========
recipients_str = os.environ.get('MAIL_RECIPIENTS')
if recipients_str:
    # 如果有值，按逗号分割，并去除每个邮箱地址前后的空格
    RECIPIENTS = [email.strip() for email in recipients_str.split(',') if email.strip()]
else:
    # 如果环境变量未设置，给出一个明确的提示并退出，或者设置一个开发测试用的默认列表
    print("错误：未配置 MAIL_RECIPIENTS 环境变量，请先设置收件人邮箱列表。", flush=True)
    sys.exit(1)  # 退出程序
# =========================================

def send_email(title, link):
    print(f">>> 正在发送邮件给 {len(RECIPIENTS)} 个收件人...", flush=True)
    if not MAIL_USER or not MAIL_PASS:
        print("错误：未配置 MAIL_USER 或 MAIL_PASS 变量", flush=True)
        return

    msg = MIMEText(f"发现新比赛：{title}\n\n详情链接：{link}", 'plain', 'utf-8')
    msg['Subject'] = Header("【科创提醒】" + title[:20], 'utf-8')
    msg['From'] = MAIL_USER
    msg['To'] = ", ".join(RECIPIENTS)

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(MAIL_USER, MAIL_PASS)
        server.sendmail(MAIL_USER, RECIPIENTS, msg.as_string())
        server.quit()
        print(f">>> 邮件发送成功！", flush=True)
    except Exception as e:
        print(f">>> 邮件发送失败: {e}", flush=True)

def main():
    print(">>> 脚本启动", flush=True)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        res = requests.get(URL, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        news_item = soup.find('li', class_='news')
        if not news_item:
            print("未找到比赛列表", flush=True)
            return

        topic_span = news_item.find('span', class_='topic')
        a_tag = news_item.find('a')
        
        title = topic_span.get_text(strip=True).replace('>', '', 1)
        link = a_tag['href']
        if not link.startswith('http'):
            link = "https://cxw.xmu.edu.cn" + link

        print(f">>> 抓取到最新标题: {title}", flush=True)

        fname = "notified_ids.txt"
        notified_ids = set()

        if os.path.exists(fname):
            with open(fname, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        notified_ids.add(line)

        current_id = link.split('/')[-1]
        print(f">>> 当前比赛ID: {current_id}", flush=True)

        if current_id not in notified_ids:
            print(f">>> 发现新比赛！", flush=True)
            send_email(title, link)
            notified_ids.add(current_id)
            with open(fname, 'w', encoding='utf-8') as f:
                for id in notified_ids:
                    f.write(id + '\n')
            print(">>> 状态已更新", flush=True)
        else:
            print(f">>> 比赛已通知过，跳过", flush=True)

    except Exception as e:
        print(f">>> 运行出错: {e}", flush=True)

if __name__ == "__main__":
    main()
