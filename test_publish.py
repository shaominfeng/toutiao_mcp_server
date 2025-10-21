"""
今日头条内容发布测试脚本
"""

from toutiao_mcp_server.auth import TouTiaoAuth
from toutiao_mcp_server.publisher import TouTiaoPublisher

def test_login_status():
    """测试登录状态"""
    print("=" * 60)
    print("1. 检查登录状态")
    print("=" * 60)

    auth = TouTiaoAuth()
    is_logged_in = auth.check_login_status()

    if is_logged_in:
        print("✅ 已登录")
        user_info = auth.get_user_info()
        if user_info:
            print(f"用户信息: {user_info}")
    else:
        print("❌ 未登录,请先运行 python login_simple.py 登录")
        return False

    return True

def test_publish_micro_post():
    """测试发布微头条"""
    print("\n" + "=" * 60)
    print("2. 测试发布微头条")
    print("=" * 60)

    auth = TouTiaoAuth()
    publisher = TouTiaoPublisher(auth)

    # 发布一条简单的测试微头条
    content = """
🎉 今日头条 MCP 服务器测试

这是一条通过 MCP 服务器自动发布的测试微头条!

✨ 主要功能:
• 自动登录管理
• 内容智能发布
• 多平台兼容

#科技 #自动化 #测试
    """.strip()

    print(f"\n准备发布内容:\n{content}\n")

    result = publisher.publish_micro_post(
        content=content,
        images=None,  # 如果有图片,可以传入图片路径列表
        topic="科技"
    )

    print(f"\n发布结果: {result}")

    if result.get('success'):
        print("✅ 微头条发布成功!")
    else:
        print(f"❌ 发布失败: {result.get('message')}")

    return result

def test_publish_article():
    """测试发布图文文章"""
    print("\n" + "=" * 60)
    print("3. 测试发布图文文章")
    print("=" * 60)

    auth = TouTiaoAuth()
    publisher = TouTiaoPublisher(auth)

    title = "今日头条 MCP 服务器使用指南"

    content = """
# 今日头条 MCP 服务器

## 简介

这是一个功能完整的今日头条内容管理 MCP 服务器,支持:

- 🔐 自动登录管理
- 📝 内容智能发布
- 📊 数据分析统计
- 🌐 多平台兼容

## 主要特性

### 1. 自动化发布
支持图文文章和微头条的自动发布,提高内容创作效率。

### 2. 多平台兼容
完全兼容小红书自动发布工具的数据格式,支持一键多平台发布。

### 3. 数据分析
提供详细的数据分析和报告生成功能,帮助优化内容策略。

## 快速开始

1. 安装依赖: `pip install -r requirements.txt`
2. 登录账号: `python login_simple.py`
3. 发布内容: 使用 MCP 工具或 API 接口

## 总结

今日头条 MCP 服务器是一个强大的内容管理工具,适合个人创作者和团队使用。

---
本文由 MCP 服务器自动发布 🚀
    """.strip()

    print(f"\n准备发布文章:")
    print(f"标题: {title}")
    print(f"内容长度: {len(content)} 字符\n")

    result = publisher.publish_article(
        title=title,
        content=content,
        images=None,  # 如果有图片,可以传入图片路径列表
        tags=["科技", "工具", "自动化"],
        category="科技",
        original=True
    )

    print(f"\n发布结果: {result}")

    if result.get('success'):
        print("✅ 文章发布成功!")
    else:
        print(f"❌ 发布失败: {result.get('message')}")

    return result

def main():
    """主函数"""
    print("\n🚀 今日头条内容发布测试\n")

    # 1. 检查登录状态
    if not test_login_status():
        return

    # 2. 选择测试类型
    print("\n" + "=" * 60)
    print("请选择测试类型:")
    print("=" * 60)
    print("1. 发布微头条(推荐,快速简单)")
    print("2. 发布图文文章(复杂,需要更多参数)")
    print("3. 两者都测试")
    print("0. 退出")

    choice = input("\n请输入选项 (0-3): ").strip()

    if choice == "1":
        test_publish_micro_post()
    elif choice == "2":
        test_publish_article()
    elif choice == "3":
        test_publish_micro_post()
        print("\n" + "-" * 60 + "\n")
        input("按回车键继续测试文章发布...")
        test_publish_article()
    elif choice == "0":
        print("退出测试")
    else:
        print("无效选项")

    print("\n测试完成! 🎉")

if __name__ == "__main__":
    main()
