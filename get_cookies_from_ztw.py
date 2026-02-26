#author:PIDUJING
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# 获取cookies函数
def get_cookies():
    try:
        # 创建Chrome选项
        options = webdriver.ChromeOptions()
        
        # 尝试自动获取Chrome浏览器路径（Windows系统）
        chrome_path = 'E:\Software\Google\Chrome\Application\chrome.exe'

        if chrome_path:
            print(f"找到了Chrome浏览器: {chrome_path}")
            options.binary_location = chrome_path
        else:
            print("警告：未找到默认安装的Chrome浏览器。请手动在代码中设置Chrome路径。")
            # 如果用户知道自己的Chrome路径，请取消下面这行的注释并修改为实际路径
            # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        
        # 使用webdriver_manager自动管理ChromeDriver
        service = Service(ChromeDriverManager().install())
        # 初始化Chrome浏览器
        driver = uc.Chrome(service=service, options=options)
        
        print("浏览器已启动，正在打开登录页面...")
        # 打开登录页面
        driver.get('https://www.bookschina.com/RegUser/login.aspx')
        
        # 等待页面加载
        time.sleep(6)
        
        print("开始输入用户名和密码...")
        # 输入用户名和密码
        driver.find_element(By.ID, 'userName').send_keys('17623322954')
        driver.find_element(By.ID, 'userPas').send_keys('pidujing123')
        
        # 点击登录按钮
        print("正在点击登录按钮...")
        driver.find_element(By.XPATH, '//*[@id="btnLogin"]/a').click()
        
        # 等待登录完成
        time.sleep(10)
        
        # 获取cookie
        cookies = driver.get_cookies()
        print(f"成功获取cookie，共{len(cookies)}个")
        print("Cookie信息:", cookies)
        
        # 关闭浏览器
        driver.quit()
        print("浏览器已关闭")
        
        return cookies
        
    except Exception as e:
        print(f"程序执行出错: {e}")
        return None

# 主程序
if __name__ == '__main__':
    print("===== 中图网登录cookie获取程序 =====")
    print("注意：请确保已在代码中替换为您的实际用户名和密码")
   
    cookies = get_cookies()
    
    if cookies:
        # 保存cookie到JSON文件
        with open('ztw_cookies-1.json', 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print("\n操作完成！已成功获取cookie信息并保存为JSON文件")
    else:
        print("\n操作失败，请检查错误信息")
