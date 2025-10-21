#!/usr/bin/env python3
"""
今日头条内容发布工具
使用方法: python publish.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from pathlib import Path

def load_cookies():
    """加载登录 cookies"""
    cookie_file = Path("toutiao_cookies.json")
    if cookie_file.exists():
        with open(cookie_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('cookies', [])
    return []

def publish_weitoutiao(content, auto_publish=False):
    """
    发布微头条

    Args:
        content: 要发布的内容
        auto_publish: 是否自动点击发布按钮（默认 False，需要手动确认）
    """
    print("\n" + "=" * 60)
    print("🚀 今日头条微头条发布工具")
    print("=" * 60)

    # 检查登录状态
    cookies = load_cookies()
    if not cookies:
        print("\n❌ 未找到登录凭证！")
        print("请先运行: python login_simple.py")
        return False

    print(f"\n✅ 找到登录凭证 ({len(cookies)} 个 cookies)")

    # 初始化浏览器
    print("\n[1/5] 启动浏览器...")
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # 如果需要无头模式，取消下面的注释
    # options.add_argument('--headless')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(1920, 1080)
        print("✅ 浏览器启动成功")
    except Exception as e:
        print(f"❌ 浏览器启动失败: {e}")
        return False

    try:
        # 设置登录状态
        print("\n[2/5] 设置登录状态...")
        driver.get("https://mp.toutiao.com")
        time.sleep(2)

        for cookie in cookies:
            try:
                cookie_dict = {
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie.get('domain', '.toutiao.com')
                }
                if 'path' in cookie:
                    cookie_dict['path'] = cookie['path']
                driver.add_cookie(cookie_dict)
            except:
                pass

        print("✅ 登录状态设置完成")

        # 访问微头条发布页面
        print("\n[3/5] 打开发布页面...")
        url = "https://mp.toutiao.com/profile_v4/weitoutiao/publish?from=toutiao_pc"
        driver.get(url)
        time.sleep(8)

        # 检查是否需要重新登录
        if "login" in driver.current_url:
            print("❌ 登录状态已过期，请重新登录")
            print("运行: python login_simple.py")
            return False

        print("✅ 发布页面加载成功")

        # 查找编辑器
        print("\n[4/5] 填充内容...")
        editor = None
        wait = WebDriverWait(driver, 10)

        # 按优先级尝试不同的选择器
        selectors = [
            ".ProseMirror",
            "[contenteditable='true']",
            "div[role='textbox']",
            "textarea"
        ]

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    if elem.is_displayed() and elem.is_enabled():
                        editor = elem
                        print(f"✅ 找到编辑器: {selector}")
                        break
                if editor:
                    break
            except:
                continue

        if not editor:
            print("❌ 未找到编辑器元素")
            driver.save_screenshot("error_no_editor.png")
            print("已保存错误截图: error_no_editor.png")
            print("\n⏸️  浏览器将保持打开30秒供检查...")
            time.sleep(30)
            return False

        # 填充内容
        try:
            # 点击编辑器获取焦点
            editor.click()
            time.sleep(1)

            # 使用 JavaScript 设置内容
            driver.execute_script(
                "arguments[0].innerText = arguments[1];",
                editor,
                content
            )

            # 触发 input 事件确保内容被识别
            driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                editor
            )

            time.sleep(2)
            print("✅ 内容填充成功")

        except Exception as e:
            print(f"❌ 内容填充失败: {e}")
            return False

        # 保存预览截图
        driver.save_screenshot("publish_preview.png")
        print("✅ 预览截图已保存: publish_preview.png")

        print("\n[5/5] 发布状态...")
        print("\n" + "=" * 60)
        print("📝 发布内容预览:")
        print("-" * 60)
        print(content)
        print("-" * 60)

        if auto_publish:
            # 自动点击发布按钮
            print("\n正在尝试自动发布...")
            try:
                # 查找发布按钮
                publish_selectors = [
                    "button.publish-btn",
                    "button[class*='publish']",
                    "//button[contains(text(), '发布')]",
                    "//button[contains(text(), '发表')]"
                ]

                publish_btn = None
                for selector in publish_selectors:
                    try:
                        if selector.startswith("//"):
                            buttons = driver.find_elements(By.XPATH, selector)
                        else:
                            buttons = driver.find_elements(By.CSS_SELECTOR, selector)

                        for btn in buttons:
                            if btn.is_displayed() and btn.is_enabled():
                                publish_btn = btn
                                break
                        if publish_btn:
                            break
                    except:
                        continue

                if publish_btn:
                    publish_btn.click()
                    print("✅ 已点击发布按钮")
                    time.sleep(3)
                    print("✅ 发布完成！")
                else:
                    print("⚠️  未找到发布按钮，请手动点击")
                    time.sleep(30)
            except Exception as e:
                print(f"⚠️  自动发布失败: {e}")
                print("请手动点击发布按钮")
                time.sleep(30)
        else:
            # 手动发布模式
            print("\n✅ 内容已填充！")
            print("\n请在浏览器中:")
            print("  1. 检查内容是否正确")
            print("  2. 添加话题标签（可选）")
            print("  3. 点击「发布」按钮完成发布")
            print("\n浏览器将保持打开60秒...")
            time.sleep(60)

        return True

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot("error.png")
        print("错误截图已保存: error.png")
        return False

    finally:
        print("\n关闭浏览器...")
        driver.quit()
        print("✅ 完成！")


def main():
    """主函数"""
    print("\n" + "🎯" * 30)
    print("欢迎使用今日头条发布工具")
    print("🎯" * 30)

    # 示例内容
    default_content = """🎉 测试发布

这是通过自动化工具发布的内容！

✨ 发布时间: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """

#测试 #自动化"""

    print("\n请选择操作:")
    print("1. 使用示例内容发布（快速测试）")
    print("2. 输入自定义内容发布")
    print("0. 退出")

    choice = input("\n请选择 (0-2): ").strip()

    if choice == "1":
        print("\n使用示例内容:")
        print("-" * 60)
        print(default_content)
        print("-" * 60)
        confirm = input("\n确认发布？(y/n): ").strip().lower()
        if confirm == 'y':
            publish_weitoutiao(default_content, auto_publish=False)
        else:
            print("已取消")

    elif choice == "2":
        print("\n请输入要发布的内容（输入 END 结束）:")
        print("-" * 60)
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        content = "\n".join(lines)
        if content.strip():
            print("\n将要发布的内容:")
            print("-" * 60)
            print(content)
            print("-" * 60)
            confirm = input("\n确认发布？(y/n): ").strip().lower()
            if confirm == 'y':
                publish_weitoutiao(content, auto_publish=False)
            else:
                print("已取消")
        else:
            print("内容为空，已取消")

    elif choice == "0":
        print("退出")

    else:
        print("无效选择")


if __name__ == "__main__":
    main()

