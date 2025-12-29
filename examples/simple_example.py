"""
简单示例：使用内容创作 Agent 系统

这个示例展示如何使用系统为一个主题生成创作素材
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import run_content_creation


async def main():
    """运行简单示例"""
    
    # 示例主题
    topics = [
        "第一次工业革命",
        "人工智能在医疗领域的应用",
        "中国春节习俗",
        "钱学森的航天事业",
    ]
    
    print("=" * 60)
    print("内容创作 Agent 系统 - 简单示例")
    print("=" * 60)
    
    # 让用户选择或输入主题
    print("\n可选的示例主题:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic}")
    print("0. 自定义主题")
    
    choice = input("\n请选择（输入数字）: ").strip()
    
    if choice == "0":
        topic = input("请输入自定义主题: ").strip()
    elif choice.isdigit() and 1 <= int(choice) <= len(topics):
        topic = topics[int(choice) - 1]
    else:
        print("无效选择，使用默认主题")
        topic = topics[0]
    
    print(f"\n选择的主题: {topic}\n")
    
    # 运行内容创作
    try:
        result = await run_content_creation(
            topic=topic,
            use_selector=False,  # 使用简单的轮询模式
            verbose=True
        )
        
        # 可选：将结果保存到文件
        output_file = f"output_{topic[:20]}.md".replace(" ", "_").replace("/", "_")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        
        print(f"\n结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
