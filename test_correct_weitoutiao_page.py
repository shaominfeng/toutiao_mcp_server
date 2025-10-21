"""
测试正确的微头条发布页面
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from pathlib import Path

def load_cookies():
    """加载保存的 cookies"""
    cookie_file = Path("toutiao_cookies.json")
    if cookie_file.exists():
        with open(cookie_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('cookies', [])
    return []

def test_correct_weitoutiao_page():
    """测试正确的微头条发布页面"""
    print("=" * 60)
    print("测试正确的微头条发布页面")
    print("=" * 60)

    # 初始化浏览器
    print("\n[1] 初始化浏览器...")
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 不使用无头模式，方便观察
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)
    print("✅ 浏览器初始化成功")

    try:
        # 先访问主页并设置 cookies
        print("\n[2] 访问主页并设置 cookies...")
        driver.get("https://mp.toutiao.com")
        time.sleep(2)

        cookies = load_cookies()
        print(f"📝 找到 {len(cookies)} 个 cookies")

        for cookie in cookies:
            try:
                cookie_dict = {
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie.get('domain', '.toutiao.com')
                }
                if 'path' in cookie:
                    cookie_dict['path'] = cookie['path']
                if 'secure' in cookie:
                    cookie_dict['secure'] = cookie['secure']
                if 'httpOnly' in cookie:
                    cookie_dict['httpOnly'] = cookie['httpOnly']

                driver.add_cookie(cookie_dict)
            except Exception as e:
                pass

        print("✅ Cookies 设置完成")

        # 访问正确的微头条发布页面
        print("\n[3] 访问微头条发布页面...")
        correct_url = "https://mp.toutiao.com/profile_v4/weitoutiao/publish?from=toutiao_pc"
        driver.get(correct_url)
        print(f"✅ 已访问: {correct_url}")

        # 等待页面加载
        print("\n[4] 等待页面加载（15秒）...")
        time.sleep(15)

        current_url = driver.current_url
        print(f"当前URL: {current_url}")

        # 检查是否重定向到登录页
        if "login" in current_url or "auth" in current_url:
            print("❌ 页面重定向到登录页")
            screenshot_path = "correct_page_login_required.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 截图已保存: {screenshot_path}")
            return

        print("✅ 页面未重定向，正常加载")

        # 尝试查找所有可能的编辑器元素
        print("\n[5] 查找编辑器元素...")

        selectors_to_try = [
            ".ProseMirror",
            "textarea",
            "[contenteditable='true']",
            "div[role='textbox']",
            ".syl-editor",
            ".wtt-publish-wrap",
            ".publish-box",
            "div[class*='editor']",
            "div[class*='publish']",
        ]

        found_elements = []
        for selector in selectors_to_try:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for elem in elements:
                        if elem.is_displayed():
                            found_elements.append({
                                'selector': selector,
                                'tag': elem.tag_name,
                                'class': elem.get_attribute('class'),
                                'id': elem.get_attribute('id'),
                                'placeholder': elem.get_attribute('placeholder'),
                                'displayed': elem.is_displayed(),
                                'enabled': elem.is_enabled()
                            })
                            print(f"\n✅ 找到元素: {selector}")
                            print(f"   标签: {elem.tag_name}")
                            print(f"   Class: {elem.get_attribute('class')}")
                            print(f"   ID: {elem.get_attribute('id')}")
                            print(f"   Placeholder: {elem.get_attribute('placeholder')}")
                            break
            except Exception as e:
                pass

        if not found_elements:
            print("\n❌ 未找到任何编辑器元素")
        else:
            print(f"\n✅ 总共找到 {len(found_elements)} 个可能的编辑器元素")

        # 保存页面源代码
        print("\n[6] 保存调试文件...")
        with open("correct_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ 页面源代码已保存: correct_page_source.html")

        # 保存截图
        screenshot_path = "correct_page_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"✅ 截图已保存: {screenshot_path}")

        # 保存找到的元素信息
        if found_elements:
            with open("found_elements.json", "w", encoding="utf-8") as f:
                json.dump(found_elements, f, indent=2, ensure_ascii=False)
            print("✅ 元素信息已保存: found_elements.json")

        print("\n" + "=" * 60)
        print("测试完成！浏览器将保持打开30秒供查看")
        print("=" * 60)
        time.sleep(30)

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

        screenshot_path = "correct_page_error.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 错误截图已保存: {screenshot_path}")

    finally:
        print("\n关闭浏览器...")
        driver.quit()
        print("✅ 浏览器已关闭")

if __name__ == "__main__":
    test_correct_weitoutiao_page()

