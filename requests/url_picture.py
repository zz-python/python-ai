from selenium import webdriver
from PIL import Image

# 设置Selenium的webdriver路径，以及保存截图的路径
webdriver_path = "F:/chromedriver.exe"
save_path = "screenshot.png"

# 初始化webdriver
driver = webdriver.Chrome(webdriver_path)

# 打开网页
url = "https://baidu.com"
driver.get(url)

# 等待页面加载完成
driver.implicitly_wait(10)  # 这里设置等待时间为10秒，你可以根据实际情况调整

# 获取网页内容的尺寸
width = driver.execute_script("return document.body.scrollWidth")
height = driver.execute_script("return document.body.scrollHeight")

# 设置浏览器窗口大小
driver.set_window_size(width, height)

# 保存网页内容的截图
driver.save_screenshot(save_path)

# 关闭浏览器
driver.quit()

# 打开截图并保存为图片文件
screenshot = Image.open(save_path)
screenshot.save("webpage_screenshot.png")

print("Screenshot saved successfully!")
