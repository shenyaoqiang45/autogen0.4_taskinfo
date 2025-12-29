"""
内容创作 Agent 系统主程序
"""
import asyncio
import logging
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .agents_clean import create_content_creation_team, create_selector_team
from .config import settings

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 Rich Console 用于美化输出
console = Console()


async def run_content_creation(
    topic: str,
    use_selector: bool = False,
    verbose: bool = True
) -> str:
    """运行内容创作流程
    
    Args:
        topic: 用户提供的主题
        use_selector: 是否使用 SelectorGroupChat（更灵活但成本更高）
        verbose: 是否显示详细输出
        
    Returns:
        创作素材的文本内容
    """
    # 显示开始信息
    if verbose:
        try:
            console.print(Panel.fit(
                f"[bold blue]开始内容创作流程[/bold blue]\n主题: {topic}",
                border_style="blue"
            ))
        except UnicodeEncodeError:
            # 控制台可能不支持某些 unicode 字符；记录并继续，不中断流程
            import re
            safe_name = re.sub(r'[^0-9A-Za-z_-]', '_', topic)[:120]
            logger.info("控制台不支持某些字符，跳过开始面板输出")
    
    try:
        # 创建团队
        if use_selector:
            logger.info("使用 SelectorGroupChat 模式")
            team = create_selector_team()
        else:
            logger.info("使用 RoundRobinGroupChat 模式")
            team = create_content_creation_team()
        
        # 运行团队
        if verbose:
            console.print("[yellow]Agent 团队正在工作...[/yellow]\n")
        
        # 执行任务
        result = await team.run(task=topic)
        
        # 提取结果
        messages = result.messages
        
        # 找到最后一条消息（通常是 Integrator 的输出）
        final_output = ""
        for msg in reversed(messages):
            if hasattr(msg, 'content') and msg.content:
                final_output = msg.content
                break
        
        if verbose:
            console.print("[green]内容创作完成！[/green]\n")
            try:
                console.print(Panel(
                    Markdown(final_output),
                    title="创作素材",
                    border_style="green"
                ))
            except UnicodeEncodeError:
                # Windows 控制台编码可能不支持某些 unicode 字符，回退为把结果写入文件并通过 logger 提示
                import re
                safe_name = re.sub(r'[^0-9A-Za-z_-]', '_', topic)[:120]
                out_path = f"output_{safe_name}.md"
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(final_output)
                logger.info(f"控制台不支持某些字符，已将输出写入: {out_path}")
        
        return final_output
        
    except Exception as e:
        logger.error(f"内容创作过程出错: {e}", exc_info=True)
        if verbose:
            console.print(f"[red]错误: {e}[/red]")
        raise


async def interactive_mode():
    """交互模式"""
    try:
        console.print(Panel.fit(
            "[bold cyan]内容创作 Agent 系统[/bold cyan]\n"
            "基于 AutoGen 0.4+\n"
            "输入主题，AI 自动补充时间、地点、人物和引用",
            border_style="cyan"
        ))
    except UnicodeEncodeError:
        logger.info("控制台不支持某些字符，跳过欢迎面板输出")
    
    while True:
        console.print("\n" + "="*50)
        topic = console.input("[bold]请输入主题（输入 'quit' 退出）: [/bold]")
        
        if topic.lower() in ['quit', 'exit', 'q']:
            console.print("[yellow]再见！[/yellow]")
            break
        
        if not topic.strip():
            console.print("[red]请输入有效的主题[/red]")
            continue
        
        try:
            await run_content_creation(topic, verbose=True)
        except Exception as e:
            console.print(f"[red]处理失败: {e}[/red]")
            continue


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        # 命令行模式
        topic = " ".join(sys.argv[1:])
        asyncio.run(run_content_creation(topic, verbose=True))
    else:
        # 交互模式
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
