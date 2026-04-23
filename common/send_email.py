import os
import smtplib
import sys
import zipfile
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

# 这行代码会将项目根目录（apiobj140）添加到 Python 的搜索路径中
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.environment import sender_email, password_email, EMAIL_SERVER, PORT


# ... (dotenv 和变量读取部分保持不变) ...

def send_test_report(receiver_email, allure_report_dir=None, report_url=None):
    """
    发送测试报告
    :param receiver_email: 收件人邮箱
    :param allure_report_dir: 本地 Allure 报告目录的路径（如 ./allure-report）
    :param report_url: 在线报告的链接（如 http://jenkins.xxx.com/job/xxx/allure）
    """
    msg = EmailMessage()
    msg["Subject"] = "接口自动化测试报告"
    msg["From"] = formataddr(("测试小助手", f"{sender_email}"))
    msg["To"] = receiver_email

    # 1. 准备邮件正文（HTML格式）
    html_content = """
    <html>
      <body>
        <h2>🤖 自动化测试执行完成</h2>
        <p>您好，本次接口自动化测试已执行完毕。</p>
    """

    # 如果提供了在线报告链接，就把链接加到正文里
    if report_url:
        html_content += f'<p>📊 <a href="{report_url}">点击查看详细 Allure 报告</a></p>'

    html_content += """
        <hr>
        <p>⭐ 此邮件由自动化脚本自动发送，请勿回复。</p>
      </body>
    </html>
    """

    msg.set_content("您的邮箱客户端不支持查看HTML内容，请升级客户端。")  # 纯文本备用
    msg.add_alternative(html_content, subtype="html")

    # 2. 如果有本地报告目录，则打包并添加为附件
    if allure_report_dir and Path(allure_report_dir).exists():
        zip_path = "allure-report.zip"
        # 把整个报告目录压缩成 zip 文件
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(allure_report_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=allure_report_dir)
                    zipf.write(file_path, arcname)

        # 读取 zip 文件并添加到邮件附件
        with open(zip_path, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='zip',
                filename='allure-report.zip'
            )
        # 可选：清理临时 zip 文件
        # os.remove(zip_path)

    # 3. 发送邮件（这部分你的原代码没问题）
    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())


# 使用示例
# send_email_script.py 末尾直接写（不用 if __name__）
send_test_report(
    receiver_email="647079757@qq.com",
    report_url="http://172.31.52.35:8080/job/apiobj140/allure/"
)
