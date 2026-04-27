import os
import smtplib
import sys
import json
import zipfile
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
# -*- coding: utf-8 -*-
import sys
import io

# 设置标准输出为 UTF-8 编码（解决 Windows 控制台 emoji 问题）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 这行代码会将项目根目录（apiobj140）添加到 Python 的搜索路径中
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.environment import sender_email, password_email, EMAIL_SERVER, PORT


def get_allure_stats_from_results(allure_results_dir):
    """
    从 Allure 的原始 results 目录中读取测试统计数据

    :param allure_results_dir: Allure 原始结果目录路径（包含 -result.json 文件的目录）
    :return: (total, passed, failed, skipped)
    """
    total = 0
    passed = 0
    failed = 0
    skipped = 0

    results_path = Path(allure_results_dir)

    if not results_path.exists():
        print(f"⚠️ Allure results 目录不存在: {allure_results_dir}")
        return 0, 0, 0, 0

    # 遍历所有 -result.json 文件
    result_files = list(results_path.glob("*-result.json"))

    for result_file in result_files:
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                total += 1
                status = data.get('status', 'unknown')

                if status == 'passed':
                    passed += 1
                elif status == 'failed':
                    failed += 1
                elif status == 'skipped':
                    skipped += 1
        except Exception as e:
            print(f"⚠️ 读取文件失败 {result_file}: {e}")

    print(f"📊 从 Allure results 读取到: 总数={total}, 通过={passed}, 失败={failed}, 跳过={skipped}")
    return total, passed, failed, skipped


def send_test_report(receiver_email, allure_results_dir=None, report_url=None):
    """
    发送测试报告（自动从 Allure results 读取统计数据）

    :param receiver_email: 收件人邮箱
    :param allure_results_dir: Allure 原始结果目录的路径（如 ./report/data）
    :param report_url: 在线报告的链接
    """
    # 如果没有指定 results 目录，使用默认路径
    if allure_results_dir is None:
        allure_results_dir = "report/data"

    # 从 Allure results 读取真实统计数据
    if Path(allure_results_dir).exists():
        total, passed, failed, skipped = get_allure_stats_from_results(allure_results_dir)
    else:
        print(f"⚠️ 未找到 Allure results 目录: {allure_results_dir}")
        total, passed, failed, skipped = 0, 0, 0, 0

    # 如果没有测试数据，不发送邮件
    if total == 0:
        print("❌ 没有找到任何测试结果，取消发送邮件")
        return

    msg = EmailMessage()
    msg["Subject"] = f"接口自动化测试报告 - 通过: {passed}/{total}"
    msg["From"] = formataddr(("测试小助手", f"{sender_email}"))
    msg["To"] = receiver_email

    # 计算通过率
    pass_rate = (passed / total * 100) if total > 0 else 0

    # 准备邮件正文（HTML格式，包含统计信息）
    html_content = f"""
    <html>
      <body>
        <h2>🤖 自动化测试执行完成</h2>
        <p>您好，本次接口自动化测试已执行完毕。</p>

        <pre>
📊 测试执行结果：
-----------------------------------
🌟 总用例数: {total}
✅ 通过: {passed}
❌ 失败: {failed}
⏭ 跳过: {skipped}
-----------------------------------
📈 通过率: {pass_rate:.1f}%
        </pre>
    """

    if report_url:
        html_content += f'<p>📊 <a href="{report_url}">点击查看详细 Allure 报告</a></p>'

    html_content += """
        <hr>
        <p>⭐ 此邮件由自动化脚本自动发送，请勿回复。</p>
      </body>
    </html>
    """

    msg.set_content("您的邮箱客户端不支持查看HTML内容，请升级客户端。")
    msg.add_alternative(html_content, subtype="html")

    # 发送邮件
    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print(f"✅ 测试报告邮件已发送至: {receiver_email}")


# 使用示例（直接调用）
send_test_report(
    receiver_email="2301857691@qq.com",
    allure_results_dir="allure-results",  # 指定 Allure 原始结果目录
    report_url="http://172.31.52.35:8080/job/apiobj140/allure/"
)
