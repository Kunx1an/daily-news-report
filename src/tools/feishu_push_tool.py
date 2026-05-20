"""飞书消息推送工具 - 将资讯日报推送到飞书群"""

import json
import requests
from langchain_core.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context


# 飞书机器人 Webhook URL
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/1b707f8e-61ca-4f2e-a742-b902d2c7d1c5"


def _get_webhook_url() -> str:
    """获取飞书 Webhook URL"""
    # 优先尝试从集成配置获取
    try:
        from coze_workload_identity import Client
        client = Client()
        credential = client.get_integration_credential("integration-feishu-message")
        if credential:
            return json.loads(credential).get("webhook_url", FEISHU_WEBHOOK_URL)
    except Exception:
        pass
    
    # 使用默认的 webhook URL
    return FEISHU_WEBHOOK_URL


def _send_feishu_message(payload: dict) -> dict:
    """发送飞书消息的底层方法"""
    webhook_url = _get_webhook_url()
    response = requests.post(webhook_url, json=payload, timeout=10)
    return response.json()


@tool
def send_daily_report_to_feishu(report_content: str) -> str:
    """
    将每日资讯日报发送到飞书群。
    
    Args:
        report_content: 格式化好的日报内容（Markdown格式）
    
    Returns:
        发送结果的描述
    """
    ctx = request_context.get() or new_context(method="send_daily_report_to_feishu")
    
    # 构建飞书富文本消息
    # 将 Markdown 内容转换为飞书富文本格式
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "📰 每日资讯日报",
                    "content": [
                        [
                            {"tag": "text", "text": report_content}
                        ]
                    ]
                }
            }
        }
    }
    
    try:
        result = _send_feishu_message(payload)
        if result.get("StatusCode") == 0:
            return "✅ 日报已成功发送到飞书群"
        else:
            return f"❌ 发送失败: {result}"
    except Exception as e:
        return f"❌ 发送异常: {str(e)}"


@tool
def send_news_card_to_feishu(title: str, content: str, news_items: str) -> str:
    """
    发送格式化的资讯卡片到飞书群。
    
    Args:
        title: 卡片标题
        content: 卡片内容摘要
        news_items: JSON格式的资讯列表，包含每条资讯的标题、来源、链接
    
    Returns:
        发送结果的描述
    """
    ctx = request_context.get() or new_context(method="send_news_card_to_feishu")
    
    try:
        # 解析资讯列表
        items = json.loads(news_items) if isinstance(news_items, str) else news_items
        
        # 构建卡片元素
        elements = []
        
        # 添加摘要内容
        if content:
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            })
        
        # 添加每条资讯
        for item in items[:10]:  # 最多显示10条
            item_title = item.get("title", "无标题")
            item_source = item.get("source", "")
            item_url = item.get("url", "")
            
            # 构建资讯条目
            if item_url:
                news_text = f"**[{item_title}]({item_url})**"
            else:
                news_text = f"**{item_title}**"
            
            if item_source:
                news_text += f" _{item_source}_"
            
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": news_text
                }
            })
        
        # 发送交互式卡片
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    },
                    "template": "blue"
                },
                "elements": elements
            }
        }
        
        result = _send_feishu_message(payload)
        if result.get("StatusCode") == 0:
            return f"✅ 资讯卡片「{title}」已成功发送"
        else:
            return f"❌ 发送失败: {result}"
    except Exception as e:
        return f"❌ 发送异常: {str(e)}"
