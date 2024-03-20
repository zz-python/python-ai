python -m venv venv
venv\Scripts\activate

url_picture：截图url网页整体图像  
https://chromedriver.chromium.org/downloads 下载chromedriver.exe放到平级目录  
根据实际的版本下载 https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.59/win64/chromedriver-win64.zip  
pip install selenium pillow

```
attrs             23.2.0
certifi           2024.2.2
cffi              1.16.0
exceptiongroup    1.2.0
h11               0.14.0
idna              3.6
outcome           1.3.0.post0
pillow            10.2.0
pycparser         2.21
PySocks           1.7.1
selenium          4.18.1
sniffio           1.3.1
sortedcontainers  2.4.0
trio              0.25.0
trio-websocket    0.11.1
typing-extensions 4.10.0
urllib3           2.2.1
wsproto           1.2.0
```

url_img：爬取url关联的img图像  
pip install requests beautifulsoup4
