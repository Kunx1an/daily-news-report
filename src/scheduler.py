"""定时任务模块 - 每天早上 9 点自动触发资讯日报推送"""

import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from coze_coding_utils.runtime_ctx.context import new_context

logger = logging.getLogger(__name__)

# 全局调度器实例
scheduler = AsyncIOScheduler()


async def daily_news_report_job():
    """
    定时任务：每天早上 9 点自动获取资讯日报并推送到飞书
    """
    logger.info("=" * 50)
    logger.info(f"📅 定时任务触发: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("开始执行每日资讯日报推送...")
    logger.info("=" * 50)
    
    try:
        # 创建上下文
        ctx = new_context(method="daily_news_report")
        
        # 导入 Agent
        from agents.agent import build_agent
        
        # 构建 Agent
        agent = build_agent(ctx)
        
        # 准备输入消息
        input_message = {
            "messages": [
                {"role": "user", "content": "请帮我获取今天的资讯日报并发送到飞书"}
            ]
        }
        
        # 执行 Agent
        config = {"configurable": {"thread_id": f"daily_report_{datetime.now().strftime('%Y%m%d')}"}}
        
        result = await agent.ainvoke(input_message, config=config)
        
        # 记录结果
        logger.info("✅ 每日资讯日报推送完成")
        logger.info(f"执行结果: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ 定时任务执行失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise


def setup_scheduler():
    """
    配置定时调度器
    """
    # 添加定时任务：每天早上 9 点执行
    scheduler.add_job(
        daily_news_report_job,
        CronTrigger(hour=9, minute=0, timezone="Asia/Shanghai"),
        id="daily_news_report",
        name="每日资讯日报推送",
        replace_existing=True,
        misfire_grace_time=300,  # 如果错过触发时间，5分钟内仍然执行
    )
    
    logger.info("✅ 定时调度器配置完成")
    logger.info("📅 定时任务: 每天早上 9:00 (北京时间)")
    
    # 打印所有任务
    for job in scheduler.get_jobs():
        next_run = job.next_run_time if hasattr(job, 'next_run_time') else "pending"
        logger.info(f"   - {job.name}: {next_run}")


def start_scheduler():
    """
    启动定时调度器
    """
    setup_scheduler()
    scheduler.start()
    logger.info("🚀 定时调度器已启动")


def stop_scheduler():
    """
    停止定时调度器
    """
    scheduler.shutdown()
    logger.info("⏹️ 定时调度器已停止")


def get_scheduler_status():
    """
    获取调度器状态
    """
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run_time": str(job.next_run_time),
            "trigger": str(job.trigger),
        })
    
    return {
        "running": scheduler.running,
        "jobs": jobs
    }
