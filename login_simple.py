"""
简单的今日头条登录脚本
直接调用auth模块进行登录
"""

import logging
from toutiao_mcp_server.auth import TouTiaoAuth

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    print("=" * 60)
    print("今日头条登录")
    print("=" * 60)
    print()
    print("注意事项:")
    print("1. 会自动打开 Chrome 浏览器窗口")
    print("2. 需要手动在浏览器中完成登录操作")
    print("3. 登录成功后浏览器会自动关闭")
    print("4. Cookie 会自动保存到本地文件")
    print()
    print("登录方式:")
    print("- 今日头条使用手机号 + 验证码登录")
    print("- 输入手机号后点击获取验证码")
    print("- 输入收到的验证码并点击登录")
    print()

    input("按回车键开始登录...")

    try:
        # 初始化认证管理器
        auth = TouTiaoAuth()

        # 执行登录
        print("\n正在打开浏览器...")
        success = auth.login_with_selenium()

        if success:
            print("\n✅ 登录成功!")
            print("Cookie 已保存,下次启动服务器会自动加载")

            # 检查登录状态
            is_logged_in = auth.check_login_status()
            print(f"登录状态验证: {'通过' if is_logged_in else '失败'}")
        else:
            print("\n❌ 登录失败或超时")
            print("请重试或检查网络连接")

    except Exception as e:
        print(f"\n❌ 登录过程出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
