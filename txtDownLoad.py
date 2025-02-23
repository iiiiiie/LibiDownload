import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_chrome_options():
    options = Options()
    options.add_experimental_option('detach', True)
    # 指向 selenium 官方下载的 Chrome（便携版）
    options.binary_location = os.path.join(os.getcwd(), "chrome-win64", "chrome.exe")
    options.add_argument('--no-sandbox')
    return options


def create_webdriver():
    driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=get_chrome_options())
    driver.implicitly_wait(30)
    driver.set_page_load_timeout(180)
    driver.minimize_window()
    return driver

print("""该软件为开源软件，如果你是购买的，请立即退款并举报投诉

软件为：v1.0版本

作用是下载https://www.wenkuchina.com/的小说，也就是【轻之文库轻小说、哩哔轻小说】，中的小说，下载文字到txt文件中

作者：ie

b站网址：https://space.bilibili.com/27683010

视频教程：

github链接为：

使用方式：复制任意一本小说的需要开始下载的页面的地址，也就是说，你复制的是第一章的链接，就会从第一章开始下载，从第20章复制的链接，就会从第20章开始下载


错误一般是网络错误，想要断点续传的
    可以打开文档查看你下载到哪了，然后从那里往后一章开始
    如果不会的话可以把txt删掉，从头开始下载
    如果还不会的话可以看视频教程

目前情况与后续计划：仅保证了能正常下载，多线程等我之后有空会做的，插图下载我没需要，如果有人需要的话我会考虑做一下

================================================================================================
""")

# pyinstaller -F .\txtDownLoad.py

# 起始页 URL
START_PAGE_URL = input('输入你要下载的页面：')

# 'https://www.wenkuchina.com/lightnovel/3586/162098.html'
def main():
    driver = create_webdriver()
    driver.get(START_PAGE_URL)

    # 获取目录页 URL，用于判断是否下载完成以及显示进度
    driver.get(driver.find_element(By.PARTIAL_LINK_TEXT, '目录').get_attribute('href'))
    catalogue_url=driver.find_element(By.PARTIAL_LINK_TEXT,'开始阅读').get_attribute('href')
    driver.get(catalogue_url)

    # 获取所有章节链接元素
    chapter_elements = driver.find_elements(By.CSS_SELECTOR, '.col-4 a')
    # 提取每个章节链接的 href 属性存入列表
    chapter_urls = [elem.get_attribute('href') for elem in chapter_elements]

    # 返回起始页，开始下载章节
    driver.get(START_PAGE_URL)

    while True:
        current_url = driver.current_url

        # 进度显示
        if current_url in chapter_urls:
            index = chapter_urls.index(current_url)
            print(f"当前下载进度：{int((index + 1) / len(chapter_urls) * 100)}%")

        # 判断是否下载完成：比较当前 URL 与目录页 URL
        if current_url == catalogue_url:
            print('全部下载完成')
            driver.quit()
            break

        # 移除页面中所有 <ins> 和 <iframe> 标签（避免广告干扰）
        driver.execute_script("""
            var elems = document.querySelectorAll('ins, iframe');
            elems.forEach(function(el) { el.remove(); });
        """)

        print(f'当前 URL：{driver.current_url}')
        title = driver.find_element(By.CSS_SELECTOR, '#mlfy_main_text > h1').text
        content = driver.find_element(By.CSS_SELECTOR, '#TextContent').text

        with open(f'{driver.find_element(By.XPATH,'/html/body/div[1]/div/div/a[3]').text}.txt', 'a', encoding='utf-8') as f:
            f.write(title + '\n')
            f.write(f'{driver.current_url}\n' + content + '\n\n')

        # 点击“下一”
        driver.find_element(By.PARTIAL_LINK_TEXT, '下一').click()


if __name__ == '__main__':
    main()

# todo: 多线程下载

# todo: 插图也下载,我感觉插图不是很必要，至少我不看，看看有没有人想要自动下载这个插图，如果有的话我写一下插图的逻辑，没有人想要就算了
