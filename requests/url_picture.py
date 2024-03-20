from selenium import webdriver
# from PIL import Image

# 设置Selenium的webdriver路径，以及保存截图的路径
# webdriver_path = "chromedriver.exe"
save_path = "selenium-screenshot.png"
# 初始化webdriver https://chromedriver.chromium.org/downloads 下载chromedriver.exe放到平级目录
# 根据实际的版本下载 https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.59/win64/chromedriver-win64.zip
driver = webdriver.Chrome()
# 打开网页
url = "https://baidu.com"
# url = "https://blog.csdn.net/"
driver.get(url)
# 等待页面加载完成
driver.implicitly_wait(10)  # 这里设置等待时间为10秒，你可以根据实际情况调整
# 获取网页内容的尺寸
width = driver.execute_script("return document.body.scrollWidth")
height = driver.execute_script("return document.body.scrollHeight")
print(f"width = {width},height = {height}")
# 设置浏览器窗口大小
driver.set_window_size(width, height)
# 保存网页内容的截图
driver.save_screenshot(save_path)
# 打开截图并保存为图片文件
# screenshot = Image.open(save_path)
# screenshot.save("webpage_screenshot.png")
# print("Screenshot saved successfully!")