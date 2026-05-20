"""资讯搜索工具 - 搜索 AI 和财经领域的最新资讯"""

from langchain_core.tools import tool
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_utils.log.write_log import request_context
import json


@tool
def search_ai_news() -> str:
    """搜索 AI 人工智能领域的最新资讯。返回包含标题、来源、链接和摘要的资讯列表。"""
    ctx = request_context.get() or new_context(method="search_ai_news")
    
    client = SearchClient(ctx=ctx)
    
    # 搜索 AI 相关资讯，限制最近一天的内容
    response = client.search(
        query="AI 人工智能 大模型 最新动态",
        search_type="web",
        count=8,
        need_summary=True,
        time_range="1d"
    )
    
    results = []
    if response.web_items:
        for item in response.web_items:
            results.append({
                "title": item.title,
                "source": item.site_name,
                "url": item.url,
                "snippet": item.snippet[:200] if item.snippet else "",
                "summary": item.summary if item.summary else ""
            })
    
    return json.dumps(results, ensure_ascii=False, indent=2)


@tool
def search_finance_news() -> str:
    """搜索财经经济领域的最新资讯。返回包含标题、来源、链接和摘要的资讯列表。"""
    ctx = request_context.get() or new_context(method="search_finance_news")
    
    client = SearchClient(ctx=ctx)
    
    # 搜索财经相关资讯，限制最近一天的内容
    response = client.search(
        query="财经 经济 市场 最新动态",
        search_type="web",
        count=8,
        need_summary=True,
        time_range="1d"
    )
    
    results = []
    if response.web_items:
        for item in response.web_items:
            results.append({
                "title": item.title,
                "source": item.site_name,
                "url": item.url,
                "snippet": item.snippet[:200] if item.snippet else "",
                "summary": item.summary if item.summary else ""
            })
    
    return json.dumps(results, ensure_ascii=False, indent=2)
