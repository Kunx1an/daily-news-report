#!/usr/bin/env python3
"""
每日资讯日报定时触发脚本

用途：
- 可独立运行，用于手动或定时触发日报推送
- 可部署到云函数（如阿里云函数计算、腾讯云 SCF）作为定时任务
- 可在服务器上通过 crontab 定时调用

使用方式：
1. 手动触发：python trigger_daily_report.py
2. crontab 定时：0 9 * * * cd /path/to/project && python trigger_daily_report.py
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_utils.log.write_log import setup_logging

# 配置日志
setup_logging(
    log_file="/app/work/logs/bypass/app.log",
    max_bytes=100 * 1024 * 1024,
    backup_count=5,
    log_level="INFO",
    use_json_format=True,
    console_output=True
)

logger = logging.getLogger(__name__)


async def run_daily_report():
    """
    执行每日资讯日报推送
    """
    logger.info("=" * 60)
    logger.info(f"📅 定时触发开始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # 创建上下文
        ctx = new_context(method="daily_news_report_trigger")
        
        # 导入并构建 Agent
        from agents.agent import build_agent
        
        logger.info("正在构建 Agent...")
        agent = build_agent(ctx)
        
        # 准备输入消息
        input_message = {
            "messages": [
                {"role": "user", "content": "请帮我获取今天的资讯日报并发送到飞书"}
            ]
        }
        
        # 生成唯一的 thread_id
        thread_id = f"daily_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        config = {"configurable": {"thread_id": thread_id}}
        
        logger.info(f"正在执行 Agent, thread_id: {thread_id}")
        
        # 执行 Agent
        result = await agent.ainvoke(input_message, config=config)
        
        # 记录结果
        logger.info("✅ 每日资讯日报推送完成")
        logger.info(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 提取最后的消息内容
        if result and "messages" in result:
            last_message = result["messages"][-1] if result["messages"] else None
            if last_message:
                content = getattr(last_message, "content", str(last_message))
                logger.info(f"Agent 响应: {content[:500]}..." if len(str(content)) > 500 else f"Agent 响应: {content}")
        
        return {
            "status": "success",
            "thread_id": thread_id,
            "timestamp": datetime.now().isoformat(),
            "result": str(result)[:1000] if result else None
        }
        
    except Exception as e:
        logger.error(f"❌ 定时触发执行失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def main():
    """主入口"""
    result = asyncio.run(run_daily_report())
    
    print("\n" + "=" * 60)
    print("执行结果:")
    print("=" * 60)
    print(f"状态: {result.get('status')}")
    print(f"时间: {result.get('timestamp')}")
    if result.get('status') == 'error':
        print(f"错误: {result.get('error')}")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    main()
