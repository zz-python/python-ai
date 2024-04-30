import requests
from bs4 import BeautifulSoup

# 定义要截取文字的网页 URL
url = 'https://haokan.baidu.com'

# 发送 GET 请求获取网页内容
response = requests.get(url)

# 检查响应状态码是否为 200（表示请求成功）
if response.status_code == 200:
    # 使用 BeautifulSoup 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    # 查找网页中的所有文本内容（即去除 HTML 标签后的纯文本）
    text = soup.get_text()
    # 输出截取到的网页文字
    print(text)
else:
    print('请求失败：', response.status_code)