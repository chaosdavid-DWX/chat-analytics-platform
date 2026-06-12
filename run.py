#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信AI知识管理平台 - 启动脚本
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
