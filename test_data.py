#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据加载
"""

import json
from pathlib import Path

EXPORT_DIR = Path(r"F:\软件安装\WorkBuddy项目储存\2026-05-31-task-29\wechat-decrypt\export")

def test_contacts():
    """测试联系人数据加载"""
    contacts_file = EXPORT_DIR / "contacts.json"
    if contacts_file.exists():
        with open(contacts_file, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
        print(f"✅ 联系人数据加载成功: {len(contacts)} 人")
        print(f"   第一个联系人: {contacts[0] if contacts else '无'}")
        return True
    else:
        print("❌ 联系人文件不存在")
        return False

def test_faq():
    """测试FAQ数据加载"""
    faq_file = EXPORT_DIR / "faq_knowledge_base.json"
    if faq_file.exists():
        with open(faq_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            faq_items = data.get('faq', [])
        print(f"✅ FAQ数据加载成功: {len(faq_items)} 条")
        if faq_items:
            print(f"   第一条FAQ: {faq_items[0]}")
        return True
    else:
        print("❌ FAQ文件不存在")
        return False

def test_statistics():
    """测试统计数据加载"""
    stats_file = EXPORT_DIR / "statistics.json"
    if stats_file.exists():
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        print(f"✅ 统计数据加载成功")
        print(f"   总联系人: {stats.get('total_contacts', 0)}")
        print(f"   总消息数: {stats.get('total_messages', 0)}")
        return True
    else:
        print("❌ 统计文件不存在")
        return False

def test_messages():
    """测试消息数据加载"""
    messages_file = EXPORT_DIR / "messages_simplified.csv"
    if messages_file.exists():
        print(f"✅ 消息文件存在: {messages_file}")
        return True
    else:
        print("❌ 消息文件不存在")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("数据加载测试")
    print("=" * 50)
    
    test_contacts()
    test_faq()
    test_statistics()
    test_messages()
    
    print("=" * 50)
    print("测试完成")
    print("=" * 50)