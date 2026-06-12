#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信AI知识管理平台 - 主程序
基于FastAPI框架
"""

import os
import json
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# 项目路径配置
PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
EXPORT_DIR = Path(r"F:\软件安装\WorkBuddy项目储存\2026-05-31-task-29\wechat-decrypt\export")

# 创建FastAPI应用
app = FastAPI(
    title="微信AI知识管理平台",
    description="实时读取微信聊天记录、自动脱敏、AI分析销冠话术、知识沉淀",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=PROJECT_DIR / "static"), name="static")

# 配置模板引擎
templates = Jinja2Templates(directory=PROJECT_DIR / "templates")

# ============ 数据模型 ============

class Contact(BaseModel):
    """联系人模型"""
    id: int
    username: str
    nick_name: str
    remark: Optional[str] = None
    alias: Optional[str] = None
    type: str
    display_name: str
    message_count: int = 0
    last_active: Optional[str] = None
    brand: Optional[str] = None

class Message(BaseModel):
    """消息模型"""
    id: str
    contact_id: str
    content: str
    message_type: int
    send_time: str
    is_from_me: bool

class FAQItem(BaseModel):
    """FAQ项目模型"""
    question: str
    answer: str
    categories: List[str]
    frequency: int = 0
    examples: List[dict] = []

class Statistics(BaseModel):
    """统计数据模型"""
    total_contacts: int
    total_messages: int
    total_faq: int
    active_contacts: int
    top_contacts: List[dict]
    message_distribution: dict

# ============ 数据加载 ============

def load_contacts() -> List[dict]:
    """加载联系人数据"""
    contacts_file = EXPORT_DIR / "contacts.json"
    if contacts_file.exists():
        with open(contacts_file, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
        # 添加默认字段
        for contact in contacts:
            contact.setdefault('message_count', 0)
            contact.setdefault('last_active', None)
            contact.setdefault('brand', None)
        return contacts
    return []

def load_messages(contact_id: str = None) -> List[dict]:
    """加载消息数据"""
    if contact_id:
        chat_file = EXPORT_DIR / "chats" / f"{contact_id}.json"
        if chat_file.exists():
            with open(chat_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    # 加载所有消息（简化版，实际应该分页）
    messages_file = EXPORT_DIR / "messages_simplified.csv"
    if messages_file.exists():
        import pandas as pd
        df = pd.read_csv(messages_file, nrows=1000)  # 限制加载数量
        return df.to_dict('records')
    return []

def load_faq() -> List[dict]:
    """加载FAQ数据"""
    faq_file = EXPORT_DIR / "faq_knowledge_base.json"
    if faq_file.exists():
        with open(faq_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('faq', [])
    return []

def load_statistics() -> dict:
    """加载统计数据"""
    stats_file = EXPORT_DIR / "statistics.json"
    if stats_file.exists():
        with open(stats_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# ============ API路由 ============

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """首页"""
    stats = load_statistics()
    contacts = load_contacts()
    
    # 计算统计信息
    total_contacts = len(contacts)
    total_messages = stats.get('total_messages', 0)
    total_faq = len(load_faq())
    
    # 获取活跃联系人（消息数最多的前10个）
    active_contacts = sorted(contacts, key=lambda x: x.get('message_count', 0), reverse=True)[:10]
    
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={
            "total_contacts": total_contacts,
            "total_messages": total_messages,
            "total_faq": total_faq,
            "active_contacts": active_contacts,
        }
    )

@app.get("/contacts", response_class=HTMLResponse)
async def contacts_page(request: Request):
    """联系人列表页面"""
    contacts = load_contacts()
    return templates.TemplateResponse(
        name="contacts.html",
        request=request,
        context={"contacts": contacts}
    )

@app.get("/contacts/{contact_id}", response_class=HTMLResponse)
async def contact_detail(request: Request, contact_id: str):
    """联系人详情页面"""
    contacts = load_contacts()
    contact = next((c for c in contacts if c.get('id') == contact_id), None)
    
    if not contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    
    messages = load_messages(contact_id)
    
    return templates.TemplateResponse(
        name="contact_detail.html",
        request=request,
        context={"contact": contact, "messages": messages}
    )

@app.get("/messages", response_class=HTMLResponse)
async def messages_page(request: Request, contact_id: str = None):
    """聊天记录页面"""
    messages = load_messages(contact_id)
    contacts = load_contacts()
    
    return templates.TemplateResponse(
        name="messages.html",
        request=request,
        context={
            "messages": messages,
            "contacts": contacts,
            "selected_contact": contact_id,
        }
    )

@app.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    """FAQ知识库页面"""
    faq_items = load_faq()
    
    # 获取所有类别
    categories = list(set(item.get('category', '未分类') for item in faq_items))
    
    return templates.TemplateResponse(
        name="faq.html",
        request=request,
        context={"faq_items": faq_items, "categories": categories}
    )

@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    """分析页面"""
    return templates.TemplateResponse(
        name="analysis.html",
        request=request,
        context={}
    )

# ============ API接口 ============

@app.get("/api/contacts", response_model=List[Contact])
async def api_contacts(
    page: int = 1,
    page_size: int = 50,
    search: str = None,
    brand: str = None
):
    """获取联系人列表"""
    contacts = load_contacts()
    
    # 搜索过滤
    if search:
        contacts = [
            c for c in contacts
            if search.lower() in c.get('nickname', '').lower()
            or search.lower() in c.get('remark', '').lower()
        ]
    
    # 品牌过滤
    if brand:
        contacts = [c for c in contacts if c.get('brand') == brand]
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    paginated_contacts = contacts[start:end]
    
    return paginated_contacts

@app.get("/api/contacts/{contact_id}")
async def api_contact_detail(contact_id: str):
    """获取联系人详情"""
    contacts = load_contacts()
    contact = next((c for c in contacts if c.get('id') == contact_id), None)
    
    if not contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    
    return contact

@app.get("/api/contacts/{contact_id}/messages")
async def api_contact_messages(
    contact_id: str,
    page: int = 1,
    page_size: int = 50
):
    """获取联系人消息"""
    messages = load_messages(contact_id)
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    paginated_messages = messages[start:end]
    
    return paginated_messages

@app.get("/api/messages")
async def api_messages(
    page: int = 1,
    page_size: int = 50,
    search: str = None
):
    """获取消息列表"""
    messages = load_messages()
    
    # 搜索过滤
    if search:
        messages = [
            m for m in messages
            if search.lower() in m.get('content', '').lower()
        ]
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    paginated_messages = messages[start:end]
    
    return paginated_messages

@app.get("/api/faq", response_model=List[FAQItem])
async def api_faq(
    page: int = 1,
    page_size: int = 50,
    category: str = None,
    search: str = None
):
    """获取FAQ列表"""
    faq_items = load_faq()
    
    # 类别过滤
    if category:
        faq_items = [item for item in faq_items if item.get('category') == category]
    
    # 搜索过滤
    if search:
        faq_items = [
            item for item in faq_items
            if search.lower() in item.get('question', '').lower()
            or search.lower() in item.get('answer', '').lower()
        ]
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    paginated_faq = faq_items[start:end]
    
    return paginated_faq

@app.get("/api/statistics")
async def api_statistics():
    """获取统计数据"""
    stats = load_statistics()
    contacts = load_contacts()
    faq_items = load_faq()
    
    # 计算额外统计
    total_contacts = len(contacts)
    total_faq = len(faq_items)
    
    # 品牌统计
    brand_stats = {}
    for contact in contacts:
        brand = contact.get('brand', '未知')
        brand_stats[brand] = brand_stats.get(brand, 0) + 1
    
    # 消息分布（按小时）
    message_distribution = stats.get('message_distribution', {})
    
    return {
        "total_contacts": total_contacts,
        "total_messages": stats.get('total_messages', 0),
        "total_faq": total_faq,
        "active_contacts": stats.get('active_contacts', 0),
        "brand_stats": brand_stats,
        "message_distribution": message_distribution,
    }

@app.get("/api/search")
async def api_search(
    q: str,
    type: str = "all"  # all, contacts, messages, faq
):
    """全局搜索"""
    results = {
        "contacts": [],
        "messages": [],
        "faq": [],
    }
    
    if type in ["all", "contacts"]:
        contacts = load_contacts()
        results["contacts"] = [
            c for c in contacts
            if q.lower() in c.get('nickname', '').lower()
            or q.lower() in c.get('remark', '').lower()
        ][:10]  # 限制返回数量
    
    if type in ["all", "messages"]:
        messages = load_messages()
        results["messages"] = [
            m for m in messages
            if q.lower() in m.get('content', '').lower()
        ][:10]
    
    if type in ["all", "faq"]:
        faq_items = load_faq()
        results["faq"] = [
            item for item in faq_items
            if q.lower() in item.get('question', '').lower()
            or q.lower() in item.get('answer', '').lower()
        ][:10]
    
    return results

# ============ 启动配置 ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
