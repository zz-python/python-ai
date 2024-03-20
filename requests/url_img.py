import requests
from bs4 import BeautifulSoup
import os

def download_images(url, save_folder):
    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    if response.status_code == 200:
        # 使用Beautiful Soup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # 提取所有图片链接
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            # 下载图片
            img_url = 'https:' + img_url
            print(f"下载图片2：{img_url}")
            download_image(img_url, save_folder)

def download_image(img_url, save_folder):
    # 发送HTTP请求下载图片
    response = requests.get(img_url)
    if response.status_code == 200:
        # 构造保存路径
        img_name = img_url.split('/')[-1]
        save_path = os.path.join(save_folder, img_name)
        # 保存图片到本地
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"下载完成：{img_name}")

if __name__ == "__main__":
    url = 'https://baidu.com'
    save_folder = 'F:/test_img'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    download_images(url, save_folder)
